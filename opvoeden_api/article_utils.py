# coding=utf-8
from __future__ import unicode_literals

import re

PLACEHOLDER_MATCHER = re.compile('{((?:[Jj]gzs?)|(?:[Dd]e jgzs)|(?:[Hh]et jgz))}')
SUBSTITUTION_DEFAULTS = {
    'jgz': 'centrum voor Jeugd en Gezin (CJG)',
    'Jgz': 'Centrum voor Jeugd en Gezin (CJG)',
    'jgzs': 'CJG’s',
    'Jgzs': 'CJG’s',
    'de jgzs': 'de CJG’s',
    'De jgzs': 'De CJG’s',
    'het jgz': 'het Centrum voor Jeugd en Gezin (CJG)',
    'Het jgz': 'Het Centrum voor Jeugd en Gezin (CJG)'
}


def replace_placeholders(article_text, substitutions=None):
    """
    Replace all JGZ placeholders in the article text with the
    appropriate strings.

    Use the optional ``substitutions`` argument to override
    any of the default substitution strings.

    """
    substitutions = substitutions or {}

    def replace(match):
        return substitutions.get(match.group(1), SUBSTITUTION_DEFAULTS.get(match.group(1)))

    return PLACEHOLDER_MATCHER.sub(replace, article_text)


ANCHOR_MATCHER = re.compile('\[a=([0-9]+),(.+?)\]')


def replace_links(article_text, replacement_function):
    """
    Replace all internal links in the article text
    with the return value of ``replacement_function``.

    If ``replacement_function`` returns ``None``
    no substitution will take place.

    """
    def replace(match):
        external_id = match.group(1)
        link_text = match.group(2)
        replacement = replacement_function(external_id, link_text)
        return match.group(0) if replacement is None else replacement

    return ANCHOR_MATCHER.sub(replace, article_text)
