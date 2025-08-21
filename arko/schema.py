from pydantic import BaseModel, Field
from typing import List, Optional

class RegionSchema(BaseModel):
    id: int 
    nome: str 
    sigla: str 

class StateSchema(BaseModel):
    id: int 
    nome: str
    sigla: str 
    regiao: RegionSchema 

class UFSchema(BaseModel):
    id: int
    sigla: str
    nome: str 
    regiao: RegionSchema

class MunicipalityRefSchema(BaseModel):
    id:int

class MesorregiaoSchema(BaseModel):
    id: int
    nome: str
    UF: UFSchema

class MicrorregiaoSchema(BaseModel):
    id: int
    nome: str
    mesorregiao: Optional[MesorregiaoSchema] = Field(alias='mesorregiao')

class IntermediateRegion(BaseModel):
    id: int
    nome: str
    UF: UFSchema

class ImmediateRegion(BaseModel):
    id: int
    nome: str
    regiaointermediaria: IntermediateRegion = Field(alias='regiao-intermediaria')

class MunicipalitySchema(BaseModel):
    id: int
    nome: str = Field(alias='nome')
    microrregiao: Optional[MicrorregiaoSchema] = Field(alias='microrregiao')
    regiao_imediata: Optional[ImmediateRegion] = Field(alias='regiao-imediata')

class DistrictSchema(BaseModel):
    id: int
    nome: str = Field(alias='nome')
    municipio: MunicipalityRefSchema = Field(alias='municipio')
