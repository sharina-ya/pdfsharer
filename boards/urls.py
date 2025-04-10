from django.urls import path
from . import views

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
]
