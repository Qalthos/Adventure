# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode

from adventure.model import DeclarativeBase, metadata, DBSession


class Link(DeclarativeBase):
    __tablename__ = 'link'

    #{ Columns
    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    direction = Column(Unicode(255), nullable=False)
    new_card_id = Column(Integer, ForeignKey('card.id'))
    #}


class Card(DeclarativeBase):
    __tablename__ = 'card'

    #{ Columns
    id = Column(Integer, primary_key=True)
    description = Column(Unicode(255), nullable=False)
    special = Column(Unicode(255), unique=True)
    #}

    links = relation('Card', secondary=Link.__table__, primaryjoin=id==Link.card_id,
            secondaryjoin=id==Link.new_card_id, backref='backlinks')
