
from app.database.connection import Base, engine
from app.database import models


def initialize_database():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

    print("\nAvailable tables:")
    for table_name in Base.metadata.tables:
        print(f"- {table_name}")


if __name__ == "__main__":
    initialize_database()
