from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Veiculo, StatusFuncionario, Funcionario, Viagem, Abastecida, Caixa

# ==========================================
# INLINES
# ==========================================

class AbastecidaInline(admin.TabularInline):
    model = Abastecida
    extra = 0
    fields = ('data_abastecida', 'veiculo', 'motorista_responsavel', 'valor_abastecida', 'litros', 'nota_fiscal')
    raw_id_fields = ('veiculo', 'motorista_responsavel')


class ViagemMotoristaInline(admin.TabularInline):
    model = Viagem
    fk_name = 'motorista'
    extra = 0
    fields = ('data_inicio', 'local_inicio', 'local_final', 'veiculo_1', 'status_da_viagem', 'valor_total', 'media')
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
    inlines = [ViagemMotoristaInline]


@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    # Inclui Nota Fiscal, MIC e a Média calculada (Km/L)
    list_display = (
        'id', 'contratante', 'data_inicio', 'data_final', 'local_inicio', 'local_final', 
        'mic', 'nota_fiscal', 'km_rodados', 'media', 'motorista', 'veiculo_1', 
        'status_da_viagem', 'valor_adiantamento', 'valor_quitacao', 'valor_total'
    )
    list_filter = ('status_da_viagem', 'data_inicio', 'data_quitacao', 'contratante', 'motorista', 'usuario')
    search_fields = ('contratante', 'local_inicio', 'local_final', 'carga', 'mic', 'nota_fiscal', 'motorista__nome', 'veiculo_1__placa')
    
    list_editable = ('status_da_viagem', 'valor_quitacao')
    list_per_page = 15
    
    raw_id_fields = ('motorista', 'veiculo_1', 'reboque')
    inlines = [AbastecidaInline]


@admin.register(Abastecida)
class AbastecidaAdmin(admin.ModelAdmin):
    # Removido 'nota_fiscal' de list_display e search_fields
    list_display = ('id', 'data_abastecida', 'veiculo_link', 'motorista_responsavel_link', 'valor_abastecida', 'litros', 'viagem')
    list_filter = ('data_abastecida', 'veiculo', 'motorista_responsavel', 'usuario')
    search_fields = ('veiculo__placa', 'motorista_responsavel__nome', 'viagem__id')
    list_per_page = 20
    raw_id_fields = ('veiculo', 'motorista_responsavel', 'viagem')

    def veiculo_link(self, obj):
        if obj.veiculo:
            url = reverse("admin:app_veiculo_change", args=[obj.veiculo.id])
            return format_html('<a href="{}">{}</a>', url, obj.veiculo)
        return "-"
    veiculo_link.short_description = "Veículo"

    def motorista_responsavel_link(self, obj):
        if obj.motorista_responsavel:
            url = reverse("admin:app_funcionario_change", args=[obj.motorista_responsavel.id])
            return format_html('<a href="{}">{}</a>', url, obj.motorista_responsavel)
        return "-"
    motorista_responsavel_link.short_description = "Motorista Responsável"


@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    # Usando os métodos/propriedades existentes do seu model Caixa (ex: mic_exibicao)
    list_display = (
        'id', 'data', 'tipo', 'centro_de_custo', 
        'valor_entrada', 'valor_saida', 'usuario'
    )
    list_filter = ('tipo', 'data', 'usuario')
    search_fields = ('centro_de_custo', 'descricao')
    list_per_page = 20