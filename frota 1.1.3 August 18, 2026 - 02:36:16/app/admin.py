from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Veiculo, StatusFuncionario, Funcionario, Viagem, Abastecida, Caixa

# ==========================================
# INLINES (Tabelas estrangeiras dentro do painel de edição)
# ==========================================

class AbastecidaInline(admin.TabularInline):
    model = Abastecida
    extra = 0  # Quantidade de linhas em branco extras para adicionar novos registros
    fields = ('data_abastecida', 'veiculo', 'motorista_responsavel', 'valor_abastecida', 'litros')
    # Evita carregar listas gigantescas no select de veículo e motorista dentro do inline
    raw_id_fields = ('veiculo', 'motorista_responsavel')


class ViagemMotoristaInline(admin.TabularInline):
    model = Viagem
    fk_name = 'motorista'  # Define qual FK usar caso haja mais de uma para o mesmo model
    extra = 0
    fields = ('data_inicio', 'local_inicio', 'local_final', 'veiculo_1', 'status_da_viagem', 'valor_proposto')
    raw_id_fields = ('veiculo_1', 'reboque')


# ==========================================
# CONFIGURAÇÕES DOS ADMINS
# ==========================================

@admin.register(StatusFuncionario)
class StatusFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_fantasia', 'placa', 'renavam', 'chassi', 'ano_modelo', 'status', 'usuario')
    list_filter = ('status', 'ano_fabricacao', 'ano_modelo', 'usuario')
    search_fields = ('nome_fantasia', 'placa', 'chassi', 'renavam', 'usuario__username')
    list_per_page = 20


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'funcao', 'cpf', 'cnh', 'status', 'usuario')
    list_filter = ('funcao', 'status', 'usuario')
    search_fields = ('nome', 'cpf', 'cnh', 'usuario__username')
    list_per_page = 20
    # Adiciona a lista de Viagens deste motorista direto na tela de edição dele!
    inlines = [ViagemMotoristaInline]


# ==========================================
# CONFIGURAÇÃO: VIAGEM
# ==========================================
@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    # Atualizados para os novos campos e incluindo o valor_total (propriedade calculada)
    list_display = (
        'id', 'contratante', 'data_inicio', 'data_final', 'local_inicio', 'local_final', 
        'motorista', 'veiculo_1', 'status_da_viagem', 'valor_adiantamento', 'valor_quitacao', 'valor_total'
    )
    list_filter = ('status_da_viagem', 'data_inicio', 'data_quitacao', 'contratante', 'motorista', 'usuario')
    search_fields = ('contratante', 'local_inicio', 'local_final', 'carga', 'mic', 'motorista__nome', 'veiculo_1__placa')
    
    # Atualizado o list_editable para usar o status e o valor_quitacao
    list_editable = ('status_da_viagem', 'valor_quitacao')
    list_per_page = 15
    
    raw_id_fields = ('motorista', 'veiculo_1', 'reboque')
    inlines = [AbastecidaInline]

@admin.register(Abastecida)
class AbastecidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_abastecida', 'veiculo_link', 'motorista_responsavel_link', 'valor_abastecida', 'litros', 'viagem')
    list_filter = ('data_abastecida', 'veiculo', 'motorista_responsavel', 'usuario')
    search_fields = ('veiculo__placa', 'motorista_responsavel__nome', 'viagem__id')
    list_per_page = 20
    raw_id_fields = ('veiculo', 'motorista_responsavel', 'viagem')

    # Exemplo de link direto: Cria um atalho clicável para abrir o veículo correspondente no admin
    def veiculo_link(self, obj):
        if obj.veiculo:
            url = reverse("admin:enterprise_veiculo_change", args=[obj.veiculo.id])
            return format_html('<a href="{}">{}</a>', url, obj.veiculo)
        return "-"
    veiculo_link.short_description = "Veículo"

    # Cria um atalho clicável para abrir o funcionário correspondente no admin
    def motorista_responsavel_link(self, obj):
        if obj.motorista_responsavel:
            url = reverse("admin:enterprise_funcionario_change", args=[obj.motorista_responsavel.id])
            return format_html('<a href="{}">{}</a>', url, obj.motorista_responsavel)
        return "-"
    motorista_responsavel_link.short_description = "Motorista Responsável"


@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'data', 'tipo', 'centro_de_custo', 
        'mic_exibicao', 'nota_fiscal_exibicao', 'valor_entrada', 'valor_saida', 'usuario'
    )
    list_filter = ('tipo', 'data', 'usuario')
    search_fields = ('centro_de_custo', 'descricao')
    list_per_page = 20