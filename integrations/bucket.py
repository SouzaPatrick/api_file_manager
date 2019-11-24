#!/usr/bin/python
# -*- coding: utf-8 -*-

from models.tables import Bucket as BucketTable


class Bucket:
    def insert(data, db):
        # Cria uma instância da classe User utilizando os dados do post
        _bucket = BucketTable(name=data['name'], creation_date=data['creation_date'], user=data['_user'])

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        db.session.add(_bucket)  # Adiciona os dados no banco
        db.session.commit()  # Serve para o salvamento de informações

        return _bucket

    # Faz um select no banco e obtem os dados de todos os usuários cadastrados no sistema
    def get_all():
        _bucket = BucketTable.query.all()  # Criar uma instância da classe

        return _bucket

    # Faz um select no banco e obtem os dados de todos os usuários cadastrados no sistema
    def get_for_name(name):
        _bucket = BucketTable.query.filter_by(name=name).first()  # Criar uma instância da classe

        return _bucket

    def get_for_id(id):
        _bucket = BucketTable.query.get(id)

        return _bucket

    def delete(id, db):
        _bucket = BucketTable.query.filter_by(id=id).first()

        # Enquanto um usuário tiver usando minha aplicação ele usa essa sessão
        db.session.delete(_bucket)  # Adiciona os dados no banco
        db.session.commit()  # Serve para o salvamento de informações

        return _bucket




