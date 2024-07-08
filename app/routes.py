import sqlalchemy as sa
from flask import render_template,  redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

from app import app, db
from app.forms import LoginForm, RegisterForm, PostForm
from app.models import User, Post
from app.utils.load_minecraft_details import get_minecraft_avatar


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/staff')
def staff():
    staffs = db.session.scalars(
        sa.select(User).where(User.rank == 'Owner')).all()

    return render_template('staff.html',
                           staffs=staffs)


@app.route('/form/<int:page>')
def form(page=1):
    PER_PAGE = 5
    posts = [
        {'title': 'Hello!',
         'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
         'author': '_Revalorise',
         'body': "Allow me to introduce myself!"
         },
        {'title': 'Hello!',
         'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
         'author': 'Vcera',
         'body': "Allow me to introduce myself!"
         },
        {'title': 'Hello!',
         'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
         'author': 'Vcera',
         'body': "Allow me to introduce myself!"
         },
        {'title': 'Hello!',
         'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
         'author': 'Vcera',
         'body': "Allow me to introduce myself!"
         },
        {'title': 'Hello!',
         'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
         'author': 'Vcera',
         'body': "Allow me to introduce myself!"
         },
        {'title': 'Hello!',
         'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
         'author': 'Vcera',
         'body': "Allow me to introduce myself!"
         },
    ]

    return render_template('form.html', posts=posts)


@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.post.data, body=form.post.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('form', page=1))

    return render_template('form.html', form=form)


@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/profile')
def profile():
    """
    Display s the user's profile information, including their Minecraft username, rank, and UUID.
    """
    hb_rank = None
    mc_username = None
    uuid = None
    avatar = None

    if current_user.is_authenticated:
        hb_rank = db.session.scalar(
            sa.select(User.rank).where(User.id == current_user.id))
        mc_username = db.session.scalar(
            sa.select(User.minecraft_username).where(User.id == current_user.id))
        uuid = db.session.scalar(
            sa.select(User.minecraft_uuid).where(User.id == current_user.id))
        avatar = get_minecraft_avatar(uuid)

    else:
        redirect(url_for('profile'))

    return render_template('profile.html',
                           uuid=uuid,
                           hb_rank=hb_rank,
                           mc_username=mc_username,
                           avatar=avatar)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('profile'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('profile'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            minecraft_username=form.minecraft_username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        user.set_uuid(form.minecraft_username.data)
        uuid = user.get_uuid()
        user.set_avatar(get_minecraft_avatar(uuid))
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered!')
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('register.html', form=form)
