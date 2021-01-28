from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Realty, Tag


def index(request):
    turn_on_block = True
    params = {"turn_on_block": turn_on_block, "current_user": request.user}
    return render(request, "main/index.html", params)


class RealtyListView(ListView):
    paginate_by = 2
    model = Realty

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["tags"] = Tag.objects.all()
        return context


class RealtyDetailView(DetailView):
    model = Realty
