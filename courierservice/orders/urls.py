from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductsListView.as_view(), name='product_list'),
    path('courier-form/', views.contact_view, name='contact_view'),
    path('courier-form/success/', views.success_view, name='success'),
    path('new-order/', views.new_order, name='new_order')
]
