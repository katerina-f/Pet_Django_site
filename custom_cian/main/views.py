from typing import Union, Type, Tuple, Optional

from django.contrib.auth.mixins import LoginRequiredMixin, \
                                       UserPassesTestMixin, \
                                       PermissionRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.views.generic.edit import ModelFormMixin
from django.db.models.signals import post_save
from django.db.models import QuerySet, Model
from django.dispatch import receiver
from django.forms import BaseForm
from django.http import Http404, \
                        HttpRequest, \
                        HttpResponse, \
                        HttpResponseRedirect, \
                        HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Realty, Tag, Saller, Subscriber
from .forms import RealtyForm, SallerProfileForm

from .tasks import send_email_task


def get_common_users_group() -> Group:
    common_users, created = Group.objects.get_or_create(name="common_users")
    if created:
        common_users.permissions.set(
            list(
                Permission.objects.filter(codename__icontains="saller").
                exclude(codename__startswith="delete")
                )
        )
    return common_users


@receiver(post_save, sender=User)
def create_user_profile(sender: User, instance: User, created: bool, **kwargs) -> None:
    if kwargs['raw']:
        return
    if created:
        instance.groups.add(get_common_users_group())
        Saller.objects.create(email=instance.email,
                              created_by=instance,
                              first_name=instance.first_name,
                              last_name=instance.last_name)
        Subscriber.objects.create(user=instance,
                                  novelty_subscribed=False)
        if instance.email:
            send_email_task([instance, ],
                            "main/email_templates/registration_email.html",
                            "Регистрация на сайте")


@receiver(post_save, sender=Realty)
def create_realty_object(sender: Realty, instance: Realty, created: bool, **kwargs) -> None:
    if kwargs['raw']:
        return
    if created:
        for s in Subscriber.objects.all():
            send_email_task.delay({"username": s.user.username, "email": s.user.email},
                                  "main/email_templates/novelty_email.html",
                                  "Появилась новинка!", new_object_url=instance.get_absolute_url(),
                                  new_object_name=instance.name, new_object_price=instance.price)


@csrf_protect
@login_required
def subscribe_on_novelty(request: HttpRequest) -> \
                         Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    if request.POST:
        subscriber, created = Subscriber.objects.get_or_create(user=request.user)
        subscriber.novelty_subscribed = True
        subscriber.save()
        messages.success(request, "Вы успешно подписались на новинки!")
    return redirect('realty_list')


def index(request: HttpRequest) -> HttpResponse:
    turn_on_block = True
    params = {"turn_on_block": turn_on_block}
    return render(request, "main/index.html", params)


class RealtyListView(ListView):
    paginate_by: int = 10
    model: Type[Model] = Realty

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["current_tag"] = self.request.GET.get("tag") if self.request.GET.get("tag") else ""
        return context

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        if tag_name := self.request.GET.get("tag"):
            queryset = Realty.objects.filter(tags__name=tag_name)

        return queryset


class RealtyDetailView(DetailView):
    model: Type[Model] = Realty

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        self.object.counter += 1
        self.object.save()

        counter = cache.get_or_set(f"{self.object.pk}_counter", self.object.counter, 60)
        context["counter"] = counter
        return context


class SallerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model: Type[Model] = Saller
    template_name_suffix: str = '_update_form'
    form_class: Optional[Type[BaseForm]] = SallerProfileForm

    def form_valid(self, form: ModelFormMixin) -> HttpResponse:
        messages.success(self.request, "Обновление успешно!")
        return super().form_valid(form)

    def form_invalid(self, form: SallerProfileForm) -> HttpResponse:
        messages.error(self.request, "Обновление не удалось - проверьте правильность данных!")
        return super().form_invalid(form)

    def get_object(self) -> Saller:
        try:
            user = User.objects.get(pk=self.kwargs.get("slug"))
        except User.DoesNotExist:
            raise Http404

        saller, created = Saller.objects.get_or_create(created_by=user)
        if created:
            saller.email = user.email
            saller.first_name = user.first_name
            saller.last_name = user.last_name
            saller.save()
        return saller

    def test_func(self) -> bool:
        obj = self.get_object()
        return (obj.created_by.groups.filter(name='common_users').exists() or \
            obj.created_by.is_staff) and obj.created_by.pk == self.request.user.pk


class RealtyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model: Type[Model] = Realty
    form_class: Optional[Type[BaseForm]] = RealtyForm
    permission_required: Tuple[Optional[str]] = ("main.add_realty", )

    def form_valid(self, form: RealtyForm) -> HttpResponse:
        messages.success(self.request, "Сохранение успешно!")
        return super().form_valid(form)

    def form_invalid(self, form: RealtyForm) -> HttpResponse:
        messages.error(self.request,
                       "Сохранение не удалось - проверьте правильность данных!")
        return super().form_invalid(form)


class RealtyUpdateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       UserPassesTestMixin,
                       UpdateView):
    model: Type[Model] = Realty
    form_class: Optional[Type[BaseForm]] = RealtyForm
    permission_required: Tuple[Optional[str]] = ("main.change_realty", )

    def form_valid(self, form: RealtyForm) -> HttpResponse:
        messages.success(self.request, "Сохранение успешно!")
        return super().form_valid(form)

    def form_invalid(self, form: RealtyForm) -> HttpResponse:
        messages.error(self.request, "Сохранение не удалось - проверьте правильность данных!")
        return super().form_invalid(form)

    def test_func(self) -> bool:
        return self.request.user.id == self.get_object().saller.created_by.id
