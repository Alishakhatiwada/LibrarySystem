from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('signup/', views.signup_view, name='signup'),
    path('history/', views.history_view, name='history'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:book_id>/', views.return_book, name='return_book'),
    path('history/', views.history_view, name='history'),
    path('dashboard/', views.user_dashboard, name='dashboard'),

]


