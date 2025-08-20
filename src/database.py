from typing import Any, Generator

from sqlmodel import SQLModel, create_engine
from sqlmodel.orm.session import Session

from config import settings

engine = create_engine(settings.database_url)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, None]:
    from sqlmodel import Session

    with Session(engine) as session:
        yield session
