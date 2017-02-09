from __future__ import unicode_literals

from urlparse import urljoin

import requests

from . import models

BASE_URL = 'https://api.stichtingopvoeden.nl/rest/v1/'


class Client(object):
    def __init__(self, api_key, base_url=None, session=None):
        self.base_url = base_url or BASE_URL
        self.session = session or requests.Session()
        self.session.headers['Authorization'] = api_key

    def get(self, path, object_hook=None):
        response = self.session.get(urljoin(self.base_url, path))
        response.raise_for_status()
        return response.json(object_hook=object_hook)

    def contentset(self, contentset_id=None):
        if contentset_id is None:
            url = 'contentset'
            object_hook = models.ContentSet.from_dict
        else:
            url = 'contentset/{}'.format(contentset_id)
            object_hook = models.Article.from_dict
        return self.get(url, object_hook=object_hook)

    def article(self, external_reference):
        url = 'article/{}'.format(external_reference)
        object_hook = models.Article.from_dict
        return self.get(url, object_hook=object_hook)

    def image(self, image_id):
        url = 'image/{}'.format(image_id)
        object_hook = models.Image.from_dict
        return self.get(url, object_hook=object_hook)
