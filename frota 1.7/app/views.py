from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django import forms
from .models import Veiculo, Funcionario, StatusFuncionario, Viagem, Abastecida, Caixa 

# Create your views here.

def index(request):
    return HttpResponse("Olá, mundo! Você está no index do app de enquetes.")

#-------------------------------
def login_view(request):
    if request.method == 'POST':
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')
        # O authenticate faz a verificação segura da senha criptografada
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
            veiculo = form.save(commit=False)
            
            veiculo.usuario = request.user 
            
            veiculo.save()
            return redirect('lista_veiculos') 
    else:
        form = VeiculoForm()
        
    return render(request, 'enterprise/veiculo/add_veiculo.html', {'form': form})

@login_required
def editar_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        # Atualiza o registro existente
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Veículo {veiculo.placa} atualizado com sucesso!")
            return redirect('lista_veiculos')
    else:
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




#-------------------------------
#FUNCIONARIOS
#-------------------------------

# 1. Formulário do Funcionário (Excluindo apenas o campo 'usuario')
class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'funcao', 'cpf', 'cnh', 'data_nascimento', 'status', 'descricao']
        widgets = {
            # O segredo está em passar o 'format' para o widget do Django
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date'}, 
                format='%Y-%m-%d' # <-- Força o Django a renderizar como AAAA-MM-DD no HTML
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        # Garante que, ao editar (quando houver uma instância), o valor seja formatado corretamente
        if self.instance and self.instance.data_nascimento:
            self.initial['data_nascimento'] = self.instance.data_nascimento.strftime('%Y-%m-%d')

@login_required
def lista_funcionario(request):
    # Buscamos os funcionários do usuário logado
    funcionarios = Funcionario.objects.filter(usuario=request.user)
    
    # Filtramos na própria listagem usando o nome do status associado à ForeignKey
    funcionarios_contratados = funcionarios.filter(status__nome__iexact='contratado')
    funcionarios_neutros = funcionarios.filter(status__nome__iexact='neutro')
    
    # Caso existam funcionários sem status ou com outros status difetrentes de contratado/neutro
    outros_funcionarios = funcionarios.exclude(status__nome__iexact='contratado').exclude(status__nome__iexact='Neutro')

    return render(request, 'enterprise/funcionario/funcionario.html', {
        'contratados': funcionarios_contratados,
        'neutros': funcionarios_neutros,
        'outros': outros_funcionarios
    })

# 3. Adicionar Funcionário
@login_required
def add_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save(commit=False)
            funcionario.usuario = request.user
            funcionario.save()
            messages.success(request, f"Funcionário {funcionario.nome} adicionado com sucesso!")
            return redirect('lista_funcionario')
    else:
        form = FuncionarioForm()
        
    return render(request, 'enterprise/funcionario/add_funcionario.html', {'form': form})

# 4. Editar Funcionário
@login_required
def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cadastro de {funcionario.nome} atualizado com sucesso!")
            return redirect('lista_funcionario')
    else:
        form = FuncionarioForm(instance=funcionario)
        
    return render(request, 'enterprise/funcionario/editar_funcionario.html', {
        'form': form,
        'funcionario': funcionario
    })

# 5. Excluir Funcionário (Exclusão Física Real - ou mude para mudar status se preferir)
@login_required
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        nome = funcionario.nome
        funcionario.delete()
        messages.success(request, f"Funcionário {nome} foi removido definitivamente do sistema.")
        
    return redirect('lista_funcionario')



# ==========================================
# VIAGENS
# ==========================================

# 1. Formulário de Viagem com calendários 
class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = [
            'contratante', 'data_inicio', 'data_final', 'data_adiantamento', 
            'data_quitacao', 'local_inicio', 'local_final', 'km_rodados', 
            'status_da_viagem', 'carga', 'mic', 'motorista', 'veiculo_1', 
            'reboque', 'valor_proposto', 'valor_pago', 'media', 'descricao'
        ]
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_final': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_adiantamento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_quitacao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    # pegar informacoes por usuario
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ViagemForm, self).__init__(*args, **kwargs)


        if user:
            self.fields['motorista'].queryset = Funcionario.objects.filter(usuario=user)
            self.fields['veiculo_1'].queryset = Veiculo.objects.filter(usuario=user)
            self.fields['reboque'].queryset = Veiculo.objects.filter(usuario=user)


        for field_name in ['data_inicio', 'data_final', 'data_adiantamento', 'data_quitacao']:
            if self.instance and getattr(self.instance, field_name):
                self.initial[field_name] = getattr(self.instance, field_name).strftime('%Y-%m-%d')


# 2. View de Listagem de Viagens
@login_required
def lista_viagem(request):
    viagens = Viagem.objects.filter(usuario=request.user)
    
    # Operação ativa ou planejada
    viagens_ativas = viagens.filter(status_da_viagem__in=['planejada', 'em_andamento'])
    
    # Histórico de viagens (Concluídas, Quitadas e Canceladas)
    viagens_historico = viagens.filter(status_da_viagem__in=['concluida', 'quitada', 'cancelada'])

    return render(request, 'enterprise/viagem/viagem.html', {
        'ativas': viagens_ativas,
        'historico': viagens_historico
    })


# 3. Adicionar Viagem
@login_required
def add_viagem(request):
    if request.method == 'POST':
        # Passa o request.user para o formulário no POST
        form = ViagemForm(request.POST, user=request.user)
        if form.is_valid():
            viagem = form.save(commit=False)
            viagem.usuario = request.user
            viagem.save()
            messages.success(request, f"Viagem para {viagem.local_final} adicionada com sucesso!")
            return redirect('lista_viagem')
    else:
        # Passa o request.user para o formulário no GET
        form = ViagemForm(user=request.user)
        
    return render(request, 'enterprise/viagem/add_viagem.html', {'form': form})


# 4. editar viagem
@login_required
def edit_viagem(request, pk):
    viagem = get_object_or_404(Viagem, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        # Passa o request.user e a instância no POST
        form = ViagemForm(request.POST, instance=viagem, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Viagem #{viagem.id} atualizada com sucesso!")
            return redirect('lista_viagem')
    else:
        # Passa o request.user e a instância no GET
        form = ViagemForm(instance=viagem, user=request.user)
        
    return render(request, 'enterprise/viagem/edit_viagem.html', {
        'form': form, 
        'viagem': viagem
    })


# 5. View Excluir Viagem
@login_required
def excluir_viagem(request, pk):
    viagem = get_object_or_404(Viagem, id=pk, usuario=request.user)
    if request.method == 'POST':
        viagem.delete()
        messages.success(request, "Viagem removida do sistema.")
    return redirect('lista_viagem')