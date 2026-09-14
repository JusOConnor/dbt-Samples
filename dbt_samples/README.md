# dbt_lab

A starter dbt project that builds a small set of models into a local Postgres
warehouse. It ships with a tiny sample dataset, so you can run the whole flow
end to end before you point it at real data.

## What is in here

- `docker-compose.yml` and `.env` (your files) run Postgres in a container.
- `pyproject.toml` lists the tools; uv installs them into a private environment.
- `profiles.yml` holds the database connection and reads every value from `.env`.
- `dbt_project.yml` sets how each layer is built.
- `seeds/raw_orders.csv` is sample data that dbt loads into a table.
- `models/staging/stg_orders.sql` cleans that data.
- `models/marts/orders_by_customer.sql` summarizes it for a business question.
- `notebooks/` lets you read the results with pandas.

## One time setup

1. Install uv if you have not already. See the uv site for your platform.

2. Create your `.env` from the example and adjust it if your values differ:

   ```
   cp .env.example .env
   ```

3. Install the tools into a private environment for this folder:

   ```
   uv sync
   ```

## Every time you work

1. Start the warehouse:

   ```
   docker compose up -d
   ```

2. Confirm dbt can reach the database. The `--env-file` flag loads your `.env`
   into the command so dbt can read your settings:

   ```
   uv run --env-file .env dbt debug
   ```

3. Build everything and check it:

   ```
   uv run --env-file .env dbt seed     # load the sample data
   uv run --env-file .env dbt run      # build the models
   uv run --env-file .env dbt test     # check the results
   ```

   `dbt seed` loads the CSV, `dbt run` builds the staging view and the mart
   table, and `dbt test` confirms the key rules hold. dbt reads `profiles.yml`
   straight from this folder, so there is nothing else to point it at. If it
   ever cannot find the profile, set `DBT_PROFILES_DIR` to this folder.

## Look at the results in a notebook

Start Jupyter from inside this folder so the helper file is found:

   ```
   uv run --env-file .env jupyter lab
   ```

Open `notebooks/explore.ipynb` and run the cells. It connects to the same
database dbt just built into and reads two tables into pandas.

## Where to go next

- Add your own seed or point a model at a real source table.
- Turn on `dbt_utils` in `packages.yml` for ready made tests and macros.
- Add a `.yml` file next to the mart to document and test it, the same way
  `_staging.yml` documents the staging model.

## How the pieces stay in step

Your `.env` sets `POSTGRES_PORT=5434`, and Docker Compose maps that to the
container, so the database is reachable at `localhost:5434`. dbt and the
notebook both read that same value, so they always point at the same place.
