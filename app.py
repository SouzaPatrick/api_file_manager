#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_extension, file_type_magic
from resources import get_bucket, get_buckets_list
from flask_sqlalchemy import SQLAlchemy #Importação da ORI (Estrutura que facilita a comunicação da linguagem com o banco, sem usar sql)
from flask_migrate import Migrate

#Login
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.utils import secure_filename #Ipede que o arquivo seja adicionad em outra pasta seão esta do projeto
import os
from datetime import datetime

#Main
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)

#Jinja
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type_magic

#SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///storege.db" #Configuração de coneção com o banco
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Integrations
# from .integrations.bucket import Bucket
from integrations.file import File
from integrations.bucket import Bucket
from integrations.user import User



#Login
lm = LoginManager(app)
lm.init_app(app)

@lm.user_loader
def load_user(id):
    return User().user_by_id(id)

@lm.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

# Obter dados dos cursos (Marcos)
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', titulo="Gestor de Arquivos")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Auetnticar usuário
@app.route('/api/auth', methods=['POST'])
def authenticate():
    user = User()
    _user = user.user_by_usercpf(request.form['usercpf'])  # Caso encontre o usuário, retorna

    # Caso o usuáro seja encontrado
    if _user != None:
        resultPassaword = user.check_password(
            request.form['password'], _user.password_hash)
        # Caso o usuáro seja encontrado
        if resultPassaword:
            login_user(_user)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        _bucket = Bucket.get_for_name(current_user.bucket[0].name)


        return render_template("index.html", bucket=_bucket)


@app.route('/files')
@login_required
def files():
    # my_bucket = get_bucket()
    # summaries = my_bucket.objects.all()
    _bucket = Bucket.get_for_name(name=current_user.bucket[0].name) #Saber o usuário que está logado no momento
    files = _bucket.files

    return render_template('files.html', my_bucket=_bucket, files=files)


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('files'))

    file = request.files['file']


    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('files'))

    fileExtension = get_file_extension(file)

    if file and fileExtension != '':
        # filename = secure_filename(file.filename)
        result = insert_db(file, fileExtension)

        if result:
            '''
            file = request.files['file']
        
            my_bucket = get_bucket()
            my_bucket.Object(file.filename).put(Body=file)
        
            
            '''
            flash('File uploaded successfully')
        else:
            flash('Error uploading file')
    else:
        flash('Invalid file extension')

    return redirect(url_for('files'))

def insert_db(file, fileExtension):
    dataFile = {'name':  os.path.splitext(file.filename)[0], 'path': file.filename,
                'insertion_date': datetime.now(), 'size': get_size(file), 'extension':  fileExtension,
                'expiration_date': datetime.now(), '_bucket': Bucket.get_for_name(name=current_user.bucket[0].name),
                '_user': User.get(id=current_user.id)}

    _file = File().insert(data=dataFile, db=db)

    if _file:
        return True

    return False

def get_file_extension(file):
    # fileType = file_type_magic(file, get_size(file))

    fileExtension = file_extension(file, get_size(file))

    return fileExtension

def get_size(file):
    if file.content_length:
        return file.content_length
    try:
        pos = file.tell()
        file.seek(0, 2)  #seek to end
        size = file.tell()
        file.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    _file = File().delete(id=request.form['id'], db=db)
    '''
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    
    '''
    flash('File deleted successfully')
    return redirect(url_for('files'))



@app.route('/download', methods=['POST'])
@login_required
def download():
    key = request.form['key']

    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == "__main__":
    app.run()
