from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django import forms
from .models import Veiculo, Funcionario, StatusFuncionario, Viagem, Abastecida, Caixa 

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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


# ==========================================
# Sincronismo VIAGEM CAIXA

def sincronizar_recebimentos_viagem(viagem):
    veiculo_nome = str(viagem.veiculo_1)

    # 1. ADIANTAMENTO
    if viagem.data_adiantamento and viagem.valor_adiantamento and viagem.valor_adiantamento > 0:
        Caixa.objects.update_or_create(
            viagem=viagem,
            tipo='adiantamento',
            defaults={
                'usuario': viagem.usuario,
                'data': viagem.data_adiantamento,
                'valor_entrada': viagem.valor_adiantamento,
                'valor_saida': 0.00,
                'centro_de_custo': veiculo_nome,
                'descricao': f"Adiantamento de Frete - Viagem #{viagem.id} ({viagem.contratante} | {viagem.local_inicio} x {viagem.local_final})"
            }
        )
    else:
        Caixa.objects.filter(viagem=viagem, tipo='adiantamento').delete()

    # 2. QUITAÇÃO
    if viagem.data_quitacao and viagem.valor_quitacao and viagem.valor_quitacao > 0:
        Caixa.objects.update_or_create(
            viagem=viagem,
            tipo='quitacao',
            defaults={
                'usuario': viagem.usuario,
                'data': viagem.data_quitacao,
                'valor_entrada': viagem.valor_quitacao,
                'valor_saida': 0.00,
                'centro_de_custo': veiculo_nome,
                'descricao': f"Quitação Final de Frete - Viagem #{viagem.id} ({viagem.contratante} | {viagem.local_inicio} x {viagem.local_final})"
            }
        )
    else:
        Caixa.objects.filter(viagem=viagem, tipo='quitacao').delete()
        
#==========================================



# 1. Formulário de Viagem com calendários 
class ViagemForm(forms.ModelForm):
    # Tornando os campos de valor não obrigatórios no formulário HTML
    valor_adiantamento = forms.DecimalField(required=False, initial=0.00, decimal_places=2, max_digits=10, label="Valor do Adiantamento")
    valor_quitacao = forms.DecimalField(required=False, initial=0.00, decimal_places=2, max_digits=10, label="Valor da Quitação")

    class Meta:
        model = Viagem
        fields = [
            'contratante', 'data_inicio', 'data_final', 'data_adiantamento', 
            'data_quitacao', 'local_inicio', 'local_final', 'km_rodados', 
            'status_da_viagem', 'carga', 'mic', 'motorista', 'veiculo_1', 
            'reboque', 'valor_adiantamento', 'valor_quitacao', 'media', 'descricao'
        ]
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_final': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_adiantamento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_quitacao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

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
    
    # Operação ativa ou planejada (ordenada da mais recente para a mais antiga)
    viagens_ativas = viagens.filter(
        status_da_viagem__in=['planejada', 'em_andamento']
    ).order_by('-data_inicio')
    
    # Histórico de viagens ordenado pela data mais recente (-data_inicio)
    viagens_historico = viagens.filter(
        status_da_viagem__in=['concluida', 'quitada', 'cancelada']
    ).order_by('-data_inicio')

    return render(request, 'enterprise/viagem/viagem.html', {
        'ativas': viagens_ativas,
        'historico': viagens_historico
    })


# 3. Adicionar Viagem
@login_required
def add_viagem(request):
    if request.method == 'POST':
        form = ViagemForm(request.POST, user=request.user)
        if form.is_valid():
            # 1. Atribui o retorno com commit=False para injetar o usuário
            viagem_salva = form.save(commit=False)
            viagem_salva.usuario = request.user
            viagem_salva.save() # Salva no banco de dados

            # 2. Agora a variável 'viagem_salva' existe e pode ser usada aqui!
            sincronizar_recebimentos_viagem(viagem_salva)

            messages.success(request, f"Viagem para {viagem_salva.local_final} adicionada com sucesso!")
            return redirect('lista_viagem')
    else:
        form = ViagemForm(user=request.user)
        
    return render(request, 'enterprise/viagem/add_viagem.html', {'form': form})


