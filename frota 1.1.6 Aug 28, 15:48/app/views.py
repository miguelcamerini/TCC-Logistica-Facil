from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, ProtectedError

from .models import Veiculo, Funcionario, StatusFuncionario, Viagem, Abastecida, Caixa 


from django.db.models import Avg


from django.db.models import Sum
from .models import Abastecida, Viagem, Caixa, Veiculo, Funcionario



# -------------------------------
# AUTENTICAÇÃO E NAVEGAÇÃO BÁSICA
# -------------------------------

def index(request):
    return HttpResponse("Olá, mundo! Você está no index do app.")

def nao_autorizado_view(request):
    return render(request, 'nao_autorizado.html')

def login_view(request):
    if request.method == 'POST':
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça o login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastro.html', {'form': form})







# ==========================================
# BLOQUEIO DE EXCLUSÃO (VEÍCULO E FUNCIONÁRIO)
# ==========================================

@login_required
def excluir_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, id=pk, usuario=request.user)
    if request.method == 'POST':
        # Usa Q(...) diretamente para buscar o veículo como principal ou reboque
        viagens_vinculadas = Viagem.objects.filter(Q(veiculo_1=veiculo) | Q(reboque=veiculo)).exists()
        
        if viagens_vinculadas:
            messages.error(
                request, 
                f"O veículo '{veiculo.nome_fantasia} ({veiculo.placa})' não pode ser excluído pois possui viagens vinculadas!"
            )
            return redirect('lista_veiculos')
        
        try:
            placa = veiculo.placa
            veiculo.delete()
            messages.success(request, f"Veículo com placa {placa} foi excluído com sucesso.")
        except ProtectedError:
            messages.error(request, "Não é possível excluir este veículo pois ele está em uso no sistema.")

    return redirect('lista_veiculos')


@login_required
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, id=pk, usuario=request.user)
    if request.method == 'POST':
        # Verifica se o motorista está vinculado a alguma viagem
        if Viagem.objects.filter(motorista=funcionario).exists():
            messages.error(
                request, 
                f"O funcionário '{funcionario.nome}' não pode ser excluído pois possui viagens vinculadas como motorista!"
            )
            return redirect('lista_funcionario')

        try:
            nome = funcionario.nome
            funcionario.delete()
            messages.success(request, f"Funcionário {nome} foi removido definitivamente do sistema.")
        except ProtectedError:
            messages.error(request, "Não é possível excluir este funcionário pois ele está em uso no sistema.")
            
            
            
# -------------------------------
# VEÍCULOS
# -------------------------------

@login_required
def lista_veiculos(request):
    veiculos = Veiculo.objects.filter(usuario=request.user)
    
    # 1. Veículos Operacionais (Disponíveis ou Em Viagem)
    veiculos_operacionais = veiculos.filter(status__in=['disponivel', 'em_viagem']).order_by('nome_fantasia')
    
    # 2. Veículos Em Manutenção
    veiculos_manutencao = veiculos.filter(status='manutencao').order_by('nome_fantasia')
    
    # 3. Veículos Inativos / Vendidos
    veiculos_inativos = veiculos.filter(status='vendido').order_by('nome_fantasia')

    return render(request, 'enterprise/veiculo/veiculo.html', {
        'operacionais': veiculos_operacionais,
        'manutencao': veiculos_manutencao,
        'inativos': veiculos_inativos
    })


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = [
            'nome_fantasia', 'placa', 'chassi', 'renavam', 
            'ano_fabricacao', 'ano_modelo', 'status', 'descricao'
        ]


@login_required
def add_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.usuario = request.user 
            veiculo.save()
            messages.success(request, "Veículo cadastrado com sucesso!")
            return redirect('lista_veiculos') 
    else:
        form = VeiculoForm()
        
    return render(request, 'enterprise/veiculo/add_veiculo.html', {'form': form})


@login_required
def editar_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Veículo {veiculo.placa} atualizado com sucesso!")
            return redirect('lista_veiculos')
    else:
        form = VeiculoForm(instance=veiculo)
        
    return render(request, 'enterprise/veiculo/editar_veiculo.html', {
        'form': form, 
        'veiculo': veiculo
    })


