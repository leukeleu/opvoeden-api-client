from __future__ import unicode_literals

import datetime
import unittest

from opvoeden_api import models


class TestModelRepr(unittest.TestCase):
    def test_contentset(self):
        obj = models.ContentSet(
            contentset_id=1, name='Example',
            description='Example description', is_default=False)
        self.assertRegexpMatches(
            repr(obj),
            r"^ContentSet\(contentset_id=1, name=u?'Example', description=..., is_default=False\)$")

    def test_article(self):
        obj = models.Article(
            external_reference=1, short_title='Example', title='Example article',
            article_text='Example description', parent_reference='', position=1,
            last_change_date=datetime.date.today(), canonicaltag='https://example.com/article')
        self.assertRegexpMatches(
            repr(obj),
            r"^Article\(external_reference=1, short_title=u?'Example',"
            r" title=u?'Example article', article_text=...,"
            r" parent_reference=u?'', position=1,"
            r" last_change_date=..., canonicaltag=...\)$")

    def test_image(self):
        obj = models.Image(
            image_id=1, data='R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=',
            content_type='image/gif', name='pixel.gif', creation_date=datetime.date.today())
        self.assertRegexpMatches(
            repr(obj),
            r"^Image\(image_id=1, data=..., content_type=u?'image/gif',"
            r" name=u?'pixel.gif', creation_date=...\)$")
