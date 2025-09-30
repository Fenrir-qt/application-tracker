from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.home, name='dashboard'),
    path("add-application/", views.add_application, name="add_application"),
    path('update-application/<int:id>/', views.edit_application, name="edit_application"),
    path('delete-application/<int:id>/', views.delete_application, name="delete_application")
]
