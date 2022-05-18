import datetime

from app import database
from app.models import User, Post
from app.utils import logged

from starlette.templating import Jinja2Templates
from starlette.responses import PlainTextResponse, RedirectResponse, HTMLResponse


templates = Jinja2Templates(directory='templates')

host_ip = '127.0.0.1'


def home_page(request):
    return HTMLResponse(f'<script>window.location.replace("http://{host_ip}:5000/blog");</script>')
    #return templates.TemplateResponse('home.html', {
    #   'request': request,
    #   'nome': 'Jucian Kauê Decezare'
    #})


async def blog_page(request):
    log = logged(request.client.host)
    if not log == False:
        log = logged(request.client.host)[0]

    user_id = database.sql_execute(f"SELECT users_id FROM ip_user WHERE ip='{request.client.host}'")
    if user_id:
        user_id = user_id[0][0]

    if request.method == 'POST':
        form = await request.form()
        date_ = datetime.datetime.now()
        date = f'{date_.year}-{date_.month}-{date_.day} {date_.hour}:{date_.minute}:{date_.second}'
        post = Post(
            title=form['title'],
            content=form['content'],
            author=user_id,
            date=date
        )
        if len(post.check()) == 0:
            post.update_to_database()

        return HTMLResponse(f'<script>window.location.replace("http://{host_ip}:5000/blog");</script>')

    if request.method == 'GET':
        posts_ = database.sql_execute('SELECT * FROM posts;')
        posts = []
        for post in posts_:
            author = database.sql_execute(f'SELECT name, lastname FROM users WHERE id={post[5]}')[0]
            author_id = post[5]
            posts.append({
                'post_id': post[0],
                'title': post[1],
                'content': post[2],
                'image': post[3],
                'date': post[4],
                'author': f'{author[0]} {author[1]}',
                'author_id': author_id
            })

        return templates.TemplateResponse('blog.html', {
            'request': request,
            'user': log,
            'user_id': user_id,
            'posts': posts
        })


async def login_page(request):
    if logged(request.client.host):
        return HTMLResponse(f'<script>window.location.replace("http://{host_ip}:5000/blog");</script>')
    if request.method == 'POST':
        form = await request.form()
        user = form.get("user")
        passwd = form.get("password")
        user_id = database.sql_execute(f"SELECT id FROM users WHERE username='{user}' AND password='{passwd}';")
        # CASO NÃO HOUVER NENUHM USUÁRIO CADASTRADO
        if len(user_id) == 0:
            # CRIAR UMA MENSAGEM DE ALERTA AQUI
            return PlainTextResponse('Nenhum Usuário encontrado')
        # CASO HOUVER UM USUÁRIO CADASTRADO
        else:
            ip = request.client.host
            # verifica se o ip está cadastrado
            if f"database.sql_execute(f'SELECT ip FROM ip_user WHERE users_id={int(user_id[0][0])}')" != ip:
                # cadastra o ip na tabela e relaciona o usuario a ele.
                database.sql_execute(f"INSERT INTO ip_user VALUES (DEFAULT, '{ip}', {user_id[0][0]});")
            return HTMLResponse(f'<script>window.location.replace("http://{host_ip}:5000/blog");</script>')
    elif request.method == 'GET':
        return templates.TemplateResponse('login.html', {
            'request': request
        })


async def register_page(request):
    if request.method == 'POST':
        form = await request.form()
        user = User()
        erros = [
            user.set_username(form['username']),
            user.set_email(form['email']),
            user.set_name(form['name']),
            user.set_lastname(form['lastname']),
            user.set_password([form['password'], form['passwordconfirmation']])
        ]

        txt_erros = ''
        for erro in erros:
            if erro != None:
                txt_erros += f'{erro}\n'

        if txt_erros == '':
            db_erro = user.upload_to_database()
            if db_erro == None:
                return HTMLResponse(f'<script>window.location.replace("http://{host_ip}:5000/login");</script>')
        else:
            return PlainTextResponse(f'{txt_erros}')

    elif request.method == 'GET':
        return templates.TemplateResponse('register.html', {
            'request': request
        })


def logout_function(request):
    database.sql_execute(f"DELETE FROM ip_user WHERE ip='{request.client.host}';")
    return HTMLResponse(f'<script>window.location.replace("http://{host_ip}:5000/blog");</script>')

