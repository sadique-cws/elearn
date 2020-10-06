from django.shortcuts import redirect, render, get_object_or_404
from cws.models import *
from django.views.generic import ListView, View, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


cart_obj = OrderItem.objects.all()


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


class CartView(ListView):
    model = Course
    template_name = "public/cart.html"


class OrderSummary(View):

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


class RemoveCartItem(View):
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


class AddToCart(View):
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


class RemoveAppliedCoupon(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.coupon:
                order.coupon = None
                order.save()
            return redirect("cart")
        except ObjectDoesNotExist:
            return redirect("cart")
