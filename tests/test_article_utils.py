# coding=utf-8
from __future__ import unicode_literals

import textwrap
import unittest

from opvoeden_api import article_utils


EXAMPLE_TEXT = '''
<h2>{Jgz}</h2>

<p>{Het jgz} is onderdeel van de Jeugdgezondheidszorg. Veel {jgzs} organiseren bijeenkomsten.
Je kunt altijd bij een van {de jgzs} terecht. Neem daarvoor contact op met {het jgz} bij jou in de buurt.</p>

<p>Only specific strings between {accolades} are placeholders.</p>
'''


class TextReplacePlaceholders(unittest.TestCase):
    def test_default_replacements(self):
        expected = textwrap.dedent('''
            <h2>Centrum voor Jeugd en Gezin (CJG)</h2>

            <p>Het Centrum voor Jeugd en Gezin (CJG) is onderdeel van de Jeugdgezondheidszorg. Veel CJG’s organiseren bijeenkomsten.
            Je kunt altijd bij een van de CJG’s terecht. Neem daarvoor contact op met het Centrum voor Jeugd en Gezin (CJG) bij jou in de buurt.</p>

            <p>Only specific strings between {accolades} are placeholders.</p>
            ''')
        self.assertEqual(expected, article_utils.replace_placeholders(EXAMPLE_TEXT))

    def test_substitutions_override(self):
        expected = textwrap.dedent('''
            <h2>CJG</h2>

            <p>Het CJG is onderdeel van de Jeugdgezondheidszorg. Veel centra organiseren bijeenkomsten.
            Je kunt altijd bij een van de centra terecht. Neem daarvoor contact op met het CJG bij jou in de buurt.</p>

            <p>Only specific strings between {accolades} are placeholders.</p>
            ''')
        self.assertEqual(expected, article_utils.replace_placeholders(EXAMPLE_TEXT, substitutions={
            'Jgz': 'CJG',
            'het jgz': 'het CJG',
            'Het jgz': 'Het CJG',
            'jgzs': 'centra',
            'de jgzs': 'de centra'
        }))
