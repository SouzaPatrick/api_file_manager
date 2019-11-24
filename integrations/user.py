#!/usr/bin/python
# -*- coding: utf-8 -*-

from models.tables import User as UserTable


class User:
    def insert(data, db):
        # Cria uma instância da classe User utilizando os dados do post
        _user = UserTable(username=data['username'], usercpf=data['usercpf'], email=data['email'],
                          password_hash=data['password_hash'])

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        db.session.add(_user)  # Adiciona os dados no banco
        db.session.commit()  # Serve para o salvamento de informações

        return _user

    # Faz um select no banco e obtem os dados de todos os usuários cadastrados no sistema
    def get_all():
        _user = UserTable.query.all()  # Criar uma instância da classe

        return _user

    def get(id):
        _user = UserTable.query.filter_by(id=id).first()

        return _user

    def delete(id, db):
        _user = UserTable.query.filter_by(id=id).first()

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        db.session.delete(_user)  # Adiciona os dados no banco
        db.session.commit()  # Serve para o salvamento de informações

        return _user

    def user_by_usercpf(self, usercpf):

        try:
            return UserTable.query.filter(UserTable.usercpf == usercpf).first()
        except:
            return None

    def user_by_id(self, id):
        try:
            return UserTable.query.get(id)
        except:
            return None

    def check_password(self, passwordPost, passwordUser):
        if passwordPost == passwordUser:
            return True
        else:
            return False




