# CIRAR ESTRUTURA DO BANCO DE DADOS

from fakepinterest import dataBase
from datetime import datetime

class User(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    userName = dataBase.Column(dataBase.String, nullable=False)
    email = dataBase.Column(dataBase.String, nullable=False, unique=True)
    password = dataBase.Column(dataBase.String, nullable=False)
    photos = dataBase.relationship("Photo", backref="user", lazy=True)
    

class Photo(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    image = dataBase.Column(dataBase.String, default="default.png")
    createDate = dataBase.Column(dataBase.DateTime, nullable=False, default=datetime.utcnow())
    userId = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('user.id'), nullable=False)