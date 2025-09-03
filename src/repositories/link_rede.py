from typing import Sequence

from sqlmodel import Session, select

from models.link_rede import LinkRedeDB


def buscar_links_rede(session: Session) -> Sequence[LinkRedeDB]:
    return session.exec(select(LinkRedeDB)).all()


def buscar_link_rede_por_id(link_rede_id: int, session: Session) -> LinkRedeDB | None:
    return session.get(LinkRedeDB, link_rede_id)


def adicionar_link_rede(link_rede: LinkRedeDB, session: Session) -> LinkRedeDB:
    session.add(link_rede)
    session.commit()
    session.refresh(link_rede)
    return link_rede


def atualizar_link_rede_bd(link_rede_id: int, link_rede: LinkRedeDB, session: Session) -> LinkRedeDB | None:
    link_rede_existente = session.get(LinkRedeDB, link_rede_id)
    if not link_rede_existente:
        return None
    link_rede_existente.link = link_rede.link
    link_rede_existente.nome_rede = link_rede.nome_rede
    link_rede_existente.nome_usuario = link_rede.nome_usuario
    link_rede_existente.id_usuario = link_rede.id_usuario
    session.commit()
    session.refresh(link_rede_existente)
    return link_rede_existente


def remover_link_rede(link_rede_id: int, session: Session) -> LinkRedeDB | None:
    link_rede_existente = buscar_link_rede_por_id(link_rede_id, session)
    if not link_rede_existente:
        return None
    session.delete(link_rede_existente)
    session.commit()
    return link_rede_existente