@login_required
def excluir_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, id=pk, usuario=request.user)
    
    if request.method == 'POST':
        if Viagem.objects.filter(Q(veiculo_1=veiculo) | Q(reboque=veiculo)).exists():
            messages.error(
                request, 
                f"O veículo '{veiculo.nome_fantasia} ({veiculo.placa})' não pode ser excluído pois possui viagens vinculadas!"
            )
            return redirect('lista_veiculos')

        try:
            placa = veiculo.placa
            veiculo.delete()
            messages.success(request, f"Veículo com placa {placa} foi excluído com sucesso.")
        except ProtectedError:
            messages.error(request, "Não é possível excluir este veículo pois possui registros vinculados no sistema.")
    
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
    funcionarios_contratados = funcionarios.filter(status__nome__iexact='contratado').order_by('nome')
    funcionarios_neutros = funcionarios.filter(status__nome__iexact='neutro').order_by('nome')
    
    # Caso existam funcionários sem status ou com outros status diferentes de contratado e neutro
    outros_funcionarios = funcionarios.exclude(status__nome__iexact='contratado').exclude(status__nome__iexact='neutro').order_by('nome')

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
                'nota_fiscal': viagem.nota_fiscal if hasattr(viagem, 'nota_fiscal') else '', # Copia a NF da Viagem para o Caixa
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
                'nota_fiscal': viagem.nota_fiscal if hasattr(viagem, 'nota_fiscal') else '', # Copia a NF da Viagem para o Caixa
                'descricao': f"Quitação Final de Frete - Viagem #{viagem.id} ({viagem.contratante} | {viagem.local_inicio} x {viagem.local_final})"
            }
        )
    else:
        Caixa.objects.filter(viagem=viagem, tipo='quitacao').delete()


# 1. Formulário de Viagem com Nota Fiscal inclusa
# ==========================================
# 1. FORMULÁRIO DE VIAGEM (REORGANIZADO)
# ==========================================
class ViagemForm(forms.ModelForm):
    nota_fiscal = forms.CharField(
        required=False, 
        max_length=50, 
        label="Nº Nota Fiscal",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: NF-1025'})
    )
    valor_adiantamento = forms.DecimalField(
        required=False, 
        initial=0.00, 
        decimal_places=2, 
        max_digits=10, 
        label="Valor Adiantamento (R$)"
    )
    valor_quitacao = forms.DecimalField(
        required=False, 
        initial=0.00, 
        decimal_places=2, 
        max_digits=10, 
        label="Valor Quitação (R$)"
    )

    class Meta:
        model = Viagem
        # Campos reordenados por fluxo lógico de trabalho
        fields = [
            # 1. Dados Básicos e Status
            'contratante', 'status_da_viagem', 'carga', 'mic', 'nota_fiscal',
            # 2. Rotas e Quilometragem
            'local_inicio', 'local_final', 'km_rodados',
            # 3. Equipe e Veículos
            'motorista', 'veiculo_1', 'reboque',
            # 4. Cronograma de Datas
            'data_inicio', 'data_final', 'data_adiantamento', 'data_quitacao',
            # 5. Financeiro e Média
            'valor_adiantamento', 'valor_quitacao', 'media',
            # 6. Observações
            'descricao'
        ]
        labels = {
            'contratante': 'Empresa Contratante',
            'status_da_viagem': 'Status da Viagem',
            'carga': 'Tipo de Carga / Mercadoria',
            'mic': 'Nº MIC / DTA',
            'local_inicio': 'Origem (Cidade/UF)',
            'local_final': 'Destino (Cidade/UF)',
            'km_rodados': 'Km Percorridos',
            'motorista': 'Motorista Responsável',
            'veiculo_1': 'Veículo / Trator',
            'reboque': 'Reboque / Carreta (Opcional)',
            'data_inicio': 'Data de Partida',
            'data_final': 'Data de Chegada',
            'data_adiantamento': 'Data de Recebimento do Adiantamento',
            'data_quitacao': 'Data da Quitação do Frete',
            'media': 'Média de Consumo (Km/L)',
            'descricao': 'Observações Adicionais',
        }
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_final': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_adiantamento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_quitacao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Detalhes do frete, observações ou ocorrências...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ViagemForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['motorista'].queryset = Funcionario.objects.filter(usuario=user)
            self.fields['veiculo_1'].queryset = Veiculo.objects.filter(usuario=user)
            self.fields['reboque'].queryset = Veiculo.objects.filter(usuario=user)

        # O campo de média é preenchido via cálculo de abastecimento, ficando somente leitura
        self.fields['media'].widget.attrs['readonly'] = True
        self.fields['media'].widget.attrs['placeholder'] = 'Calculado automaticamente via Abastecimento'

        for field_name in ['data_inicio', 'data_final', 'data_adiantamento', 'data_quitacao']:
            if self.instance and getattr(self.instance, field_name):
                self.initial[field_name] = getattr(self.instance, field_name).strftime('%Y-%m-%d')
                
                
                
                
                
                
                

