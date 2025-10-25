"""Modelos de dados para associação entre obras e eventos."""

from sqlmodel import Field, SQLModel


class ObraEventoDB(SQLModel, table=True):
    __tablename__ = "obra_evento"  # type: ignore

    id_obra: int = Field(foreign_key="obras.id", primary_key=True)
    id_evento: int = Field(foreign_key="eventos.id", primary_key=True)
