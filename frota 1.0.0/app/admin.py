from django.contrib import admin

# Register your models here.
from .models import Veiculo, Funcionario, Viagem, Abastecida, Caixa

# ==========================================
# CONFIGURAÇÃO: VEICULO
# ==========================================
@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    # Colunas que vão aparecer na listagem
    list_display = ('id', 'nome_fantasia', 'placa', 'renavam', 'ano_modelo', 'status', 'usuario')
    # Filtros laterais
    list_filter = ('status', 'ano_fabricacao', 'ano_modelo', 'usuario')
    # Campos de busca (o 'username' busca pelo login do usuário vinculado)
    search_fields = ('nome_fantasia', 'placa', 'chassi', 'renavam', 'usuario__username')
    # Organização dos campos ao editar/criar
    list_per_page = 20


# ==========================================
# CONFIGURAÇÃO: FUNCIONARIO
# ==========================================
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'funcao', 'cpf', 'cnh', 'usuario')
    list_filter = ('funcao', 'usuario')
    search_fields = ('nome', 'cpf', 'cnh', 'usuario__username')
    list_per_page = 20


# ==========================================
# CONFIGURAÇÃO: VIAGEM
# ==========================================
@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'data_inicio', 'local_inicio', 'local_final', 
        'motorista', 'veiculo_1', 'status_da_viagem', 'valor_proposto', 'valor_pago'
    )
    # Filtros avançados por status e períodos de datas
    list_filter = ('status_da_viagem', 'data_inicio', 'data_quitacao', 'motorista', 'usuario')
    search_fields = ('local_inicio', 'local_final', 'carga', 'mic', 'motorista__nome', 'veiculo_1__placa')
    # Atalho para clicar e editar o status direto na listagem
    list_editable = ('status_da_viagem', 'valor_pago')
    list_per_page = 15


# ==========================================
# CONFIGURAÇÃO: ABASTECIDA
# ==========================================
@admin.register(Abastecida)
class AbastecidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_abastecida', 'veiculo', 'motorista_responsavel', 'valor_abastecida', 'litros', 'viagem')
    list_filter = ('data_abastecida', 'veiculo', 'motorista_responsavel', 'usuario')
    search_fields = ('veiculo__placa', 'motorista_responsavel__nome', 'viagem__id')
    list_per_page = 20


# ==========================================
# CONFIGURAÇÃO: CAIXA
# ==========================================
@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'centro_de_custo', 'valor_gasto', 'usuario')
    list_filter = ('data', 'centro_de_custo', 'usuario')
    search_fields = ('centro_de_custo', 'descricao', 'usuario__username')
    list_per_page = 20