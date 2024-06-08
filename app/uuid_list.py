from mojang import API


api = API()


def get_user_details(email, username):
    uuid = api.get_uuid(username)
    avatar = f'https://mc-heads.net/avatar/{uuid}'


minecraft_uuids = {
    'Blackball007b@gmail.com': {
        'uuid': 'c93e86fe39f04779aa764bfddaf2f848'
    },
    'Vcera@honeybar-admin.com': {
        'uuid': '3ccf053de27a4f45a8e9d6d1feaa9977'
    },
}

minecraft_details = {
    '_Revalorise': {
        'uuid': minecraft_uuids['Blackball007b@gmail.com']['uuid'],
        'avatar': f'https://mc-heads.net/avatar/{minecraft_uuids["Blackball007b@gmail.com"]["uuid"]}',
        'username': api.get_username(minecraft_uuids['Blackball007b@gmail.com']['uuid'])
    },
    'Vcera': {
        'uuid':  minecraft_uuids['Vcera@honeybar-admin.com']['uuid'],
        'avatar': f'https://mc-heads.net/avatar/{minecraft_uuids["Vcera@honeybar-admin.com"]["uuid"]}',
        'username': api.get_username(minecraft_uuids['Vcera@honeybar-admin.com']['uuid']),
    },
}


def print_uuid_list():
    for users in minecraft_details:
        print(f'{users}')
