from django.urls import path
from . import views
urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.home, name='dashboard'),
    path("add-application/", views.add_application, name="add_application"),
    path('update-application/<int:id>/', views.edit_application, name="edit_application"),
    path('delete-application/<int:id>/', views.delete_application, name="delete_application"),
    path("search-application/", views.search_application, name="search_application"),
    path('profile/', views.profile, name='profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', views.reset_password_confirm, name='password_reset_confirm'),
]
