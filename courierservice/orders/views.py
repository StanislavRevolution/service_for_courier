from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy

from .forms import CourierForm, OrderForm
from users.forms import CourierSignUpForm
from orders.models import CourierProfile, Product
from .utils import try_to_send_mail

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
        template_name="orders/../templates/authorization/applying_for_courier.html",
        context={'form': form}
    )


def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')


def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "orders/index.html", context)


def new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.client = request.user
            commit.save()
            return redirect('orders:index')
        return render(request, 'orders/new_order.html', {'form': form})
    form = OrderForm()

    return render(request, "orders/new_order.html", {'form': form})


class CouriersSignUpView(CreateView):
    model = User
    form_class = CourierSignUpForm
    template_name = 'orders/../templates/authorization/signup_couriers_form.html'
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