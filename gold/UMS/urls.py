from django.urls import path
from UMS.views import admin_dashboard
from UMS.views.admin_create_user import admin_create_user
from UMS.views.admin_users import admin_users
from UMS.views.create_user_category import create_user_category
from UMS.views.delete_user import delete_user
from UMS.views.delete_user_category import delete_user_category
from UMS.views.do_logout import do_logout
from UMS.views.edit_user import edit_user
from UMS.views.edit_user_category import edit_user_category
from UMS.views.do_login import do_login
from UMS.views.toggle_user_status import toggle_user_status
from UMS.views.user_category_list import user_category_list
from UMS.views.user_dashboard import user_dashboard

urlpatterns = [

    path('', do_login, name='do_login'),

    path('do_logout/', do_logout, name='do_logout'),

    path("admin-panel/create-user/", admin_create_user, name="admin_create_user"),

   path("admin-panel/edit-user/<int:user_id>/", edit_user, name="edit_user"),

    path("admin-panel/users/", admin_users, name="admin_users"),

   path("admin-panel/toggle-user/<int:user_id>/", toggle_user_status, name="toggle_user_status"),

   path("admin-panel/delete-user/<int:user_id>/", delete_user, name="delete_user"),

    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),

    path('user_dashboard/', user_dashboard, name='user_dashboard'),

    path('user_category_list/', user_category_list, name='user_category_list'),

    path('create_user_category/', create_user_category, name='create_user_category'),

    path('edit_user_category/<int:pk>/', edit_user_category, name='edit_user_category'),

    path('delete_user_category/<int:pk>/', delete_user_category, name='delete_user_category'),




]
