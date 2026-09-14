'''
Helper for connecting to the Postgres warehouse from a notebook.

Import this into any notebook to get a live connection, then use pandas to
read whatever dbt has built. Keeping the connection in one place means you
set it up once and reuse it everywhere.
'''

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Find the .env file that sits one folder above this notebooks folder, then
# load those values so this file can read your database settings.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / '.env')


def get_engine():
    '''
    Build and return a connection to the warehouse.

    This reads the same settings dbt uses from your .env file, so the notebook
    and dbt always point at the same database. It returns a SQLAlchemy engine,
    which pandas can read from directly with pd.read_sql.
    '''
    host = os.environ['POSTGRES_HOST']
    port = os.environ['POSTGRES_PORT']
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    database = os.environ['POSTGRES_DB']

    connection_url = (
        f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    )
    return create_engine(connection_url)
