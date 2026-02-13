from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("DATABASE_CONNECTION_SUCCESS")
    except Exception as e:
        print(f"DATABASE_CONNECTION_FAILED: {e}")
