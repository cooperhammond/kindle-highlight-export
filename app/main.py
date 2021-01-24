from flask import Blueprint, render_template, flash
from flask import redirect
from flask.globals import request
from flask.helpers import url_for
from flask_login import login_required, current_user
from . import db

from .models import User, Export
from .exportslib.gmail_dl import test_gmail_login
from .exportslib import get_formatted_exports


main = Blueprint('main', __name__)


@main.route('/')
def index():
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
    # NOTE: this password is not hashed, it is stored plaintext. This is because the hashed password would be
    # useless to interface with gmail's IMAP. DO NOT USE A PASSWORD THAT SECURES ANY OF YOUR OTHER ONLINE ACCOUNTS.
    user.gmail_password = gmail_password

    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/highlights', methods=['POST'])
def highlights():
    gmail_email = request.form.get('email')
    gmail_password = request.form.get('password')

    if not test_gmail_login(gmail_email, gmail_password):
        flash("Please check your login details and try again.")
        return redirect(url_for('main.index'))

    exports = get_formatted_exports(gmail_email, gmail_password)

    # only logged in users should update the database
    if current_user.is_authenticated:
        for export_key in exports:

            # check if the export already exists in the database by comparing title and corresponding user 
            # and if does, update the contents of the export with the newly retrieved export
            export_already_existed = False
            existing_exports = Export.query.filter_by(title=export_key)
            for existing_export in existing_exports:
                if existing_export.title == export_key and existing_export.user_id == current_user.id:
                    existing_export.text = exports[export_key]
                    export_already_existed = True
                    db.session.add(existing_export)
        
            # if the export does not already exist, create and link it to the current_user
            if not export_already_existed:
                user = User.query.filter_by(id=current_user.id).first()
                new_export = Export(title=export_key, text=exports[export_key])
                user.exports.append(new_export)
                db.session.add(new_export)

        db.session.commit()

    return render_template('highlights.html', exports=exports)  

@main.route('/highlights', methods=['GET'])
def highlights_get():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))

    return render_template('highlights.html', )