# 2. View de Listagem de Viagens (Com Filtros e Média Geral)
@login_required
def lista_viagem(request):
    viagens = Viagem.objects.filter(usuario=request.user)
    motoristas_usuario = Funcionario.objects.filter(usuario=request.user)

    # Obter parâmetros GET de filtro
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    motorista_id = request.GET.get('motorista')

    # Aplicação dos filtros
    if data_inicio:
        viagens = viagens.filter(data_inicio__gte=data_inicio)
    if data_fim:
        viagens = viagens.filter(data_inicio__lte=data_fim)
    if motorista_id:
        viagens = viagens.filter(motorista_id=motorista_id)

    # Cálculo da Média Geral das viagens filtradas (desconsiderando médias zeradas ou None)
    media_geral = viagens.filter(media__gt=0).aggregate(Avg('media'))['media__avg'] or 0.0

    # Separação das listas ativas e histórico a partir do conjunto filtrado
    viagens_ativas = viagens.filter(
        status_da_viagem__in=['planejada', 'em_andamento']
    ).order_by('-data_inicio')

    viagens_historico = viagens.filter(
        status_da_viagem__in=['concluida', 'quitada', 'cancelada']
    ).order_by('-data_inicio')

    return render(request, 'enterprise/viagem/viagem.html', {
        'ativas': viagens_ativas,
        'historico': viagens_historico,
        'motoristas_usuario': motoristas_usuario,
        'media_geral': round(media_geral, 2),
        'data_inicio': data_inicio or '',
        'data_fim': data_fim or '',
        'motorista_selecionado': int(motorista_id) if motorista_id else '',
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
    
    # Soma total dos litros abastecidos para esta viagem específica
    total_litros = Abastecida.objects.filter(viagem=viagem).aggregate(Sum('litros'))['litros__sum'] or 0.00
    
    if request.method == 'POST':
        form = ViagemForm(request.POST, instance=viagem, user=request.user)
        if form.is_valid():
            viagem_salva = form.save(commit=False)

            # Recalcula a média (KM / Total de Litros)
            if total_litros > 0 and viagem_salva.km_rodados and viagem_salva.km_rodados > 0:
                viagem_salva.media = round(float(viagem_salva.km_rodados) / float(total_litros), 2)
            else:
                viagem_salva.media = 0.00

            viagem_salva.save()
            sincronizar_recebimentos_viagem(viagem_salva)
            
            messages.success(request, f"Viagem #{viagem_salva.id} atualizada com sucesso!")
            return redirect('lista_viagem')
    else:
        form = ViagemForm(instance=viagem, user=request.user)
        
    return render(request, 'enterprise/viagem/edit_viagem.html', {
        'form': form, 
        'viagem': viagem,
        'total_litros': round(total_litros, 2)  # <-- PASSA O TOTAL DE LITROS PARA A TELA
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












# ==========================================
# BLOQUEIO DE EXCLUSÃO (VEÍCULO E FUNCIONÁRIO)
# ==========================================

@login_required
def excluir_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, id=pk, usuario=request.user)
    if request.method == 'POST':
        # Usa Q(...) diretamente para buscar o veículo como principal ou reboque
        viagens_vinculadas = Viagem.objects.filter(Q(veiculo_1=veiculo) | Q(reboque=veiculo)).exists()
        
        if viagens_vinculadas:
            messages.error(
                request, 
                f"O veículo '{veiculo.nome_fantasia} ({veiculo.placa})' não pode ser excluído pois possui viagens vinculadas!"
            )
            return redirect('lista_veiculos')
        
        try:
            placa = veiculo.placa
            veiculo.delete()
            messages.success(request, f"Veículo com placa {placa} foi excluído com sucesso.")
        except ProtectedError:
            messages.error(request, "Não é possível excluir este veículo pois ele está em uso no sistema.")

    return redirect('lista_veiculos')


@login_required
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, id=pk, usuario=request.user)
    if request.method == 'POST':
        # Verifica se o motorista está vinculado a alguma viagem
        if Viagem.objects.filter(motorista=funcionario).exists():
            messages.error(
                request, 
                f"O funcionário '{funcionario.nome}' não pode ser excluído pois possui viagens vinculadas como motorista!"
            )
            return redirect('lista_funcionario')

        try:
            nome = funcionario.nome
            funcionario.delete()
            messages.success(request, f"Funcionário {nome} foi removido definitivamente do sistema.")
        except ProtectedError:
            messages.error(request, "Não é possível excluir este funcionário pois possui registros vinculados.")

    return redirect('lista_funcionario')









# ==========================================
# SINCRONIZAÇÃO BIDIRECIONAL (VIAGEM <-> CAIXA)
# ==========================================

def sincronizar_recebimentos_viagem(viagem):
    """Sincroniza os recebimentos da Viagem para o Caixa."""
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
                'valor_saida': Decimal('0.00'),
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
                'valor_saida': Decimal('0.00'),
                'centro_de_custo': veiculo_nome,
                'descricao': f"Quitação Final de Frete - Viagem #{viagem.id} ({viagem.contratante} | {viagem.local_inicio} x {viagem.local_final})"
            }
        )
    else:
        Caixa.objects.filter(viagem=viagem, tipo='quitacao').delete()


