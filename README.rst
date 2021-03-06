#############################
Stichting Opvoeden API client
#############################

A client for the `stichtingopvoeden.nl`_ `API version 2`_.


Usage
=====

Import the client class from ``opvoeden_api.client`` and instantiate
it with an API key::

    client = Client(MY_API_KEY)

The client methods map to the following set of endpoints:

===============================  =======================================
Method                           Endpoint
===============================  =======================================
``contentset_list``              `/rest/v2/contentset`_
``contentset(contentset_id)``    `/rest/v2/contentset/{id}`_
``article(external_reference)``  `/rest/v2/article/{externalReference}`_
``image(image_id)``              `/rest/v2/image/{id}`_
===============================  =======================================

.. note:: The ``contentset`` method does not support the ``changedAfter``
    or ``article`` parameters that are documented in the API docs.


Data types
==========

Each client method returns a different data type.


``ContentSet``
--------------

The ``contentset_list`` method returns a ``list`` of
``ContentSet`` objects.

A ``ContentSet`` object has of the following properties:

* ``contentset_id``
* ``name``
* ``description``
* ``is_default``

Refer to the `API data types docs`_ for more information on
these fields.


``ArticleNode``
---------------

The ``contentset(contentset_id)`` method returns a single ``ArticleNode``.
This node represents the root of a tree of ``Articles``.

An ``ArticleNode`` has the following properties:

``article``
    The ``Article`` instance associated with this node
``children``
    A ``list`` of ``ArticleNode`` instances of which the current node
    is the parent.

It is possible to iterate over an article node. This will traverse the
entire tree in a depth first order. So, for example, to get a flat list
of all the articles in a tree one could do this::

    tree = client.contentset(1)
    articles = [node.article for node in tree if node.article]


To recurse over the tree use the children property::

    def visit(node, parent=None):
        """
        Visit each node in the tree.
        """
        # do something with node, then recurse
        for child in node.children:
            visit(child, node)

    tree = client.contentset(1)
    visit(tree)


``Article``
-----------

The ``article(external_reference)`` method returns a single ``Article``
instance. Another way to get an ``Article`` object is by accessing
the ``article`` property of an ``ArticleNode``.

An ``Article`` has the following properties:

* ``external_reference``
* ``short_title``
* ``title``
* ``article_text``
* ``parent_reference``
* ``position``
* ``last_change_date``
* ``canonicaltag``
* ``tags``

Refer to the `API data types docs`_ for more information on
these fields.

.. note:: The ``article_text`` of ``Articles`` retrieved from the
    ``contentset`` endpoint can contain several placeholder strings.
    This library provides a number of `utilities`__
    to deal with those.

In addition to these fields the ``Article`` object also
provides these properties:

``path``
    The url of the article. This is identical to the ``canonicaltag``
    but the ``schema://domain`` prefix is stripped.
``slug``
    The last element of the path. i.e. if ``path`` is ``'/foo/bar/'``
    then ``slug`` will be ``'bar'``.

``Image``
---------

The ``image(image_id)`` method returns a single ``Image``
instance.

* ``image_id``
* ``data``
* ``content_type``
* ``name``
* ``creation_date``

Refer to the `API data types docs`_ for more information on
these fields.

Converting image data to binary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Image`` object also provides an ``as_binary`` method.

This method converts to base64 encoded value of the ``data``
property to binary. The return value of this method can be used
to store images on a file system.

__

Article utils
=============

The ``article_text`` of ``Articles`` returned by the ``contentset``
method can contain a number special placeholder strings.

``opvoeden_api.article_utils`` provides functions to deal with
these placeholders.


Replace JGZ placeholders
------------------------

To replace `JGZ placeholders`_ with appropriate strings use
``replace_jgz``.

By default these are the substitutions:

===========  =====================================
Placeholder  Substitution
===========  =====================================
jgz          centrum voor Jeugd en Gezin (CJG)
Jgz          Centrum voor Jeugd en Gezin (CJG)
jgzs         CJG’s
Jgzs         CJG’s
de jgzs      de CJG’s
De jgzs      De CJG’s
het jgz      het Centrum voor Jeugd en Gezin (CJG)
Het jgz      Het Centrum voor Jeugd en Gezin (CJG)
===========  =====================================

To override any of the substitutions use the optional
``substitutions`` argument to ``replace_jgz`` i.e.::

    replace_jgz(article_text, substitutions={
        'jgz': 'centrum voor Jeugd en Gezin'
    })


Replace internal link placeholders
----------------------------------

To replace `internal link placeholders`_ use ``replace_links``
with a replacement callback.

The replacement callback is called with the ``external_id``
and ``link_text`` for each placeholder in the article text.

If the replacement callback returns anything other than ``None``
the link is replaced with the return value.

For example::

    external_id_to_href = {
        '1': '/example/',
        '2': '/example/more/'
    }

    def get_link(external_id, link_text):
        """
        Get the url for an article and return an HTML snippet
        that links to this url with the given text.

        """
        href = external_id_to_href.get(external_id, None)
        if href:
            return '<a href="{}">{}</a>'.format(href, link_text)

    replace_links(article_text, get_link)


Replace image placeholders
--------------------------

To replace `image placeholders`_ use ``replace_images``
with a replacement callback.

The replacement callback is called with the ``image_id``
for each placeholder in the article text.

If the replacement callback returns anything other than ``None``
the placeholder is replaced with the return value.

For example::

        image_id_to_src = {
            '1': '/media/1.gif',
            '2': '/media/2.gif'
        }

        def get_image_tag(image_id):
            src = image_id_to_src.get(image_id, None)
            if src:
                return '<img src="{}">'.format(src)


.. hint:: The replacement callback is an excellent place call the
    image endpoint of the API.


Replace video placeholders
--------------------------

To replace `YouTube video placeholders`_ use ``replace_videos``
with a replacement callback.

The replacement callback is called with the ``video_id``, ``embed_url``
and ``external_url`` for each placeholder in the article text.

If the replacement callback returns anything other than ``None``
the placeholder is replaced with the return value.

Some examples::

        def get_video_embed(video_id, embed_url, external_url):
            """Create an iframe to embed the video"""
            return '<iframe src="{}">'.format(embed_url)


        def get_video_link(video_id, embed_url, external_url):
            """Create a link to the video player on opvoeden.nl"""
            return '<a href="{}" target="_blank">Watch the video</a>'.format(
                external_url)


Changes
=======

v2.1.0
------

- Expose article tags

v2.0.1
------

- Fix YouTube url regex

v2.0.0
------

- Use API version 2

v1.0.0
------

- Initial release


.. _`stichtingopvoeden.nl`: https://stichtingopvoeden.nl/
.. _`API version 2`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/
.. _`/rest/v2/contentset`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/de-contentset-service/
.. _`/rest/v2/contentset/{id}`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/de-contentset-service/
.. _`/rest/v2/article/{externalReference}`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/de-article-service/
.. _`/rest/v2/image/{id}`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/de-image-service/
.. _`API data types docs`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/data-types/
.. _`JGZ placeholders`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/de-artikeltekst/
.. _`internal link placeholders`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/de-artikeltekst/
.. _`image placeholders`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/de-artikeltekst/
.. _`Youtube video placeholders`: https://documentatie.beheerportaalgemeenten.nl/rest-api/versie-2/youtube-video-s/
