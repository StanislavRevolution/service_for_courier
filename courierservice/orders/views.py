from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy

from .forms import CourierForm, OrderForm
from users.forms import UserSignUpForm, CourierSignUpForm
from orders.models import CourierProfile, Category, Product

User = get_user_model()


def product_list(request, category_slug=None):
    category = None
    print('1')
    # categories = Category.objects.all()
    print('2')
    products = Product.objects.filter(available=True)
    print('3')
    # context = {'category': category,
    #            'categories': categories,
    #            'products': products}
    # if category_slug:
    #     category = get_object_or_404(Category, slug=category_slug)
    #     products = products.filter(category=category)
    return render(request, template_name='orders/product_list.html', context={'products':products})



def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    # return render(request,
    #               'shop/product/detail.html',
    #               {'product': product})


def try_to_send_mail(email):
    try:
        send_mail(
            'Спасибо, что подали заявку на работу в нашей компании',
            'Пройдите регистрацию на курьера по данной ссылке:  '
            'http://127.0.0.1:8000/auth/signup_for_couriers/',
            'courierjob@mail.ru',  # Это поле "От кого"
            [email],  # Это поле "Кому" (можно указать список адресов)
            fail_silently=False,
        )
    except Exception as e:
        return HttpResponse(f'Ошибка при отправке письма: {e}')


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
        template_name="orders/applying_for_courier.html",
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
    template_name = 'orders/signup_couriers_form.html'
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


