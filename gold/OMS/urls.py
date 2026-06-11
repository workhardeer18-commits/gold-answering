from django.urls import path
from OMS.views import category_mazane_list, create_product, create_product_category, delete_category_mazaneh, \
    delete_product, \
    delete_product_category, edit_category_mazaneh, edit_order, \
    edit_product, edit_product_category, live_prices, order_list, \
    create_order, product_category_list


from OMS.views.product_list import product_list
from OMS.views.create_category_mazane import create_category_mazaneh

urlpatterns = [

    #orders
    path('order_list/', order_list, name='order_list'),
    path('create_order/', create_order, name='create_order'),
    path('edit_order/<int:pk>/', edit_order, name='edit_order'),




    #products
    path('product_list/', product_list, name='product_list'),
    path('create_product/', create_product, name='create_product'),
    path('edit_product/<int:pk>/', edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', delete_product, name='delete_product'),

    #product_categories
    path('product_category_list/', product_category_list, name='product_category_list'),
    path('create_product_category/', create_product_category, name='create_product_category'),

    path('edit_product_category/<int:pk>/', edit_product_category, name='edit_product_category'),

    path('delete_product_category/<int:pk>/', delete_product_category, name='delete_product_category'),



    path('category_mazane_list/', category_mazane_list, name='category_mazane_list'),

    path("create_category_mazaneh/", create_category_mazaneh, name='create_category_mazaneh'),

path(
    "mazaneh/<int:mazaneh_id>/edit/",
    edit_category_mazaneh,
    name="edit_category_mazaneh"
),

path(
    "mazaneh/<int:mazaneh_id>/delete/",
    delete_category_mazaneh,
    name="delete_category_mazaneh"
),

    path("live-prices/", live_prices, name="live_prices"),


]
