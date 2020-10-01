from django.shortcuts import redirect,render,get_object_or_404
from cws.models import *
from django.views.generic import ListView,View,DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


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
            order = OrderItem.objects.filter(user=self.request.user,ordered=False)
            context = {"order":order}
        except ObjectDoesNotExist:
            #todo msg: order not found
            return redirect("/")
        return render(self.request,"public/cart.html",context)

    model = Order
    template_name = "public/cart.html"

    
    
class AddToCart(View):
    def get(self,request,slug,*args,**kwargs):
        item = get_object_or_404(Course,slug=slug)

        order_item, create = OrderItem.objects.get_or_create(
            items=item,
            user = self.request.user,
            ordered=False
        )
        
        order_qs = Order.objects.filter(user=self.request.user,ordered=False)
        
        if order_qs.exists():
            order = order_qs[0]
            if OrderItem.objects.filter(items__slug=item.slug).exists():
                #todo msg: this item already in your cart
                return redirect('cart')
            else:
                 order.items.add(order_item)
                 #todo msg: this course add in your cart success 
                 return redirect('cart')
        else:
            orderDate = timezone.now()
            order = Order.objects.create(user=self.request.user,ordered=False,starting_date=orderDate,ordered_date=orderDate)
            order.items.add(order_item)
            order.save()
            #todo : msg: this course add in your cart successfully
            return redirect("cart")

        

