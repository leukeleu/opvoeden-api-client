from __future__ import unicode_literals

from datetime import datetime

DATE_FORMAT = '%Y%m%d'


class ContentSet(object):
    def __init__(self, contentset_id=None, name=None, description=None, is_default=None):
        self.contentset_id = contentset_id
        self.name = name
        self.description = description
        self.is_default = is_default

    @classmethod
    def from_dict(cls, data):
        return cls(
            contentset_id=data['id'],
            name=data['name'],
            description=data['description'],
            is_default=bool(data['isDefault']))

    def __repr__(self):
        return (
            '{name}(contentset_id={self.contentset_id!r},'
            ' name={self.name!r}, description=...,'
            ' is_default={self.is_default!r})'
        ).format(name=self.__class__.__name__, self=self)


class Article(object):
    def __init__(self, external_reference, short_title, title, article_text,
                 parent_reference, position, last_change_date, canonicaltag):
        self.external_reference = external_reference
        self.short_title = short_title
        self.title = title
        self.article_text = article_text
        self.parent_reference = parent_reference
        self.position = position
        self.last_change_date = last_change_date
        self.canonicaltag = canonicaltag

    @classmethod
    def from_dict(cls, data):
        return cls(
            external_reference=data['externalReference'],
            short_title=data['shortTitle'],
            title=data['title'],
            article_text=data['articleText'],
            parent_reference=data['parentReference'],
            position=data['position'],
            last_change_date=datetime.strptime(data['lastChangeDate'], DATE_FORMAT).date(),
            canonicaltag=data['canonicaltag'])

    def __repr__(self):
        return (
            '{name}(external_reference={self.external_reference!r},'
            ' short_title={self.short_title!r}, title={self.title!r},'
            ' article_text=..., parent_reference={self.parent_reference!r},'
            ' position={self.position!r}, last_change_date=...,'
            ' canonicaltag=...)'
        ).format(name=self.__class__.__name__, self=self)


class Image(object):
    def __init__(self, image_id, data, content_type, name, creation_date):
        self.image_id = image_id
        self.data = data
        self.content_type = content_type
        self.name = name
        self.creation_date = creation_date

    @classmethod
    def from_dict(cls, data):
        return cls(
            image_id=data['imageID'],
            data=data['data'],
            content_type=data['type'],
            name=data['name'],
            creation_date=datetime.strptime(data['creationDate'], DATE_FORMAT).date())

    def __repr__(self):
        return (
            '{name}(image_id={self.image_id!r}, data=...,'
            ' content_type={self.content_type!r},'
            ' name={self.name!r}, creation_date=...)'
        ).format(name=self.__class__.__name__, self=self)