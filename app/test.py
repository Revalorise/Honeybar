from mojang import API

api = API()


def get_minecraft_avatar(uuid: str) -> str:
    avatar = f'https://mc-heads.net/avatar/{uuid}',
    return avatar[0]


avatar = get_minecraft_avatar('3ccf053de27a4f45a8e9d6d1feaa9977')
print(type(avatar))
