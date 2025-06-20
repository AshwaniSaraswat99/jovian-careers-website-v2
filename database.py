
from sqlalchemy import create_engine, inspect, text
import os

engine = create_engine(os.environ["DB_CONNECTION_STRING"])

inspector = inspect(engine)
print("Available tables:", inspector.get_table_names())

with engine.connect() as conn:
    result = conn.execute(text("SELECT * from Jobs"))

    rows = result.mappings().all()  # returns list of MappingRow

    print(rows)                     # full list
    print(type(rows[0]))           # MappingRow
    print(dict(rows[0]))           # convert to normal dict


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Jobs"))
        rows = result.mappings().all()
        jobs = [dict(row) for row in rows]
        return jobs