#!/usr/bin/env python
# encoding: utf-8

from peewee import (MySQLDatabase, Model, ForeignKeyField,
                    TextField, BigIntegerField, DateTimeField)

import settings


database = MySQLDatabase(settings.DATABASE,
                         user=settings.USER,
                         password=settings.PASSWORD)
database.connect()


class BaseModel(Model):
    class Meta:
        database = database


class Category(BaseModel):
    name = TextField()


class Torrent(BaseModel):
    category = ForeignKeyField(Category)
    title = TextField()
    size = BigIntegerField()
    magnet = TextField()
    hash = TextField()
    nfo = TextField()
    created = DateTimeField()


class Removed(BaseModel):
    pass


if __name__ == '__main__':
    database.create_tables([Removed])
