from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django import forms
from .models import Veiculo
# Create your views here.

def index(request):
    return HttpResponse("Olá, mundo! Você está no index do app de enquetes.")

#-------------------------------
def login_view(request):
    if request.method == 'POST':
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')
        # O authenticate já faz a verificação segura da senha criptografada
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)
        if user is not None:
            login(request, user)
            return redirect('home') # Redireciona para a página principal
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    return render(request, 'login.html')

#-------------------------------
def logout_view(request):
    logout(request)
    return redirect('login') # Redireciona de volta para o login após sair

#-------------------------------
def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Salva o novo usuário no banco de dados
            messages.success(request, "Conta criada com sucesso! Faça o login.")
            return redirect('login') # Redireciona para o login
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastro.html', {'form': form})

#-------------------------------
@login_required
def home(request):
    meus_veiculos = Veiculo.objects.filter(usuario=request.user)
    return render(request, 'home.html', {'veiculos': meus_veiculos})





#-------------------------------VEICULOS
@login_required
def lista_veiculos(request):
    # O filter garante que o Miguel só veja os veículos do Miguel, o João os do João, etc.
    meus_veiculos = Veiculo.objects.filter(usuario=request.user)
    
    # Passamos a lista de veículos para o HTML através do contexto
    return render(request, 'enterprise/veiculo/veiculo.html', {'veiculos': meus_veiculos})

#-------------------------------
# 1. Criamos um ModelForm para facilitar a geração dos campos no HTML
class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        # ATENÇÃO: Removemos o campo 'usuario' daqui para o usuário logado não poder escolher outro dono
        fields = [
            'nome_fantasia', 'placa', 'chassi', 'renavam', 
            'ano_fabricacao', 'ano_modelo', 'status', 'descricao'
        ]

# 2. A View protegida por login
@login_required
def add_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            # commit=False impede o Django de salvar direto no banco ainda
            veiculo = form.save(commit=False)
            
            # Aqui está o segredo: associamos o veículo ao usuário logado
            veiculo.usuario = request.user 
            
            # Agora sim, salvamos no banco de dados
            veiculo.save()
            return redirect('lista_veiculos') # Altere para a rota que você desejar após salvar
    else:
        form = VeiculoForm()
        
    return render(request, 'enterprise/veiculo/add_veiculo.html', {'form': form})

@login_required
def editar_veiculo(request, pk):
    # Obtém o veículo pelo ID (pk) e garante que pertence ao usuário logado
    veiculo = get_object_or_404(Veiculo, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        # Atualiza o registro existente
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Veículo {veiculo.placa} atualizado com sucesso!")
            return redirect('lista_veiculos')
    else:
        # Preenche o formulário com os dados atuais do veículo para edição
        form = VeiculoForm(instance=veiculo)
        
    # Aponta para o novo template específico de edição e passa o veículo
    return render(request, 'enterprise/veiculo/editar_veiculo.html', {
        'form': form, 
        'veiculo': veiculo
    })

#-------------------------------
@login_required
def excluir_veiculo(request, pk):
    # Obtém o veículo e garante que pertence ao usuário logado por segurança
    veiculo = get_object_or_404(Veiculo, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        placa = veiculo.placa
        veiculo.delete()
        messages.success(request, f"Veículo com placa {placa} foi excluído.")
    
    return redirect('lista_veiculos')