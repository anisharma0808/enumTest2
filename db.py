from sqlmodel import create_engine, Session
from typing import Generator

DATABASE_URL = 'sqlite:///enumTest2.sqlite'

engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session