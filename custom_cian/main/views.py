from django.shortcuts import render


def index(request):
    params = {"current_user": request.user}
    return render(request, "main/index.html", params)
