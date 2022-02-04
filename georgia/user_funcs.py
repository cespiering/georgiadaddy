from georgia import db
from georgia.Database.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# ^USER RELATED FUNCTIONS:
def hash_password(password):
    """Takes in a password, uses werkzeug.security to return hashed password"""
    hash_pass = generate_password_hash(password)
    return hash_pass

def create_user(user_name, email, password):
    """Create and return a new user using hashed passwords."""
    password = hash_password(password)

    user = User(user_name = user_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_user(email):
    """Finds a user in db by email"""
    return User.query.filter_by(email=email).first()

def check_password(hash_pass, password):
    """Compares string password with hashed db password"""
    return check_password_hash(hash_pass, password)