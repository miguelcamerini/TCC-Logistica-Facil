from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),   # Sua rota de login personalizada
    path('logout/', views.logout_view, name='logout'), # Rota para deslogar o usuário
    path('cadastro/', views.cadastro_view, name='cadastro'),
    
    path('home/', views.home, name='home'),
    
    
    
    
    
    path('listar_veiculos/', views.listar_veiculos, name='listar_veiculos'),
    path('add_veiculo/', views.add_veiculo, name='add_veiculo'),
    # Novas URLs para Editar e Excluir
    path('veiculos/editar/<int:pk>/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculos/excluir/<int:pk>/', views.excluir_veiculo, name='excluir_veiculo'),
    
]

