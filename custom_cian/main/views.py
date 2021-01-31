from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView

from .models import Realty, Tag, Saller
from .forms import SallerProfileForm


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
    template_name_suffix = '_update_form'
    form_class = SallerProfileForm
