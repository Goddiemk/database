import json
import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite://')
Base = declarative_base()


class Population(Base):
    __tablename__ = 'population'
    locationcode = Column(String(20), primary_key=True)
    popno = Column(Integer)

    def __repr__(self):
        return "<Population(locationcode={}, popno={})>".format(
            self.locationcode, self.popno)


Base.metadata.create_all(engine)

url = requests.get(
    'https://raw.githubusercontent.com/Electroscope/electroscope-api/master/mongo/population.json'
)
uploads_json = json.loads(url.content)
uploads = []
for result in uploads_json:
    row = {}
    row['locationcode'] = result['location_code']
    row['popno'] = result['population']
    uploads.append(row)

Session = sessionmaker(bind=engine)
session = Session()
for upload in uploads:
    row = Population(**upload)
    session.add(row)
session.commit()
for instance in session.query(Population):
    print(instance.popno, instance.locationcode)
