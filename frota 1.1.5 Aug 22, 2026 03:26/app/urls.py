from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.login_view, name='login'),
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
    
    path('viagens/', views.lista_viagem, name='lista_viagem'),
    path('viagens/adicionar/', views.add_viagem, name='add_viagem'),
    path('viagens/editar/<int:pk>/', views.edit_viagem, name='edit_viagem'),
    path('viagens/excluir/<int:pk>/', views.excluir_viagem, name='excluir_viagem'),
    
    # app/urls.py
    path('caixa/', views.lista_caixa, name='lista_caixa'),
    path('caixa/adicionar-despesa/', views.despesa_caixa, name='add_despesa_caixa'),
    path('caixa/adicionar-entrada/', views.entrada_caixa, name='add_entrada_caixa'),
    path('caixa/editar/<int:pk>/', views.edit_caixa, name='edit_caixa'),
    path('caixa/excluir/<int:pk>/', views.excluir_caixa, name='excluir_caixa'),  
        
    path('perfil/', views.perfil_user, name='perfil_user'),
    path('perfil/editar/', views.edit_user, name='edit_user'),
    path('perfil/alterar-senha/', views.alterar_senha_user, name='alterar_senha_user'),

    path('nao-autorizado/', views.nao_autorizado_view, name='nao_autorizado'),
]

