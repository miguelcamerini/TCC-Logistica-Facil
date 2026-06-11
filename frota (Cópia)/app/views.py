from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return HttpResponse("Olá, mundo! Você está no index do app de enquetes.")
