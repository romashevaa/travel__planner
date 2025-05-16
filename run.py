from app import create_app
from app.extensions import db  # додай це

app = create_app()

# гарантовано створюємо БД
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
