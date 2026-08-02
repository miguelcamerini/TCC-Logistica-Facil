from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

# ==========================================
# MODEL: VEICULO
# ==========================================
class Veiculo(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('em_viagem', 'Em Viagem'),
        ('manutencao', 'Em Manutenção'),
        ('vendido', 'Vendido'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", db_index=True)
    nome_fantasia = models.CharField(max_length=100, verbose_name="Nome Fantasia")
    placa = models.CharField(max_length=7, unique=False, verbose_name="Placa", db_index=True)#nao pode ser unico porque um usuario pode vnder o veiculo para outro
    chassi = models.CharField(max_length=17, unique=False, verbose_name="Chassi")#nao pode ser unico porque um usuario pode vnder o veiculo para outro
    renavam = models.CharField(max_length=11, unique=False, verbose_name="RENAVAM") #nao pode ser unico porque um usuario pode vnder o veiculo para outro
    ano_fabricacao = models.PositiveIntegerField(verbose_name="Ano de Fabricação")
    ano_modelo = models.PositiveIntegerField(verbose_name="Ano do Modelo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel', verbose_name="Status", db_index=True)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def clean(self):
        if self.ano_fabricacao < 1900:
            raise ValidationError({'ano_fabricacao': 'Ano de fabricação deve ser maior que 1900'})
        if self.ano_modelo < 1900:
            raise ValidationError({'ano_modelo': 'Ano do modelo deve ser maior que 1900'})
        if self.ano_modelo < self.ano_fabricacao:
            raise ValidationError({'ano_modelo': 'Ano do modelo não pode ser anterior ao ano de fabricação'})

    def __str__(self):
        return f"{self.nome_fantasia} ({self.placa})"

    class Meta:
        db_table = 'veiculos'
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"


# ==========================================
# MODEL: FUNCIONARIO
# ==========================================

#(Foreing de status funcionario)-----------------------
class StatusFuncionario(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True, verbose_name="Status")

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'status_funcionarios'
        verbose_name = "Status de Funcionário"
        verbose_name_plural = "Status de Funcionários"
#-----------------------        

class Funcionario(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", db_index=True)
    nome = models.CharField(max_length=150, verbose_name="Nome")
    funcao = models.CharField(max_length=100, verbose_name="Função")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF", db_index=True)
    cnh = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name="CNH")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    status = models.ForeignKey(
        StatusFuncionario, 
        on_delete=models.PROTECT, 
        verbose_name="Status",
        blank=True,
        null=True
    )

    def clean(self):
        if len(self.cpf) != 11 or not self.cpf.isdigit():
            raise ValidationError({'cpf': 'CPF deve conter 11 dígitos'})
        if self.cnh and (len(self.cnh) != 11 or not self.cnh.isdigit()):
            raise ValidationError({'cnh': 'CNH deve conter 11 dígitos'})

    def __str__(self):
        return f"{self.nome} - {self.funcao}"

    class Meta:
        db_table = 'funcionarios'
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
 
# ==========================================
# MODEL: VIAGEM
# ==========================================
class Viagem(models.Model):
    STATUS_VIAGEM_CHOICES = [
        ('planejada', 'Planejada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('quitada', 'Quitada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", db_index=True)
    contratante = models.CharField(max_length=150, verbose_name="Contratante")
    data_inicio = models.DateField(verbose_name="Data de Início", db_index=True)
    data_final = models.DateField(blank=True, null=True, verbose_name="Data Final")
    data_adiantamento = models.DateField(blank=True, null=True, verbose_name="Data do Adiantamento")
    data_quitacao = models.DateField(blank=True, null=True, verbose_name="Data da Quitação")
    local_inicio = models.CharField(max_length=255, verbose_name="Local de Início")
    local_final = models.CharField(max_length=255, verbose_name="Local Final")
    km_rodados = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name="KM Rodados")
    status_da_viagem = models.CharField(max_length=20, choices=STATUS_VIAGEM_CHOICES, default='planejada', verbose_name="Status da Viagem", db_index=True)
    carga = models.CharField(max_length=150, blank=True, null=True, verbose_name="Carga")
    mic = models.CharField(max_length=50, blank=True, null=True, verbose_name="MIC")
    
    motorista = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name="viagens_motorista", verbose_name="Motorista")
    veiculo_1 = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name="viagens_veiculo", verbose_name="Veículo Principal")
    reboque = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, blank=True, null=True, related_name="viagens_reboque", verbose_name="Reboque")
    
    valor_proposto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Proposto")
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Pago")
    media = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, verbose_name="Média de Consumo (km/L)")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def clean(self):
        if self.data_final and self.data_final < self.data_inicio:
            raise ValidationError({'data_final': 'Data final não pode ser anterior à data de início'})
        if self.reboque and self.reboque.id == self.veiculo_1.id:
            raise ValidationError({'reboque': 'O reboque não pode ser o mesmo veículo principal'})
        if self.valor_pago > self.valor_proposto:
            raise ValidationError({'valor_pago': 'Valor pago não pode ser maior que o valor proposto'})
        if self.km_rodados < 0:
            raise ValidationError({'km_rodados': 'KM rodados não pode ser negativo'})

    def __str__(self):
        # Formata a data para o padrão brasileiro (DD/MM/AAAA) ao exibir
        data_formatada = self.data_inicio.strftime('%d/%m/%Y')
        return f"Viagem {self.id} ({data_formatada}): {self.local_inicio} X {self.local_final} [{self.get_status_da_viagem_display()}]"
    
    class Meta:
        db_table = 'viagens'
        verbose_name = "Viagem"
        verbose_name_plural = "Viagens"


# ==========================================
# MODEL: ABASTECIDA
# ==========================================
class Abastecida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", db_index=True)
    data_abastecida = models.DateField(verbose_name="Data do Abastecimento", db_index=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, verbose_name="Veículo")
    motorista_responsavel = models.ForeignKey(Funcionario, on_delete=models.PROTECT, verbose_name="Motorista Responsável")
    viagem = models.ForeignKey(Viagem, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Viagem")
    valor_abastecida = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor do Abastecimento")
    litros = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Litros Abastecidos")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def clean(self):
        if self.litros <= 0:
            raise ValidationError({'litros': 'Quantidade de litros deve ser maior que 0'})
        if self.valor_abastecida <= 0:
            raise ValidationError({'valor_abastecida': 'Valor do abastecimento deve ser maior que 0'})

    def __str__(self):
        return f"Abastecimento {self.id} - R$ {self.valor_abastecida}"

    class Meta:
        db_table = 'abastecimentos'
        verbose_name = "Abastecimento"
        verbose_name_plural = "Abastecimentos"


# ==========================================
# MODEL: CAIXA
# ==========================================
class Caixa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", db_index=True)
    data = models.DateField(verbose_name="Data", db_index=True)
    valor_gasto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Gasto")
    centro_de_custo = models.CharField(max_length=100, verbose_name="Centro de Custo")
    descricao = models.TextField(verbose_name="Descrição")

    def clean(self):
        if self.valor_gasto <= 0:
            raise ValidationError({'valor_gasto': 'Valor gasto deve ser maior que 0'})

    def __str__(self):
        data_formatada = self.data.strftime('%d/%m/%Y') if self.data else "Sem data"
        return f"Gasto {self.id} ({data_formatada}) - R$ {self.valor_gasto} ({self.centro_de_custo})"

    class Meta:
        db_table = 'caixa'
        verbose_name = "Fluxo de Caixa"
        verbose_name_plural = "Fluxos de Caixa"