def sincronizar_caixa_para_viagem(caixa):
    """Sincroniza edições feitas no Caixa de volta para a Viagem correspondente."""
    if not caixa.viagem:
        return

    viagem = caixa.viagem
    
    if caixa.tipo == 'adiantamento':
        if caixa.valor_entrada and caixa.valor_entrada > 0:
            viagem.valor_adiantamento = caixa.valor_entrada
            viagem.data_adiantamento = caixa.data
        else:
            viagem.valor_adiantamento = Decimal('0.00')
            viagem.data_adiantamento = None
            
    elif caixa.tipo == 'quitacao':
        if caixa.valor_entrada and caixa.valor_entrada > 0:
            viagem.valor_quitacao = caixa.valor_entrada
            viagem.data_quitacao = caixa.data
        else:
            viagem.valor_quitacao = Decimal('0.00')
            viagem.data_quitacao = None

    viagem.save()


# ==========================================
# VIEWS DO CAIXA COM SINCRONISMO E AVISOS
# ==========================================

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
        # Se for adiantamento, quitação ou receita extra
        if request.method == 'POST':
            form = EntradaCaixaForm(request.POST, instance=caixa, user=request.user)
            if form.is_valid():
                caixa_salvo = form.save()
                
                # Sincroniza a alteração de volta na Viagem se for lançamento de viagem
                if caixa_salvo.viagem:
                    sincronizar_caixa_para_viagem(caixa_salvo)
                    messages.info(request, f"O valor foi atualizado no Caixa e na Viagem #{caixa_salvo.viagem.id}!")
                else:
                    messages.success(request, "Entrada financeira atualizada com sucesso!")
                    
                return redirect('lista_caixa')
        else:
            form = EntradaCaixaForm(instance=caixa, user=request.user)
        return render(request, 'enterprise/caixa/entrada_caixa.html', {'form': form, 'editando': True})


