from django.shortcuts import render


def index(request):
    turn_on_block = True
    params = {"turn_on_block": turn_on_block}
    return render(request, "main/index.html", params)
