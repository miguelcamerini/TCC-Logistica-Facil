from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),   # Sua rota de login personalizada
    path('logout/', views.logout_view, name='logout'), # Rota para deslogar o usuário
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('home/', views.home, name='home'),

]
