from django.shortcuts import redirect, render, get_object_or_404
from cws.models import *
from django.views.generic import ListView, View, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from cws.forms import AddressForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import string
import random

cart_obj = OrderItem.objects.all()

def create_ref_code(digit):
    return "".join(random.choices(string.digits,k=digit))

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


class CartView(LoginRequiredMixin,ListView):
    model = Course
    template_name = "public/cart.html"


class OrderSummary(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            orderItem = OrderItem.objects.filter(user=self.request.user, ordered=False)
            context = {"order": order, "orderitem": orderItem}
        except ObjectDoesNotExist:
            # todo msg: order not found
            return redirect("/")
        return render(self.request, "public/cart.html", context)

    model = Order
    template_name = "public/cart.html"


class RemoveCartItem(LoginRequiredMixin,View):
    def get(self, request, slug, *args, **kwargs):
        item = get_object_or_404(Course, slug=slug)

        order_qs = Order.objects.filter(user=self.request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order.items.remove()
                oi = OrderItem.objects.get(item__slug=item.slug, user=request.user, ordered=False)
                oi.delete()
                return redirect('cart')
        else:
            return redirect("cart")


class AddToCart(LoginRequiredMixin,View):
    def get(self, request,  slug, *args, **kwargs):
        item = get_object_or_404(Course, slug=slug)

        order_item, create = OrderItem.objects.get_or_create(
            item=item,
            user=self.request.user,
            ordered=False
        )

        order_qs = Order.objects.filter(user=self.request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                # todo msg: this item already in your cart
                return redirect('cart')
            else:
                order.items.add(order_item)
                # todo msg: this course add in your cart success
                return redirect('cart')
        else:
            orderDate = timezone.now()
            order = Order.objects.create(user=self.request.user, ordered=False, starting_date=orderDate,
                                         ordered_date=orderDate)
            order.items.add(order_item)
            order.save()
            # todo : msg: this course add in your cart successfully
            return redirect("cart")


def check_coupon(code):
    coupon = Coupon.objects.filter(code=code, status=True)
    if coupon.exists():
        return coupon[0]

@login_required
def add_coupon(r):
    if r.method == "POST":
        code = r.POST.get('code')

        if check_coupon(code):
            order = Order.objects.get(user=r.user, ordered=False)
            order.coupon = check_coupon(code)
            order.save()
            return redirect('cart')
        else:
            # msg this is code is very very bad we can't accepts
            return redirect('cart')
    else:
        # msg something went wrong
        return redirect('cart')


@login_required
def makePayment(r):
    order = Order.objects.filter(user=r.user,ordered=False)
    order = order[0]
    order.ordered = True
    order.ref_code = create_ref_code(8)
    order.save()

    for x in order.items.all():
        x.ordered = True
        x.save()

@login_required
def checkout(r):
    form = AddressForm(r.POST or None)
    
    # user = User.objects.get(username=r.user.username)

    if r.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.user = r.user
            f.save()

            return redirect("checkout")

    data = {"addressForm":form,"address":Address.objects.filter(user=r.user)}
    return render(r,"public/checkout.html",data)

@login_required
def last_step(r):
    if r.method == "POST":
        address = r.POST.get("address")

        try:
            address = Address.objects.get(user=r.user,id=address)
        except ObjectDoesNotExist:
            #msg this address is not found in your account
            return redirect("checkout")
        
        order = Order.objects.filter(user=r.user, ordered=False)
        order = order[0]
        order.address = address
        order.save()
        makePayment(r)
        return redirect("my-courses")

class RemoveAppliedCoupon(View,LoginRequiredMixin):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.coupon:
                order.coupon = None
                order.save()
            return redirect("cart")
        except ObjectDoesNotExist:
            return redirect("cart")


def myCourse(r):
    order = Order.objects.filter(user=r.user,ordered=True)
    data = {"order":order}
    return render(r,"student/my_courses.html",data)
