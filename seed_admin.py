from app import app, db
from models import User
from datetime import datetime

def seed_admin_user():
    with app.app_context():
        email = 'admin@example.com'
        password = 'admin'
        first_name = 'Admin'
        last_name = 'User'

        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User with email {email} already exists. Skipping password update.")
        else:
            print(f"Creating new admin user with email {email}.")
            user = User(email=email, first_name=first_name, last_name=last_name)
            user.set_password(password) # Set password only for new user
            user.last_login = datetime.utcnow() # Set initial last login time
            db.session.add(user)
        
        db.session.commit()
        print("Admin user seeding process completed.")

if __name__ == '__main__':
    seed_admin_user()