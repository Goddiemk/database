import json
import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite://')
Base = declarative_base()


class Population(Base):
    __tablename__ = 'population'
    id = Column(Integer, Sequence('population_id'), primary_key=True)
    locationcode = Column(String(20), ForeignKey('districts.code'))
    popno = Column(Integer)
    populate = relationship('Districts', back_populates='pcode')

    def __repr__(self):
        return "<Population(locationcode={}, popno={})>".format(
            self.locationcode, self.popno)


class Townships(Base):
    __tablename__ = 'townships'
    id = Column(Integer, Sequence('town_id'), primary_key=True)
    code = Column(String(20), ForeignKey('districts.code'))
    dtcode = Column(String(20), ForeignKey('districts.code'))
    name = Column(String(20), ForeignKey('districts.name'))
    towncode = relationship(
        'Districts', back_populates=('tcode'), foreign_keys=[code])
    towndtcode = relationship(
        'Districts', back_populates=('dcode'), foreign_keys=[code])
    townname = relationship(
        'Districts', back_populates=('tname'), foreign_keys=[name])

    def __repr__(self):
        return "<Townships(code={}, name={})>".format(self.code, self.name)


class Districts(Base):
    __tablename__ = 'districts'
    code = Column(String(20), primary_key=True)
    name = Column(String(20))

    def __repr__(self):
        return "<Districts(code={}, name={})>".format(self.code, self.name)


Districts.tcode = relationship(
    'Townships', back_populates='towncode', foreign_keys='Townships.code')
Districts.dcode = relationship(
    'Townships', back_populates='towndtcode', foreign_keys='Townships.dtcode')
Districts.tname = relationship(
    'Townships', back_populates='townname', foreign_keys='Townships.name')
Districts.pcode = relationship('Population', back_populates='populate')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

url = requests.get(
    'https://raw.githubusercontent.com/'
    'Electroscope/electroscope-api/master/mongo/population.json')
uploads_json = json.loads(url.content)
for result in uploads_json:
    population = Population(
        locationcode=result['location_code'], popno=result['population'])
    session.add(population)

url2 = requests.get(
    'https://raw.githubusercontent.com/Electroscope/electroscope-api/master/mongo/townships.json'
)
uploads_json2 = json.loads(url2.content)
for result in uploads_json2:
    townships = Townships(
        code=result['code'],
        dtcode=result['dt_code'],
        name=result['name']['en'])
    session.add(townships)

url3 = requests.get(
    'https://raw.githubusercontent.com/Electroscope/electroscope-api/master/mongo/districts.json'
)
uploads_json3 = json.loads(url3.content)
for result in uploads_json3:
    districts = Districts(code=result['code'], name=result['name']['en'])
    session.add(districts)

session.commit()

# test search query
for distinct, township in session.query(
        Districts,
        Townships).filter(Districts.code == Townships.dtcode).filter(
            Townships.name == 'Kyonpyaw').all():
    print(distinct)
    print(township)
gg