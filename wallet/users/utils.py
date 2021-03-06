import os
import secrets
from PIL import Image
from flask import current_app, url_for
from flask_mail import Message
from wallet import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_filename)
    
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_filename



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request then ignore this email.    
    '''
    mail.send(msg)

def send_welcome_email(user):
    msg = Message('Welcome in eWallet!', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''Hope you will enjoy our website {user.username}'''
    mail.send(msg)