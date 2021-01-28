from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Realty, Saller

def index(request):
    turn_on_block = True
    params = {"turn_on_block": turn_on_block, "current_user": request.user}
    return render(request, "main/index.html", params)


class RealtyListView(ListView):
    model = Realty


class RealtyDetailView(DetailView):
    model = Realty

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['book_list'] = Book.objects.all()
    #     return context
