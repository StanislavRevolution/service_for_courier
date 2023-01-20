from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy

from .forms import CourierForm, OrderForm, CommentForm
from users.forms import CourierSignUpForm, UserSignUpForm
from .models import CourierProfile, Product, OrderItem, Order
from .utils import try_to_send_mail
from cart.forms import CartAddProductForm
from cart.cart import Cart

User = get_user_model()


@require_http_methods(["GET", "POST"])
def contact_view(request):
    if request.method == 'POST':
        form = CourierForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try_to_send_mail(email)
            return redirect('success/')
    form = CourierForm()
    return render(
        request,
        template_name="authorization/applying_for_courier.html",
        context={'form': form}
    )


def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')


@login_required()
def add_comment(request, pk):
    current_courier = get_object_or_404(CourierProfile, pk=pk)
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.courier = current_courier
        new_comment.user = request.user
        new_comment.save()
    return redirect('orders:courier_profile', pk=pk)


def index(request):
    products = Product.objects.all()[:3]
    couriers = CourierProfile.objects.all()
    form = CourierForm()
    context = {
        'products': products,
        'couriers': couriers,
        'form': form
    }
    return render(request, "orders/index4.html", context)


def new_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.paid = True
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']

                )
            cart.clear()
            return render(request, 'orders/sucess_order.html')
    form = OrderForm()
    return render(request, "orders/new_order.html", {'form': form})


@require_POST
@login_required
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    courier = get_object_or_404(CourierProfile, user=request.user)
    courier.orders.add(order)
    order.status = 'GT'
    order.save()
    return redirect('orders:index')


class CouriersSignUpView(CreateView):
    model = User
    form_class = CourierSignUpForm
    template_name = 'authorization/signup_couriers_form.html'
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'courier'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        valid = super(CouriersSignUpView, self).form_valid(form)
        user = form.save(commit=False)
        user.is_courier = True
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        CourierProfile.objects.create(user=user)
        return valid


class ProductsListView(ListView):
    model = Product
    template_name = 'orders/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context


class OrdersListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'


class CourierUpdateView(UpdateView):
    model = User
    template_name = 'authorization/signup_couriers_form.html'
    fields = ('username', 'email', 'phoneNumber', 'first_name', 'last_name')
    # form_class = UserSignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class CourierDetailView(DetailView):
    model = CourierProfile
    template_name = 'orders/courier_profile.html'
    context_object_name = 'courier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        return context


def order_of_clients(request, id):
    user = get_object_or_404(User, id=id)
    orders_of_user = user.all_orders.all().order_by('-pk')
    return render(
        request,
        'orders/user_orders.html',
        {'orders_of_user': orders_of_user}
    )


def own_profile(request, id):
    author = get_object_or_404(CourierProfile, pk=id)
    last_orders_by_courier = author.orders.order_by('-pk')[:2]
    form = CourierForm(request.POST or None)

    context = {
        'author': author,
        'last_orders_by_courier': last_orders_by_courier
    }
    return render(request, 'orders/own_profile.html', context)
