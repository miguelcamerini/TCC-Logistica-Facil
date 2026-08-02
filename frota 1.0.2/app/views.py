from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.

def index(request):
    return HttpResponse("Olá, mundo! Você está no index do app de enquetes.")

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

def home(request):
    return render(request, 'home.html')