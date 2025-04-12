from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import register_view, login_view, logout_view

app_name = 'boards'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_board, name='create_board'),
    path('boards/<uuid:board_id>/', views.board_view, name='boards'),
    path('boards/<uuid:board_id>/delete/', views.delete_board, name='delete_board'),
    path('boards/<int:board_id>/', views.board_view, name='board_view'),
    path('<uuid:board_id>/', views.board_view, name='board_view'),
    path('<uuid:board_id>/pdf/', views.show_pdf, name='show_pdf'),
    path('<uuid:board_id>/save_drawing/', views.save_drawing, name='save_drawing'),


    path('register/', register_view, name='register'),  # регистрация
    path('login/', login_view, name='login'),  # стандартный вход
    path('logout/', logout_view, name='logout'),  # выход

]