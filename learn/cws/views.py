from django.shortcuts import redirect,render
from cws.models import *
from django.views.generic import ListView,View,DetailView



class HomeView(ListView):
    model = Category
    template_name = "public/home.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all() 
        return context
    

class CourseView(DetailView):
    model = Course
    template_name = "public/course.html"
    slug_url_kwarg = 'slug'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["item"] = Course.objects. 
    #     return context
    

