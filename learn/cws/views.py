from django.shortcuts import redirect,render
from cws.models import *
from django.views.generic import ListView,View,DetailView
from django.core.exceptions import ObjectDoesNotExist



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
    


class OrderSummary(View):

    def get(self,*args,**kwargs):
        try:
            order = Order.objects.filter(user=self.request.user,ordered=False)
            context = {"order":order}
        except ObjectDoesNotExist:
            #todo msg: order not found
            return redirect("/")
        return render(self.request,"public/cart.html",context)

    model = Order
    template_name = "public/cart.html"

    
    
