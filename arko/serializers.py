from rest_framework import serializers
from .models import Region, State, Municipality, District, Company

class RegionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Region model.
    """
    class Meta:
        model = Region
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    """
    Serializer for the State model.
    """
    regiao = RegionSerializer(read_only=True)

    class Meta:
        model = State
        fields = ['id', 'nome', 'sigla', 'regiao']

class MunicipalitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Municipality model.
    """
    # Em vez de mostrar o ID do estado, mostra a string definida no método __str__ do modelo State.
    estado = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Municipality
        fields = ['id', 'nome', 'estado']

class DistrictSerializer(serializers.ModelSerializer):
    """
    Serializer for the District model.
    """
    municipio = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model=District
        fields=['id', 'nome', 'municipio']

class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the Company model.
    """
    class Meta:
        model=Company
        fields='__all__'
