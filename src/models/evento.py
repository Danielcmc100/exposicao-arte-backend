"""Modelos de dados para eventos culturais."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .obra_evento import ObraEventoDB

if TYPE_CHECKING:
    from models import ComentarioEventoDB, ObraDB, UsuarioDB

    from .avaliacoes_eventos import AvaliacaoEventoDB


class EventoBase(SQLModel):
    endereco: str = Field(description="Endereço completo do local do evento.")
    local: str = Field(
        description=(
            "Nome ou ponto de referência do local do evento "
            "(ex: 'Galeria Central')."
        )
    )
    latitude: float = Field(
        description="Latitude da coordenada geográfica do local do evento."
    )
    longitude: float = Field(
        description="Longitude da coordenada geográfica do local do evento."
    )
    data: datetime = Field(description="Data e hora de início do evento.")
    id_organizador: int = Field(foreign_key="usuarios.id")
    id_responsavel: int = Field(foreign_key="usuarios.id")


class EventoCreate(EventoBase):
    nome: str = Field(description="Nome de identificação do evento.")


class EventoResponse(EventoBase):
    id: int


class EventoDB(EventoCreate, table=True):
    __tablename__ = "eventos"  # type: ignore

    id: int = Field(default=None, primary_key=True)

    organizador: "UsuarioDB" = Relationship(
        sa_relationship_kwargs={"foreign_keys": ("EventoDB.id_organizador")}
    )
    responsavel: "UsuarioDB" = Relationship(
        sa_relationship_kwargs={"foreign_keys": ("EventoDB.id_responsavel")}
    )
    comentarios: list["ComentarioEventoDB"] = Relationship()
    obras: list["ObraDB"] = Relationship(
        back_populates="eventos", link_model=ObraEventoDB
    )
    avaliacoes_eventos: list["AvaliacaoEventoDB"] = Relationship(
        back_populates="evento"
    )


class PrevisaoEvento(SQLModel):
    latitude: float = Field(
        ge=-90,
        le=90,
        description="Latitude da coordenada geográfica (-90 a 90)",
    )
    longitude: float = Field(
        ge=-180,
        le=180,
        description="Longitude da coordenada geográfica (-180 a 180)",
    )
    dia_da_semana: int = Field(
        ge=0, le=6, description="Dia da semana (0=Segunda, 6=Domingo)"
    )
    mes: int = Field(
        ge=1, le=12, description="Mês do ano (1=Janeiro, 12=Dezembro)"
    )
