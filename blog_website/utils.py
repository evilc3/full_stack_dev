import bcrypt
from flask_mail import Message
import hashlib
from db import mongodb_blog

def generate_blog_id(content):
    '''
    content : user_name + user_email + blog_content
    '''
    return hashlib.sha256(content.encode()).hexdigest()

def send_email(mail, item):

    username = item['username']
    user_gmail = item['email']
    verification_code = item['verification_code']

    # Send verification email
    msg = Message('Verify your email', sender='clivefernandes20@example.com', recipients=[user_gmail])
    msg.body = f'Hi {username}, your verification code is: http://localhost:8000/verify/{user_gmail}/{verification_code}'
    mail.send(message=msg)

def generate_verification_code(email):
    return hash(email)

def find_blogs(limit=10, blog_name=None):
    ###fetch top blogs from the database.
    # return ['blogs'] * 10
    ### {'blog_id': code, 'user_id': user_data['email'], 'blog': html_blog,}

    all_blogs = mongodb_blog.get_all()

    # print([i for i in all_blogs])

    return all_blogs
    # return [f"{item['user_id']}: {item['title']}" for item in all_blogs]

# Function to hash a password with a salt
def hash_password(password):
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password, salt

# Function to verify a password against a hashed password and salt
def verify_password(password, hashed_password, salt):
    # Hash the password with the provided salt
    new_hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Compare the new hashed password with the provided hashed password
    return new_hashed_password == hashed_password