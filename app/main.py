from flask import Blueprint, render_template, flash
from flask import redirect
from flask.globals import request
from flask.helpers import url_for
from flask_login import login_required, current_user
from . import db

from .models import User
from .exportslib.gmail_dl import test_gmail_login


main = Blueprint('main', __name__)


@main.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/profile')
@login_required
def profile():
    gmail_email = current_user.gmail_email or ""

    return render_template('profile.html', name=current_user.name, 
                            gmail_email=gmail_email)

@main.route('/profile/updategmail', methods=['POST'])
def profile_post():
    gmail_email = request.form.get('email')
    gmail_password = request.form.get('password')

    good_login = test_gmail_login(gmail_email, gmail_password)

    if not good_login:
        flash("Please check your login details and try again.")
        return redirect(url_for('main.profile'))
    
    user = User.query.filter_by(id=current_user.id).first()
    user.gmail_email = gmail_email
    # NOTE: this password is not hashed, it is stored plaintext. This is because the plaintext password is needed
    # to interface with gmail's IMAP. DO NOT USE A PASSWORD THAT SECURES ANY OF YOUR OTHER ONLINE ACCOUNTS.
    user.gmail_password = gmail_password

    db.session.commit()

    return redirect(url_for('main.index'))
