from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductsListView.as_view(), name='product_list'),
    path('courier_form/', views.contact_view, name='contact_view'),
    path('courier_form/success/', views.success_view, name='success'),
    path('new_order/', views.new_order, name='new_order')
]
