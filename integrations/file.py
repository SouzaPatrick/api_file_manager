#!/usr/bin/python
# -*- coding: utf-8 -*-

from models.tables import File as FileTable
from datetime import datetime

class File:
    def insert(self, data, db):
        # Cria uma instância da classe User utilizando os dados do post
        insertion_date = datetime.now()

        _file = FileTable(
            name=data['name'], path=data['path'], size=data['size'], insertion_date=insertion_date,
            extension=data['extension'], expiration_date=data['expiration_date'], user=data['_user'],
            bucket=data['_bucket'])

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        db.session.add(_file)  # Adiciona os dados no banco
        db.session.commit()  # Serve para o salvamento de informações

        return _file

    # Faz um select no banco e obtem os dados de todos os usuários cadastrados no sistema
    def get_all(self):
        _file = FileTable.query.order_by(FileTable.name).all()  # Criar uma instância da classe

        return _file

    def get_for_id(self,id):
        _file = FileTable.query.filter_by(id=id).first()

        return _file

    def delete(self, id, db):
        _file = self.get_for_id(id)

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        db.session.delete(_file)  # Adiciona os dados no banco
        db.session.commit()  # Serve para o salvamento de informações

        return _file

