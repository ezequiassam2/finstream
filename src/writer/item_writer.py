import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.utilities.config import DATABASE_URL
from .model import Base


class ItemWriter:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save(self, data):
        session = self.Session()
        try:
            with session.begin():
                if isinstance(data, list):
                    session.add_all(data)
                else:
                    session.add(data)
            logging.info("Objeto inserido com sucesso.")
        except SQLAlchemyError as e:
            logging.error(f"Erro ao inserir objeto: {e}")
        finally:
            session.close()
