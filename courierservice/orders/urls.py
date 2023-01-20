from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductsListView.as_view(), name='product_list'),
    path('courier_profile/<int:pk>/', views.CourierDetailView.as_view(),
         name='courier_profile'),
    path('courier_profile/<int:pk>/comment/', views.add_comment,
         name='add_comment'),
    path('my_orders/<int:id>', views.order_of_clients, name='user_orders'),
    path('courier_form/', views.contact_view, name='contact_view'),
    path('courier_form/success/', views.success_view, name='success'),
    path('new_order/', views.new_order, name='new_order'),
    path('orders_list/<int:order_id>/accept/', views.accept_order,
         name='accept_order'),
    path('orders_list/', views.OrdersListView.as_view(), name='order_list'),
    path('own_profile/<int:id>/', views.own_profile, name='own_profile')

]
