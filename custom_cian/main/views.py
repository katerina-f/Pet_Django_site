from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Realty, Tag, Saller, Subscriber
from .forms import RealtyForm, SallerProfileForm

from.logic import send_information_email


def get_common_users_group():
    common_users, created = Group.objects.get_or_create(name="common_users")
    if created:
        common_users.permissions.set(list(Permission.objects.filter(codename__icontains="saller").exclude(codename__startswith="delete")))
    return common_users


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(get_common_users_group())
        saller = Saller.objects.create(email=instance.email,
                                       created_by=instance,
                                       first_name=instance.first_name,
                                       last_name=instance.last_name)
        subscriber = Subscriber.objects.create(user=instance,
                                               novelty_subscribed=False)
        if instance.email:
            send_information_email([instance, ],
                                   "main/email_templates/registration_email.html",
                                   "Регистрация на сайте")


@receiver(post_save, sender=Realty)
def create_realty_object(sender, instance, created, **kwargs):
    if created:
        subscribers = [s.user for s in Subscriber.objects.all()]
        send_information_email(subscribers, "main/email_templates/novelty_email.html",
                                "Появилась новинка!", new_object_url=instance.get_absolute_url(),
                                new_object_name=instance.name, new_object_price=instance.price)


@csrf_protect
@login_required
def subscribe_on_novelty(request):
    if request.POST:
        subscriber, created = Subscriber.objects.get_or_create(user=request.user)
        subscriber.novelty_subscribed = True
        subscriber.save()
        messages.success(request, "Вы успешно подписались на новинки!")
    return redirect('realty_list')


def index(request):
    turn_on_block = True
    params = {"turn_on_block": turn_on_block}
    return render(request, "main/index.html", params)


class RealtyListView(ListView):
    paginate_by = 10
    model = Realty

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["current_tag"] = self.request.GET.get("tag") if self.request.GET.get("tag") else ""
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if tag_name := self.request.GET.get("tag"):
            queryset = Realty.objects.filter(tags__name=tag_name)

        return queryset


class RealtyDetailView(DetailView):
    model = Realty


class SallerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Saller
    template_name_suffix = '_update_form'
    form_class = SallerProfileForm

    def form_valid(self, form):
        messages.success(self.request, "Обновление успешно!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Обновление не удалось - проверьте правильность данных!")
        return super().form_invalid(form)

    def get_object(self):
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

    def test_func(self):
        obj = self.get_object()
        return obj.created_by.groups.filter(name='common_users').exists() or obj.created_by.is_staff


class RealtyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Realty
    form_class = RealtyForm
    permission_required = ("main.add_realty", )

    def form_valid(self, form):
        messages.success(self.request, "Сохранение успешно!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Сохранение не удалось - проверьте правильность данных!")
        return super().form_invalid(form)


class RealtyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Realty
    form_class = RealtyForm
    permission_required = ("main.change_realty", )

    def form_valid(self, form):
        messages.success(self.request, "Сохранение успешно!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Сохранение не удалось - проверьте правильность данных!")
        return super().form_invalid(form)

    def test_func(self):
        return self.request.user.id == self.get_object().saller.created_by.id
