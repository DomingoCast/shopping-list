
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('congrats/', views.congrats),
    path('lista/<str:pk>/', views.lista),
    path('new_lista/', views.new_lista ,name = 'newLista'),
    path('login2/', views.login2 ),
    path('register/', views.registerPage,name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profilePage, name = 'profile'),
    path('familia/<str:pk>/', views.familia, name = 'familia'),

]

