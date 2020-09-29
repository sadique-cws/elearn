from django.shortcuts import redirect,render


def home(req):
    return render(req,"public/home.html")