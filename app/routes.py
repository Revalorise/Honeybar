import sqlalchemy as sa
from flask import render_template,  redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import Users
from mojang import API


api = API()

uuid_revalorise = api.get_uuid('_Revalorise')
uuid_vcera = api.get_uuid('Vcera')

uuid_list = {
    'Revalorise': {
        'uuid': uuid_revalorise,
        'avatar': f'https://mc-heads.net/avatar/{uuid_revalorise}',
        'username': api.get_username(uuid_revalorise)
    },
    'Vcera': {
        'uuid':  uuid_vcera,
        'avatar': f'https://mc-heads.net/avatar/{uuid_vcera}',
        'username': api.get_username(uuid_vcera),
    },
    'Dummy': {
        'uuid': '069a79f444e94726a5befca90e38aaf5',
        'avatar': 'https://mc-heads.net/avatar/069a79f444e94726a5befca90e38aaf5',
        'username': 'Dummy Staff'
    }
}


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/staff')
def staff():
    return render_template('staff.html',
                           uuid_list=uuid_list)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/profile')
def profile():
    rank = None
    if current_user.is_authenticated:
        rank = db.session.scalar(
            sa.select(Users.rank).where(Users.id == current_user.id))
    else:
        redirect(url_for('profile'))
    return render_template('profile.html',
                           uuid_list=uuid_list,
                           rank=rank)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Users).where(Users.email == form.email.data))
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
        user = Users(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered!')
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('register.html', form=form)
