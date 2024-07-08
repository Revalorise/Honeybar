from mojang import API

api = API()


def get_minecraft_avatar(uuid: str) -> str:
    avatar = f'https://mc-heads.net/avatar/{uuid}',
    return avatar[0]
