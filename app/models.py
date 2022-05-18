from app.database import sql_execute


class User:
    def __init__(self):
        self._type = 'user'
        self._username = ''
        self._email = ''
        self._name = ''
        self._lastname = ''
        self._password = ''

    def set_username(self, username: str):
        username = username.strip().title()
        if 0 < len(username) <= 50 and username.isalnum():
            self._username = username
        else:
            return f'"{username}" é inválido.'

    def set_email(self, email: str):
        email = email.strip()
        if email.find('@') != -1 or email.find('.') != -1 or 5 < len(email) <= 256:
            self._email = email
        else:
            return f'"{email}" é inválido.'

    def set_name(self, name: str):
        name = name.strip().title()
        if name.isalpha() or 0 < len(name) <= 50:
            self._name = name
        else:
            return f'"{name}" é inválido.'

    def set_lastname(self, lastname: str):
        lastname = lastname.strip().title()
        if lastname.isalpha() or 0 < len(lastname) <= 50:
            self._lastname = lastname
        else:
            return f'"{lastname}" é inválido.'

    def set_password(self, password: list):
        if password[0] == password[1]:
            if 8 <= len(f'{password[0]}') <= 50 and not password[0].isspace():
                self._password = password[0]
            else:
                return f'A senha é inválida.'
        else:
            return 'As senhas são diferentes.'

    def upload_to_database(self):
        if sql_execute(f"SELECT count(*) FROM users WHERE username='{self._username}';")[0][0] != 0:
            return 'Nome de usuário já existe.'
        elif sql_execute(f"SELECT count(*) FROM users WHERE email='{self._email}';")[0][0] != 0:
            return 'Endereço de Email já cadastrado.'
        else:
            sql_execute(
            f"""
            INSERT INTO `starlette`.`users` (id, username, email, password, name, lastname)
            VALUES (DEFAULT, '{self._username}', '{self._email}', '{self._password}', '{self._name}', '{self._lastname}');
            """)


class Post:
    def __init__(self, title: str, content: str, author: int, date, image: str=''):
        self._title = title.strip().upper()
        self._content = content.strip()
        self._image = image.strip()
        self._author = author
        self._date = date

    def check(self):
        errors = []
        if 1 > len(self._title) > 45:
            errors.append('Título Inválido.')
        if 1 > len(self._content) > 500:
            errors.append('Texto Inválido.')
        if self._image != '':
            if len(self._image) > 100:
                errors.append('Link da imagem inválida.')
            valid_formats = ['png', 'jpg', 'jpeg']
            if self._image.split('.')[1] not in valid_formats:
                errors.append('Formato de imagem inválido.')
        if sql_execute(f"SELECT COUNT(*) FROM users WHERE id={self._author}")[0][0] != 1:
            errors.append('O autor é inválido.')

        return errors

    def update_to_database(self):
        sql_execute(f"INSERT INTO `starlette`.`posts` (id, title, content, date, users_id)"
                    f"VALUES (DEFAULT, '{self._title}', '{self._content}', '{self._date}', {self._author})")
