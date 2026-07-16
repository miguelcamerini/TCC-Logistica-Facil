from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),   
    path('logout/', views.logout_view, name='logout'), 
    path('cadastro/', views.cadastro_view, name='cadastro'),
    
    path('home/', views.home, name='home'),
    
    
    
    
    
    
    path('lista_veiculos/', views.lista_veiculos, name='lista_veiculos'),
    path('add_veiculo/', views.add_veiculo, name='add_veiculo'),
    path('veiculos/editar/<int:pk>/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculos/excluir/<int:pk>/', views.excluir_veiculo, name='excluir_veiculo'),
    
    path('lista_funcionario/', views.lista_funcionario, name='lista_funcionario'),
    path('add_funcionario/', views.add_funcionario, name='add_funcionario'),
    path('funcionario/editar/<int:pk>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionario/excluir/<int:pk>/', views.excluir_funcionario, name='excluir_funcionario'),
    
]

