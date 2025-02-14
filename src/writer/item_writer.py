import logging


class ItemWriter:
    def __init__(self, engine_url='sqlite:///transacoes.db'):  # TODO: Adicionar suporte do bancos de dados
        # self.engine = db.create_engine(engine_url)
        self.engine = None

    def write(self, df):
        print(df)
        return
        if not df.empty:
            with self.engine.begin() as connection:
                df.to_sql('transacoes', con=connection, if_exists='append', index=False)
                logging.info("Dados inseridos no banco de dados com sucesso.")
