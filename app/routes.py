from flask import render_template
from app import app
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


@app.route('/')
def main_page():
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
    return render_template('profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
