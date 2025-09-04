from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(data_to_load, db_url, schema="public", if_exists="replace"):
    """
    Carrega DataFrames em tabelas PostgreSQL e cria o schema automaticamente se não existir.
    """
    engine = create_engine(db_url)

    try:
        # Garante que o schema existe
        with engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))
            conn.commit()
        logging.info(f"Schema '{schema}' verificado/criado com sucesso.")

        # Carrega os DataFrames no schema
        for table_name, df in data_to_load.items():
            df.to_sql(
                table_name,
                con=engine,
                schema=schema,
                index=False,
                if_exists=if_exists
            )
            logging.info(f"Tabela '{table_name}' carregada com sucesso no schema '{schema}'.")

    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        raise
