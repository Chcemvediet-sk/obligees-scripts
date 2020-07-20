# coding: utf-8
from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, SMALLINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Obligee(Base):
    __tablename__ = 'obligees_obligee'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    street = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    city = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    zip = Column(String(10, 'utf8_unicode_ci'), nullable=False)
    emails = Column(String(1024, 'utf8_unicode_ci'), nullable=False)
    slug = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    status = Column(SMALLINT(6), nullable=False)
    gender = Column(SMALLINT(6), nullable=False)
    ico = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    name_accusative = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_dative = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_genitive = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_instrumental = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_locative = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    notes = Column(LONGTEXT, nullable=False)
    official_description = Column(LONGTEXT, nullable=False)
    official_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    simple_description = Column(LONGTEXT, nullable=False)
    type = Column(SMALLINT(6), nullable=False)
    latitude = Column(Float(asdecimal=True))
    longitude = Column(Float(asdecimal=True))
    iczsj_id = Column(String(32, 'utf8_unicode_ci'), nullable=False, index=True)


class NewObligee(Base):
    __tablename__ = 'obligees_obligee_nove_obce'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    street = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    city = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    zip = Column(String(10, 'utf8_unicode_ci'), nullable=False)
    emails = Column(String(1024, 'utf8_unicode_ci'), nullable=False)
    slug = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    status = Column(SMALLINT(6), nullable=False)
    gender = Column(SMALLINT(6), nullable=False)
    ico = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    name_accusative = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_dative = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_genitive = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_instrumental = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_locative = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    notes = Column(LONGTEXT, nullable=False)
    official_description = Column(LONGTEXT, nullable=False)
    official_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    simple_description = Column(LONGTEXT, nullable=False)
    type = Column(SMALLINT(6), nullable=False)
    latitude = Column(Float(asdecimal=True))
    longitude = Column(Float(asdecimal=True))
    iczsj_id = Column(String(32, 'utf8_unicode_ci'), nullable=False, index=True)


class Webpage(Base):
    __tablename__ = 'obligees_webpage'

    obligee_id = Column(ForeignKey('obligees_obligee.id'), nullable=False, index=True)
    webpage = Column(LONGTEXT)
    id = Column(INTEGER(11), primary_key=True)

    obligee = relationship('Obligee')


class ZipCodes(Base):
    __tablename__ = 'obligees_zipcodes'

    obligee_id = Column(ForeignKey('obligees_obligee.id'), nullable=False, index=True)
    json_zip = Column(String(6, 'utf8_unicode_ci'), nullable=False)
    post_json_zip = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    post_obligee_zip = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    id = Column(INTEGER(11), primary_key=True)

    obligee = relationship('Obligee')
