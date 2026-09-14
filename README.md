# dbt Samples
This is meant to be a growing set of dbt samples used during development.  I structured the SQL in a manner that would make more sense to someone coming from a SQL Server enviroment or someone who prefers to write and test their SQL something like DBeaver or SSMS.

___
___
### Setup:
#### UV:
Using UV is optional, but recommended.  
Update UV enviroment:
```bash
uv sync
```

Create a copy of the .env.example:
```bash
cp .env.example .env
```
____

#### Docker and Postgres:
The compose.yaml will build your Postgre container using some of the configurations from the .env file.
```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=dbt_samples
POSTGRES_USER=dbt_user
POSTGRES_PASSWORD=dbt_password

COMPOSE_PROJECT_NAME=dbt_samples
```

Start PostgreSQL Docker container  :
The '-d' lets this run in the background and is not required
```bash
docker compose up -d
```

___
#### Raw Data:
The ./data_setup/ folder included a series of functions to build some sample data.
You can tweak a few variables in the 'generate_sample_date.py' file:
```python
# A fixed seed means 'random' produces the same sequence on every run.
RANDOM_SEED = 47

# How much data to create.
NUM_CUSTOMERS = 2000
NUM_PRODUCTS = 1500
NUM_ORDERS = 30000

# The two year window that orders fall within.
START_DATE = date(2020, 1, 1)
END_DATE = date(2025, 12, 31)
```
The 'Build and Load Data.ipynb' notebook guides you through the process to build and upload the data.

___
#### dbt
dbt
**profiles.yml** and **dbt_project.yml** can be left untouched

Run **deps** and **debug** to install any missing dependancies and also check your local configurations
```bash
uv run --project .. dbt deps
uv run --project .. dbt debug
```

This block sets up a shell letting dbt know where everything is for things like Database credentials
```bash
cd dbt_samples
export DBT_PROFILES_DIR="$(pwd)"
set -a; source ../.env; set +a
```

```bash
uv run --project .. dbt build
```

___
#### File Tree:
```
dbt_samples/
├── .env
├── docker_compose.yml
├── .gitignore                  new  keeps .env and build output out of git
├── pyproject.toml              new  uv managed dependencies
├── README.md                   new  step by step run guide
├── dbt_project.yml             new  dbt project config
├── profiles.yml                new  connection, reads env vars only
├── packages.yml                new  dbt_utils entry, commented for later
├── seeds/
│   └── raw_orders.csv          new  tiny sample so the project runs immediately
├── models/
│   ├── staging/
│   │   └── _staging.yml         new  descriptions and tests
│   └── marts/
│       └── orders_by_customer.sql  new  simple aggregate on the staging model
├── macros/.gitkeep
├── tests/.gitkeep
└── notebooks/
    ├── warehouse_connection.py  new  helper to connect from a notebook
    └── explore.ipynb            new  starter notebook that inspects what dbt built
```