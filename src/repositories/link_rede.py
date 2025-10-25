"""Repositório para operações de links de redes sociais."""

from collections.abc import Sequence

from sqlmodel import Session, select

from models.link_rede import LinkRedeDB


def buscar_links_rede(session: Session) -> Sequence[LinkRedeDB]:
    """Retorna todos os links de redes sociais.

    Args:
        session: Sessão do banco de dados.

    Returns:
        Sequence[LinkRedeDB]: Lista de links de redes sociais.

    """
    return session.exec(select(LinkRedeDB)).all()


def buscar_link_rede_por_id(
    link_rede_id: int, session: Session
) -> LinkRedeDB | None:
    """Busca um link de rede social pelo ID.

    Args:
        link_rede_id: ID do link de rede social.
        session: Sessão do banco de dados.

    Returns:
        LinkRedeDB | None: Link de rede social encontrado ou None.

    """
    return session.get(LinkRedeDB, link_rede_id)


def adicionar_link_rede(link_rede: LinkRedeDB, session: Session) -> LinkRedeDB:
    """Adiciona um novo link de rede social.

    Args:
        link_rede: Dados do link de rede social a ser adicionado.
        session: Sessão do banco de dados.

    Returns:
        LinkRedeDB: Link de rede social adicionado.

    """
    session.add(link_rede)
    session.commit()
    session.refresh(link_rede)
    return link_rede


def atualizar_link_rede_bd(
    link_rede_id: int, link_rede: LinkRedeDB, session: Session
) -> LinkRedeDB | None:
    """Atualiza um link de rede social existente.

    Args:
        link_rede_id: ID do link de rede social a ser atualizado.
        link_rede: Novos dados do link de rede social.
        session: Sessão do banco de dados.

    Returns:
        LinkRedeDB | None: Link de rede social atualizado ou None.

    """
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


def remover_link_rede(
    link_rede_id: int, session: Session
) -> LinkRedeDB | None:
    """Remove um link de rede social.

    Args:
        link_rede_id: ID do link de rede social a ser removido.
        session: Sessão do banco de dados.

    Returns:
        LinkRedeDB | None: Link de rede social removido ou None.

    """
    link_rede_existente = buscar_link_rede_por_id(link_rede_id, session)
    if not link_rede_existente:
        return None
    session.delete(link_rede_existente)
    session.commit()
    return link_rede_existente
