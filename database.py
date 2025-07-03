from sqlalchemy import create_engine, inspect, text
import os

# Ensure environment variable is set
if "DB_CONNECTION_STRING_1" not in os.environ:
    raise RuntimeError("Environment variable DB_CONNECTION_STRING_1 is not set")

engine = create_engine(os.environ["DB_CONNECTION_STRING_1"])

# Optional: print available tables
inspector = inspect(engine)
print("Available tables:", inspector.get_table_names())


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Jobs"))
        rows = result.mappings().all()  # MappingRow to dict
        jobs = [dict(row) for row in rows]
        return jobs


def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM Jobs WHERE id = :val"),
            {"val": id}
        )
        rows = result.mappings().all()
        if len(rows) == 0:
            return None
        else:
            return dict(rows[0])
def add_application_to_db(job_id, data):
    with engine.begin() as conn:  
        query = text("""
            INSERT INTO application (
                job_id, name, email, contact, linkedin,
                education, work_experience, resume
            ) VALUES (
                :job_id, :name, :email, :contact, :linkedin,
                :education, :work_experience, :resume
            )
        """)
        conn.execute(query, {
            'job_id': job_id,
            'name': data['name'],
            'email': data['email'],
            'contact': data['Contact'],
            'linkedin': data['linked_in'],
            'education': data['Education'],
            'work_experience': data['Work_Experience'],
            'resume': data['resume']
        })
