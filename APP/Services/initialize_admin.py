from APP import db
from APP.models import User
from werkzeug.security import generate_password_hash

def initialize_admin_user():
    # Check if an admin user already exists
    admin_user = User.query.filter_by(role='admin').first()
    if not admin_user:
        # Create a default admin user
        default_admin = User(
            username='admin',
            password=generate_password_hash('admin123'),  # Default password
            role='admin'
        )
        db.session.add(default_admin)
        try:
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating default admin user: {e}")