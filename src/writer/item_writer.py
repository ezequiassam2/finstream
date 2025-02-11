import logging

import sqlalchemy as db

class ItemWriter:
    def __init__(self, engine_url):
        self.engine = db.create_engine(engine_url)

    def write(self, df):
        if not df.empty:
            with self.engine.begin() as connection:
                df.to_sql('transacoes', con=connection, if_exists='append', index=False)
                logging.info("Dados inseridos no banco de dados com sucesso.")
