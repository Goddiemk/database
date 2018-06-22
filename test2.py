import json
import requests
from datetime import datetime, timedelta
from random import randint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite://')

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    UserId = Column(Integer, primary_key=True)
    Title = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    Email = Column(String)
    Username = Column(String)


class Uploads(Base):
    __tablename__ = "uploads"
    UploadId = Column(Integer, primary_key=True)
    UserId = Column(Integer)
    Title = Column(String)
    Body = Column(String)
    Timestamp = Column(DateTime)


Base.metadata.create_all(engine)

url = 'https://randomuser.me/api/?results=10'
users_json = requests.get(url).json()
url2 = requests.get('https://jsonplaceholder.typicode.com/posts/')
uploads_json = json.loads(url2.content)

users, uploads = [], []
for i, result in enumerate(users_json['results']):
    row = {}
    row['UserId'] = i
    row['Title'] = result['name']['title']
    row['FirstName'] = result['name']['first']
    row['LastName'] = result['name']['last']
    row['Email'] = result['email']
    row['Username'] = result['login']['username']

    users.append(row)
for result in uploads_json:
    row = {}
    row['UploadId'] = result['id']
    row['UserId'] = result['userId']
    row['Title'] = result['title']
    row['Body'] = result['body']
    #delta = timedelta(seconds=randint(1, 86400))
    #row['Timestamp'] = datetime.now() - delta
    uploads.append(row)

Session = sessionmaker(bind=engine)
session = Session()
for user in users:
    row = Users(**user)
    session.add(row)
for upload in uploads:
    row = Uploads(**upload)
    session.add(row)
session.commit()
for instance in session.query(Uploads):
    print(instance.Body)