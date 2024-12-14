from flask import Flask
from models import db, Book, Author, Publisher  # Включаємо Author і Publisher
from routes import routes
from config import Config
import time
import random

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(routes)
    return app

def initialize_related_tables():
    """Ініціалізація таблиць author і publisher."""
    with app.app_context():
        if not db.session.query(Author).first():
            db.session.bulk_save_objects([
                Author(name=f"Author {i}") for i in range(1, 11)  # Додаємо 10 авторів
            ])
            db.session.commit()

        if not db.session.query(Publisher).first():
            db.session.bulk_save_objects([
                Publisher(name=f"Publisher {i}") for i in range(1, 11)  # Додаємо 10 видавців
            ])
            db.session.commit()

def populate_db(record_count):
    """Заповнення бази даних тестовими даними."""
    print(f"Populating database with {record_count} records...")
    with app.app_context():
        db.session.bulk_save_objects([
            Book(
                title=f"Book {random.randint(1, 1000)}",
                author_id=random.randint(1, 10),  # Ідентифікатори авторів (1-10)
                publisher_id=random.randint(1, 10)  # Ідентифікатори видавців (1-10)
            )
            for _ in range(record_count)
        ])
        db.session.commit()
    print(f"Successfully added {record_count} records.")

def measure_query_performance(record_count):
    """Замір продуктивності для SELECT, UPDATE, INSERT, DELETE."""
    print(f"Measuring query performance for {record_count} records...")
    
    # SELECT
    start_time = time.time()
    with app.app_context():
        results = Book.query.all()
    select_time = time.time() - start_time
    
    # UPDATE
    start_time = time.time()
    with app.app_context():
        for record in results:
            record.title = f"Updated Title {random.randint(1, 1000)}"
        db.session.commit()
    update_time = time.time() - start_time

    # INSERT
    start_time = time.time()
    with app.app_context():
        db.session.bulk_save_objects([
            Book(
                title=f"New Book {random.randint(1, 1000)}",
                author_id=random.randint(1, 10),
                publisher_id=random.randint(1, 10)
            )
            for _ in range(record_count)
        ])
        db.session.commit()
    insert_time = time.time() - start_time

    # DELETE
    start_time = time.time()
    with app.app_context():
        db.session.query(Book).delete()
        db.session.commit()
    delete_time = time.time() - start_time

    print(f"Results for {record_count} records:")
    print(f"SELECT: {select_time:.4f} seconds")
    print(f"UPDATE: {update_time:.4f} seconds")
    print(f"INSERT: {insert_time:.4f} seconds")
    print(f"DELETE: {delete_time:.4f} seconds")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        initialize_related_tables()  # Ініціалізація авторів і видавців

    # Тестування з різними обсягами даних
    for count in [1000, 10000, 100000, 1000000]:
        populate_db(count)
        measure_query_performance(count)

    app.run(debug=True)
