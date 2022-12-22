from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    # path(r'products/^(?P<category_slug>[-\w]+)/$',
    #      views.product_list,
    #      name='product_list_by_category'),
    # path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
    #      views.product_detail,
    #      name='product_detail'),
    path('courier-form/', views.contact_view, name='contact_view'),
    path('courier-form/success/', views.success_view, name='success'),
    path('new-order/', views.new_order, name='new_order')
]
