from app import create_app, db
from app.models import User

app = create_app()

def seed_admin():
    with app.app_context():
        # 检查是否已存在管理员
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', role='ADMIN')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username='admin', password='admin123'")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    seed_admin()