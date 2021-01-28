from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Realty, Saller


def index(request):
    turn_on_block = True
    params = {"turn_on_block": turn_on_block, "current_user": request.user}
    return render(request, "main/index.html", params)


class RealtyListView(ListView):
    paginate_by = 10
    model = Realty


class RealtyDetailView(DetailView):
    model = Realty
