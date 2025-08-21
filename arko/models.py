# locations/models.py
from django.db import models

class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2)
    nome = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'

    def __str__(self):
        return self.nome

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=100)
    regiao = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='estados')

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['nome'] 

    def __str__(self):
        return f'{self.nome} ({self.sigla})'

class Municipality(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200)
    estado = models.ForeignKey(State, on_delete=models.PROTECT, related_name='municipios')

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class District(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200)
    municipio = models.ForeignKey(Municipality, on_delete=models.PROTECT, related_name='distritos')

    class Meta:
        verbose_name = 'Distritos'
        verbose_name_plural = 'Distritos'
        ordering = ['nome']

    def __str__(self):
        return self.nome
    
class Company(models.Model):
    cnpj = models.CharField(max_length=8, primary_key=True, help_text="CNPJ básico, 8 digitos")
    razao_social = models.CharField(max_length=255, db_index=True, help_text="Razão Social ou Nome Empresarial")
    natureza_juridica = models.CharField(max_length=4, help_text="Códgo da Natureza Jurídica")
    qualificacao_responsavel=models.CharField(max_length=2, help_text="Capital Social da Empresa")
    capital_social = models.DecimalField(max_digits=16, help_text="Porte da Empresa (01, 03, 05)", decimal_places=2)
    porte_empresa = models.CharField(max_length=2, help_text="Porte da Empresa (01, 03, 05)", null=True, blank=True)
    ente_federativo_responsavel = models.CharField(max_length=255, blank=True, null=True, help_text="Ente Federativo Responsável")

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['razao_social']
    
    def __str__(self):
        return self.razao_social