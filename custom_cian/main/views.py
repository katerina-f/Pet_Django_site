from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Realty, Tag, Saller
from .forms import RealtyForm


def index(request):
    turn_on_block = True
    params = {"turn_on_block": turn_on_block, "current_user": request.user}
    return render(request, "main/index.html", params)


class RealtyListView(ListView):
    paginate_by = 1
    model = Realty

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["current_user"] = self.request.user
        context["current_tag"] = self.request.GET.get("tag") if self.request.GET.get("tag") else ""
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if tag_name := self.request.GET.get("tag"):
            queryset = Realty.objects.filter(tags__name=tag_name)

        return queryset


class RealtyDetailView(DetailView):
    model = Realty


class SallerUpdateView(LoginRequiredMixin, UpdateView):
    model = Saller
    fields = ["first_name", "last_name"]


class RealtyCreateView(LoginRequiredMixin, CreateView):
    model = Realty
    form_class = RealtyForm

    def form_valid(self, form):
        messages.success(self.request, "Сохранение успешно!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Сохранение не удалось - проверьте правильность данных!")
        return super().form_invalid(form)


class RealtyUpdateView(LoginRequiredMixin, UpdateView):
    model = Realty
    form_class = RealtyForm

    def form_valid(self, form):
        messages.success(self.request, "Сохранение успешно!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Сохранение не удалось - проверьте правильность данных!")
        return super().form_invalid(form)