# 4. editar viagem
@login_required
def edit_viagem(request, pk):
    viagem = get_object_or_404(Viagem, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = ViagemForm(request.POST, instance=viagem, user=request.user)
        if form.is_valid():
            # 1. Salva e atribui à variável 'viagem_salva'
            viagem_salva = form.save()

            # 2. Chama a função passando 'viagem_salva'
            sincronizar_recebimentos_viagem(viagem_salva)
            
            messages.success(request, f"Viagem #{viagem_salva.id} atualizada com sucesso!")
            return redirect('lista_viagem')
    else:
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



# ==========================================
# PERFIL DO USUÁRIO (USER)
# ==========================================

# 1. Formulário para editar os dados do usuário (Username, Nome, Sobrenome, Email)
class UserPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nome de Usuário (Login)',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }


# 2. View para visualizar o Perfil
@login_required
def perfil_user(request):
    # Resumo numérico para o painel do usuário
    total_veiculos = Veiculo.objects.filter(usuario=request.user).count()
    total_funcionarios = Funcionario.objects.filter(usuario=request.user).count()
    total_viagens_ativas = Viagem.objects.filter(
        usuario=request.user, 
        status_da_viagem__in=['planejada', 'em_andamento']
    ).count()

    return render(request, 'enterprise/user/perfil_user.html', {
        'total_veiculos': total_veiculos,
        'total_funcionarios': total_funcionarios,
        'total_viagens_ativas': total_viagens_ativas,
    })


# 3. View para Editar as Informações do Perfil
@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Seus dados de perfil foram atualizados com sucesso!")
            return redirect('perfil_user')
    else:
        form = UserPerfilForm(instance=request.user)

    return render(request, 'enterprise/user/edit_user.html', {'form': form})


# 4. View para Alterar a Senha do Usuário
@login_required
def alterar_senha_user(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Mantém a sessão do usuário ativa após trocar a senha
            update_session_auth_hash(request, user)
            messages.success(request, "Sua senha foi alterada com sucesso!")
            return redirect('perfil_user')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'enterprise/user/alterar_senha_user.html', {'form': form})



# ==========================================
# VIEWS: FLUXO DE CAIXA
# ==========================================


class DespesaCaixaForm(forms.ModelForm):
    centro_de_custo = forms.ModelChoiceField(
        queryset=Veiculo.objects.none(),
        label="Veículo / Centro de Custo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Caixa
        fields = ['data', 'centro_de_custo', 'valor_saida', 'descricao']
        labels = {
            'valor_saida': 'Valor da Despesa (R$)',
            'descricao': 'Descrição / Motivo da Despesa',
        }
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'valor_saida': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex: Compra de Pneu, Combustível, Manutenção...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['centro_de_custo'].queryset = Veiculo.objects.filter(usuario=user)
        if self.instance and self.instance.data:
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%d')


class EntradaCaixaForm(forms.ModelForm):
    centro_de_custo = forms.ModelChoiceField(
        queryset=Veiculo.objects.none(),
        label="Veículo / Centro de Custo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Caixa
        fields = ['data', 'centro_de_custo', 'valor_entrada', 'descricao']
        labels = {
            'valor_entrada': 'Valor da Entrada (R$)',
            'descricao': 'Descrição da Receita / Origem do Recurso',
        }
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'valor_entrada': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex: Aporte financeiro, Reembolso, Venda de Peça...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['centro_de_custo'].queryset = Veiculo.objects.filter(usuario=user)
        if self.instance and self.instance.data:
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%d')









@login_required
def lista_caixa(request):
    gastos = Caixa.objects.filter(usuario=request.user).order_by('-data')
    veiculos_usuario = Veiculo.objects.filter(usuario=request.user)

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    veiculo_id = request.GET.get('veiculo')

    if data_inicio:
        gastos = gastos.filter(data__gte=data_inicio)
    if data_fim:
        gastos = gastos.filter(data__lte=data_fim)
    if veiculo_id:
        veiculo_obj = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
        gastos = gastos.filter(centro_de_custo=str(veiculo_obj))

    total_entradas = sum(g.valor_entrada for g in gastos)
    total_saidas = sum(g.valor_saida for g in gastos)
    saldo_conta = total_entradas - total_saidas

    return render(request, 'enterprise/caixa/caixa.html', {
        'gastos': gastos,
        'veiculos_usuario': veiculos_usuario,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_conta': saldo_conta,
        'data_inicio': data_inicio or '',
        'data_fim': data_fim or '',
        'veiculo_selecionado': int(veiculo_id) if veiculo_id else '',
    })


@login_required
def despesa_caixa(request):
    if request.method == 'POST':
        form = DespesaCaixaForm(request.POST, user=request.user)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.tipo = 'despesa'
            despesa.valor_entrada = 0.00
            despesa.save()
            messages.success(request, f"Despesa de R$ {despesa.valor_saida} cadastrada com sucesso!")
            return redirect('lista_caixa')
    else:
        form = DespesaCaixaForm(user=request.user)

    return render(request, 'enterprise/caixa/despesa_caixa.html', {'form': form})


@login_required
def entrada_caixa(request):
    if request.method == 'POST':
        form = EntradaCaixaForm(request.POST, user=request.user)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.usuario = request.user
            entrada.tipo = 'receita_extra'
            entrada.valor_saida = 0.00
            entrada.save()
            messages.success(request, f"Entrada Externa de R$ {entrada.valor_entrada} adicionada com sucesso (+)! ")
            return redirect('lista_caixa')
    else:
        form = EntradaCaixaForm(user=request.user)

    return render(request, 'enterprise/caixa/entrada_caixa.html', {'form': form})


@login_required
def edit_caixa(request, pk):
    caixa = get_object_or_404(Caixa, id=pk, usuario=request.user)

    if caixa.tipo == 'despesa':
        if request.method == 'POST':
            form = DespesaCaixaForm(request.POST, instance=caixa, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Despesa atualizada com sucesso!")
                return redirect('lista_caixa')
        else:
            form = DespesaCaixaForm(instance=caixa, user=request.user)
        return render(request, 'enterprise/caixa/despesa_caixa.html', {'form': form, 'editando': True})
    else:
        if request.method == 'POST':
            form = EntradaCaixaForm(request.POST, instance=caixa, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Entrada financeira atualizada com sucesso!")
                return redirect('lista_caixa')
        else:
            form = EntradaCaixaForm(instance=caixa, user=request.user)
        return render(request, 'enterprise/caixa/entrada_caixa.html', {'form': form, 'editando': True})


@login_required
def excluir_caixa(request, pk):
    caixa = get_object_or_404(Caixa, id=pk, usuario=request.user)
    if request.method == 'POST':
        caixa.delete()
        messages.success(request, "Lançamento removido do Caixa com sucesso.")
    return redirect('lista_caixa')



