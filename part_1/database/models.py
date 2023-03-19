import connect
from mongoengine import Document
from mongoengine.fields import StringField, DateField, ListField, ReferenceField


class Authors(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField(min_length=10)


class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors)
    quote = StringField()