@login_required
def excluir_caixa(request, pk):
    caixa = get_object_or_404(Caixa, id=pk, usuario=request.user)
    if request.method == 'POST':
        viagem_vinculada = caixa.viagem
        tipo_lancamento = caixa.get_tipo_display()

        if viagem_vinculada:
            # Ao apagar o caixa de uma viagem, zera o valor e a data na viagem correspondente
            if caixa.tipo == 'adiantamento':
                viagem_vinculada.valor_adiantamento = Decimal('0.00')
                viagem_vinculada.data_adiantamento = None
            elif caixa.tipo == 'quitacao':
                viagem_vinculada.valor_quitacao = Decimal('0.00')
                viagem_vinculada.data_quitacao = None
            
            viagem_vinculada.save()
            caixa.delete()
            messages.warning(
                request, 
                f"O lançamento de {tipo_lancamento} foi removido do Caixa e os valores foram limpados da Viagem #{viagem_vinculada.id}!"
            )
        else:
            caixa.delete()
            messages.success(request, "Lançamento removido do Caixa com sucesso.")

    return redirect('lista_caixa')


# ==========================================
# EXCLUSÃO DE VIAGEM COM AVISO DE CAIXA
# ==========================================

@login_required
def excluir_viagem(request, pk):
    viagem = get_object_or_404(Viagem, id=pk, usuario=request.user)
    if request.method == 'POST':
        id_viagem = viagem.id
        
        # Apaga os lançamentos do Caixa gerados por esta viagem
        lancamentos_caixa = Caixa.objects.filter(viagem=viagem)
        qtd_caixa = lancamentos_caixa.count()
        lancamentos_caixa.delete()
        
        viagem.delete()
        
        if qtd_caixa > 0:
            messages.warning(
                request, 
                f"A Viagem #{id_viagem} foi excluída e seus {qtd_caixa} lançamento(s) de frete vinculados no Caixa também foram removidos!"
            )
        else:
            messages.success(request, f"Viagem #{id_viagem} removida do sistema.")
            
    return redirect('lista_viagem')

















# ===================================
# PAINEL HOME
# ===================================

