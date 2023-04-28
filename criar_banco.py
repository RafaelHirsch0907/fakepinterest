from fakepinterest import dataBase, app
from fakepinterest.models import User, Photo

with app.app_context():
    dataBase.create_all()