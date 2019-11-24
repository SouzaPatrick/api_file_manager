import os
import sys
from datetime import datetime

from app import app, db

#Classes
from integrations.user import User
from integrations.bucket import Bucket
from integrations.file import File

def clear_screen():
	os.system('clear')

def stop(message):
	print("Stop: ^^^^^^^^^^^   {}   ^^^^^^^^^^".format(message))
	sys.exit()

def create_db():
	db.drop_all()
	db.create_all()

def date_time_today():
	data_e_hora_atuais = datetime.now()
	return data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')

def message(dicResult):
	for chave in dicResult:
		for result in dicResult[chave]:
			if result[0]:
				print('[{}] {} - {} -> OK'.format(result[1], chave, result[2]))
			else:
				print('[{}] {} - {} -> ERRO'.format(result[1], chave, result[2]))
			

class UserTest:
	username = 'Patrick Felipe de Souza' #Nome completo do usuário
	usercpf = '111.111.111-11'
	email = 'souza.felipe.patrick@gmail.com'
	password_hash = '123'
	# last_seen = db.Column(db.DateTime)
	# first_seen = db.Column(db.DateTime)
 
	def get_all(self):
		_users = User.get_all()
		if _users != []:
			result = True
		else:
			result = False
		
		return result, date_time_today(), 'get_all()'

	def insert(self):
		data = {'username': self.username, 'usercpf': self.usercpf,
					'email': self.email, 'password_hash': self.password_hash}

		_user = User.insert(data, db)

		if _user != "":
			result = True
		else:
			result = False

		return result, date_time_today(), 'insert()'

	def insert_2(self):
		data = {'username': 'Wanderson Santana', 'usercpf': '222.222.222-22',
					'email': 'wallafisic@gmail.com ', 'password_hash': self.password_hash}

		_user = User.insert(data, db)

		if _user != "":
			result = True
		else:
			result = False

		return result, date_time_today(), 'insert_user_2()'

	def get(self, id):
		_user = User.get(id)
		if _user != "":
			result = True
		else:
			result = False

		return result, date_time_today(), 'get()'

	def delete(self, id):
		_user = User.delete(id, db)
		if _user != "":
			result = True
		else:
			result = False

		return result, date_time_today(), 'delete()'


class BucketTest:
	# name = 'Patrick Felipe de Souza'  # Nome completo do usuário
	creation_date = datetime.now()

	def get_all(self):
		_bucket = Bucket.get_all()
		if _bucket != []:
			result = True
		else:
			result = False

		return result, date_time_today(), 'get_all()'

	def insert(self, _user):
		data = {'name': _user.usercpf, 'creation_date': self.creation_date,
				'_user': _user}

		_bucket = Bucket.insert(data, db)

		if _bucket != "":
			result = True
		else:
			result = False

		return result, date_time_today(), 'insert()'

	def get(self, id):
		_bucket = Bucket.get_for_id(id)
		if _bucket != "":
			result = True
		else:
			result = False

		return result, date_time_today(), 'get()'


class FileTest:
	name = "arquivo1"
	path = '/bucket/url'
	size = '123'
	expiration_date = datetime.now()

	def insert(self, extension, _user, _bucket):
		data = {'name': self.name, 'path': self.path,'extension': extension,
				'size': self.size, 'expiration_date': self.expiration_date, '_user': _user, '_bucket': _bucket}

		_file = File().insert(data, db)

		if _file != "":
			result = True
		else:
			result = False

		return result, date_time_today(), 'insert()'


	def get_all(self):
		_file = File().get_all()
		if _file != []:
			result = True
		else:
			result = False

		return result, date_time_today(), 'get_all()'


	def get(self, id):
		_file = File().get_for_id(id)
		if _file != []:
			result = True
		else:
			result = False

		return result, date_time_today(), 'get()'



create_db() #Criação das tabelas

dicResult = {} #Cria um dicionário que irá conter todos os resultados dos testes
listResult = []

#Teste com User
_userTest = UserTest()
listResult.append(_userTest.insert())
listResult.append(_userTest.insert_2())
listResult.append(_userTest.get_all())
listResult.append(_userTest.get(id=1))

dicResult['User'] = listResult
listResult = []

#Teste com Bucket
_bucketTeste = BucketTest()
listResult.append(_bucketTeste.insert(_user=User.get(1)))
listResult.append(_bucketTeste.insert(_user=User.get(2)))
listResult.append(_bucketTeste.get_all())
listResult.append(_bucketTeste.get(id=1))

dicResult['Bucket'] = listResult
listResult = []

#Teste com File
_fileTest = FileTest()
listResult.append(_fileTest.insert('txt', _user=User.get(1),
								   _bucket=Bucket.get_for_name(User.get(1).usercpf)))
listResult.append(_fileTest.get_all())
listResult.append(_fileTest.get(id=1))

dicResult['File'] = listResult
listResult = []





clear_screen()

message(dicResult)