@login_required
def home(request):
    # 1. Viagens em andamento (3 últimas)
    viagens_qs = Viagem.objects.filter(
        usuario=request.user, 
        status_da_viagem='em_andamento'
    ).order_by('-data_inicio')
    
    viagens_andamento = viagens_qs[:3]
    tem_mais_viagens = viagens_qs.count() > 3

    # 2. Dados do Caixa
    caixa_qs = Caixa.objects.filter(usuario=request.user)
    ultima_movimentacao = caixa_qs.order_by('-data').first()
    
    total_entradas = sum(c.valor_entrada or 0 for c in caixa_qs)
    total_saidas = sum(c.valor_saida or 0 for c in caixa_qs)
    saldo_caixa = total_entradas - total_saidas

    # 3. Funcionários contratados/ativos (3 últimos)
    func_qs = Funcionario.objects.filter(usuario=request.user).order_by('-id')
    funcionarios_ativos = func_qs[:3]
    tem_mais_funcionarios = func_qs.count() > 3

    # 4. Veículos operacionais (3 últimos)
    veic_qs = Veiculo.objects.filter(usuario=request.user).order_by('-id')
    veiculos_ativos = veic_qs[:3]
    tem_mais_veiculos = veic_qs.count() > 3

    return render(request, 'home.html', {
        'viagens_andamento': viagens_andamento,
        'tem_mais_viagens': tem_mais_viagens,
        'ultima_data_caixa': ultima_movimentacao.data if ultima_movimentacao else None,
        'saldo_caixa': saldo_caixa,
        'funcionarios_ativos': funcionarios_ativos,
        'tem_mais_funcionarios': tem_mais_funcionarios,
        'veiculos_ativos': veiculos_ativos,
        'tem_mais_veiculos': tem_mais_veiculos,
    })
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# ==========================================
# 1. FORMULÁRIO DE ABASTECIMENTO DE VIAGEM
# ==========================================
class AbastecidaViagemForm(forms.ModelForm):
    nota_fiscal = forms.CharField(
        required=False,
        max_length=50,
        label="Nota Fiscal",
        widget=forms.TextInput(attrs={'placeholder': 'Nº da Nota Fiscal (opcional)'})
    )

    class Meta:
        model = Abastecida
        fields = ['viagem', 'data_abastecida', 'valor_abastecida', 'litros', 'nota_fiscal', 'descricao']
        labels = {
            'viagem': 'Selecione a Viagem Ativa',
            'data_abastecida': 'Data do Abastecimento',
            'valor_abastecida': 'Valor Total (R$)',
            'litros': 'Litros Abastecidos (L)',
            'descricao': 'Posto / Observações',
        }
        widgets = {
            'data_abastecida': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'valor_abastecida': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'litros': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex: Posto Shell BR 116...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Mostra apenas viagens ativas do usuário
            self.fields['viagem'].queryset = Viagem.objects.filter(
                usuario=user,
                status_da_viagem__in=['planejada', 'em_andamento']
            )
            self.fields['viagem'].required = True


# ==========================================
# 2. FORMULÁRIO DE ABASTECIMENTO COMUM (FORA DE VIAGEM)
# ==========================================
class AbastecidaComumForm(forms.ModelForm):
    nota_fiscal = forms.CharField(
        required=False,
        max_length=50,
        label="Nota Fiscal",
        widget=forms.TextInput(attrs={'placeholder': 'Nº da Nota Fiscal (opcional)'})
    )

    class Meta:
        model = Abastecida
        fields = ['data_abastecida', 'veiculo', 'motorista_responsavel', 'viagem', 'valor_abastecida', 'litros', 'nota_fiscal', 'descricao']
        labels = {
            'data_abastecida': 'Data do Abastecimento',
            'veiculo': 'Veículo',
            'motorista_responsavel': 'Motorista Responsável',
            'viagem': 'Viagem Associada (Opcional)',
            'valor_abastecida': 'Valor Total (R$)',
            'litros': 'Litros Abastecidos (L)',
            'descricao': 'Posto / Observações',
        }
        widgets = {
            'data_abastecida': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'valor_abastecida': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'litros': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex: Abastecimento de Pátio / Manobra...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['veiculo'].queryset = Veiculo.objects.filter(usuario=user)
            self.fields['motorista_responsavel'].queryset = Funcionario.objects.filter(usuario=user)
            self.fields['viagem'].queryset = Viagem.objects.filter(usuario=user)
            
            
            
            
# ==========================================
# HELPER DE SINCRONISMO
# ==========================================
def sincronizar_abastecimento(abastecimento, nota_fiscal="", viagem_antiga=None):
    """
    1. Soma todos os litros vinculados à viagem.
    2. Divide os KM rodados da Viagem pelo total de litros acumulados.
    3. Salva o resultado no campo viagem.media.
    4. Atualiza/Cria a despesa correspondente no Caixa.
    """
    # Helper para calcular e atualizar a média de uma viagem específica
    def recalcular_media_viagem(viagem_obj):
        if not viagem_obj:
            return

        total_litros = Abastecida.objects.filter(viagem=viagem_obj).aggregate(Sum('litros'))['litros__sum'] or 0.00
        
        # Só calcula a média se houver litros acumulados e KM informado
        if total_litros > 0 and viagem_obj.km_rodados and viagem_obj.km_rodados > 0:
            viagem_obj.media = round(float(viagem_obj.km_rodados) / float(total_litros), 2)
        else:
            viagem_obj.media = 0.00
            
        viagem_obj.save()

    # 1. ATUALIZA A VIAGEM ATUAL
    if abastecimento.viagem:
        # Garante vínculo de veículo e motorista da viagem se não informados
        if not abastecimento.veiculo:
            abastecimento.veiculo = abastecimento.viagem.veiculo_1
        if not abastecimento.motorista_responsavel:
            abastecimento.motorista_responsavel = abastecimento.viagem.motorista
        abastecimento.save()

        recalcular_media_viagem(abastecimento.viagem)

    # RECALCULA A VIAGEM ANTIGA (caso tenha mudado de viagem durante a edição)
    if viagem_antiga and viagem_antiga != abastecimento.viagem:
        recalcular_media_viagem(viagem_antiga)

    # 2. LANÇA OU ATUALIZA NO CAIXA
    veiculo_nome = str(abastecimento.veiculo) if abastecimento.veiculo else "FROTA"
    tag_busca = f"Abastecimento #{abastecimento.id}"

    caixa_item = Caixa.objects.filter(usuario=abastecimento.usuario, descricao__icontains=tag_busca).first()
    if not caixa_item:
        caixa_item = Caixa(usuario=abastecimento.usuario, tipo='despesa')

    caixa_item.data = abastecimento.data_abastecida
    caixa_item.valor_saida = abastecimento.valor_abastecida
    caixa_item.valor_entrada = 0.00
    caixa_item.centro_de_custo = veiculo_nome
    caixa_item.nota_fiscal = nota_fiscal
    caixa_item.descricao = f"{tag_busca} - {abastecimento.litros}L ({veiculo_nome})"
    caixa_item.save()


# ==========================================
# VIEWS
# ==========================================

# 1. Abastecimento de Viagem
@login_required
def add_abastecida_viagem(request):
    if request.method == 'POST':
        form = AbastecidaViagemForm(request.POST, user=request.user)
        if form.is_valid():
            abastecimento = form.save(commit=False)
            abastecimento.usuario = request.user
            # Vincula motorista e veículo automaticamente a partir da viagem escolhida
            abastecimento.veiculo = abastecimento.viagem.veiculo_1
            abastecimento.motorista_responsavel = abastecimento.viagem.motorista
            abastecimento.save()

            nota_fiscal = form.cleaned_data.get('nota_fiscal', '')
            sincronizar_abastecimento(abastecimento, nota_fiscal)

            messages.success(request, f"Abastecimento de {abastecimento.litros}L lançado na Viagem #{abastecimento.viagem.id} e debitado no Caixa!")
            return redirect('lista_abastecida')
    else:
        form = AbastecidaViagemForm(user=request.user)

    return render(request, 'enterprise/abastecida/add_abastecida_viagem.html', {'form': form})


# 2. Abastecimento Comum (Fora de Viagem)
@login_required
def add_abastecida(request):
    if request.method == 'POST':
        form = AbastecidaComumForm(request.POST, user=request.user)
        if form.is_valid():
            abastecimento = form.save(commit=False)
            abastecimento.usuario = request.user
            abastecimento.save()

            nota_fiscal = form.cleaned_data.get('nota_fiscal', '')
            sincronizar_abastecimento(abastecimento, nota_fiscal)

            messages.success(request, f"Abastecimento comum de {abastecimento.litros}L cadastrado no Caixa com sucesso!")
            return redirect('lista_abastecida')
    else:
        form = AbastecidaComumForm(user=request.user)

    return render(request, 'enterprise/abastecida/add_abastecida.html', {'form': form})

# ==========================================
# VIEWS DE ABASTECIDA
# ==========================================
@login_required
def lista_abastecida(request):
    abastecimentos = Abastecida.objects.filter(usuario=request.user).order_by('-data_abastecida')
    veiculos_usuario = Veiculo.objects.filter(usuario=request.user)

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    veiculo_id = request.GET.get('veiculo')

    if data_inicio:
        abastecimentos = abastecimentos.filter(data_abastecida__gte=data_inicio)
    if data_fim:
        abastecimentos = abastecimentos.filter(data_abastecida__lte=data_fim)
    if veiculo_id:
        abastecimentos = abastecimentos.filter(veiculo_id=veiculo_id)

    total_litros = sum(a.litros for a in abastecimentos)
    total_valor = sum(a.valor_abastecida for a in abastecimentos)

    return render(request, 'enterprise/abastecida/abastecida.html', {
        'abastecimentos': abastecimentos,
        'veiculos_usuario': veiculos_usuario,
        'total_litros': round(total_litros, 2),
        'total_valor': round(total_valor, 2),
        'data_inicio': data_inicio or '',
        'data_fim': data_fim or '',
        'veiculo_selecionado': int(veiculo_id) if veiculo_id else '',
    })





# ==========================================
# VIEWS: EDIÇÃO E ABASTECIMENTO COMUM
# ==========================================



# 2. View Única de Edição (Detecta automaticamente o tipo de Abastecimento)
@login_required
def edit_abastecida(request, pk):
    abastecimento = get_object_or_404(Abastecida, id=pk, usuario=request.user)
    viagem_antiga = abastecimento.viagem  # Guarda a viagem anterior para recalcular se for trocada

    if request.method == 'POST':
        # Se tinha viagem vinculada, usa o formulário focado em viagem, senão o formulário comum
        if abastecimento.viagem:
            form = AbastecidaViagemForm(request.POST, instance=abastecimento, user=request.user)
        else:
            form = AbastecidaComumForm(request.POST, instance=abastecimento, user=request.user)

        if form.is_valid():
            abastecimento_salvo = form.save(commit=False)
            
            # Se for vinculado à viagem, garante que veículo e motorista venham da viagem
            if abastecimento_salvo.viagem:
                abastecimento_salvo.veiculo = abastecimento_salvo.viagem.veiculo_1
                abastecimento_salvo.motorista_responsavel = abastecimento_salvo.viagem.motorista
                
            abastecimento_salvo.save()

            nota_fiscal = form.cleaned_data.get('nota_fiscal', '')
            sincronizar_abastecimento(abastecimento_salvo, nota_fiscal, viagem_antiga=viagem_antiga)

            messages.success(request, "Abastecimento atualizado com sucesso!")
            return redirect('lista_abastecida')
    else:
        if abastecimento.viagem:
            form = AbastecidaViagemForm(instance=abastecimento, user=request.user)
        else:
            form = AbastecidaComumForm(instance=abastecimento, user=request.user)

    return render(request, 'enterprise/abastecida/edit_abastecida.html', {
        'form': form, 
        'abastecimento': abastecimento
    })


@login_required
def excluir_abastecida(request, pk):
    abastecimento = get_object_or_404(Abastecida, id=pk, usuario=request.user)
    if request.method == 'POST':
        viagem = abastecimento.viagem
        
        # Remove do Caixa
        Caixa.objects.filter(usuario=request.user, descricao__icontains=f"Abastecimento #{abastecimento.id}").delete()
        
        abastecimento.delete()

        # Recalcula a Média (Km / Litros restantes)
        if viagem:
            total_litros = Abastecida.objects.filter(viagem=viagem).aggregate(Sum('litros'))['litros__sum'] or 0.00
            if total_litros > 0 and viagem.km_rodados and viagem.km_rodados > 0:
                viagem.media = round(float(viagem.km_rodados) / float(total_litros), 2)
            else:
                viagem.media = 0.00
            viagem.save()

        messages.success(request, "Abastecimento removido e média da viagem atualizada.")
    return redirect('lista_abastecida')




































































# 1. Formulário para confirmar senha na exclusão
class ConfirmarSenhaExclusaoForm(forms.Form):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha atual'}),
        label="Senha Atual",
        required=True
    )

# 2. View para excluir a conta do usuário
@login_required
def excluir_conta_user(request):
    if request.method == 'POST':
        form = ConfirmarSenhaExclusaoForm(request.POST)
        if form.is_valid():
            senha = form.cleaned_data.get('senha')
            user = request.user
            
            # Autentica se a senha fornecida confere com a do usuário logado
            if authenticate(username=user.username, password=senha):
                # O cascade do Django excluirá todas as Viagens, Caixas e Abastecidas vinculadas ao usuário
                user.delete()
                logout(request)
                messages.success(request, "Sua conta e todos os dados vinculados foram excluídos com sucesso.")
                return redirect('login')
            else:
                form.add_error('senha', 'Senha incorreta. A conta não foi excluída.')
    else:
        form = ConfirmarSenhaExclusaoForm()

    return render(request, 'enterprise/user/excluir_conta_user.html', {'form': form})