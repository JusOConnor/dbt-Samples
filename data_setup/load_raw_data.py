'''
Loads the raw CSV files into the Postgres database, under a schema called 'raw'.

This is the step that puts data into the warehouse. dbt does not create this raw
data; it reads from it. In dbt terms, these loaded tables become your 'sources'.

Connection details are read from your .env file, so your password never has to be
typed into a script. Run this after generate_sample_data.py has created the CSVs.

The load is written to be safe to run again and again.
'''

import os
from pathlib import Path

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine, inspect, text

# The schema the raw tables land in. dbt will read from here but never write to it.
RAW_SCHEMA = 'raw'

# The four files produced by generate_sample_data.py, in load order.
RAW_TABLES = ['raw_customers', 'raw_products', 'raw_orders', 'raw_order_items']


def get_engine():
    '''
    Build a SQLAlchemy engine from the settings in your .env file.

    find_dotenv walks up the folder tree to locate the .env file, so this works
    whether you run it from the project root or from inside a notebook folder.
    '''
    load_dotenv(find_dotenv())

    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']
    port = os.environ['POSTGRES_PORT']
    database = os.environ['POSTGRES_DB']

    connection_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    return create_engine(connection_url)


def load_all(input_dir='raw_data'):
    '''
    Load every raw CSV into the raw schema. Safe to run repeatedly.

    If a table does not exist yet, it is created. If it already exists, it is
    emptied and refilled, which leaves any dbt views built on top of it untouched.
    '''
    engine = get_engine()
    input_path = Path(input_dir)

    # Make sure the target schema exists before loading anything into it.
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA}'))

    inspector = inspect(engine)

    for table_name in RAW_TABLES:
        source_file = input_path / f'{table_name}.csv'
        frame = pd.read_csv(source_file)

        if inspector.has_table(table_name, schema=RAW_SCHEMA):
            # Table exists: empty it, then append. No drop, so views survive.
            with engine.begin() as connection:
                connection.execute(text(f'TRUNCATE TABLE {RAW_SCHEMA}.{table_name}'))
            frame.to_sql(table_name, engine, schema=RAW_SCHEMA,
                         if_exists='append', index=False)
        else:
            # First time: let pandas create the table for us.
            frame.to_sql(table_name, engine, schema=RAW_SCHEMA,
                         if_exists='replace', index=False)

        print(f'Loaded {len(frame):>6} rows into {RAW_SCHEMA}.{table_name}')

    engine.dispose()


if __name__ == '__main__':
    load_all()
