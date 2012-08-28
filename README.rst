******************
cmsplugin-footnote
******************

A simple plugin allowing to add footnotes in django CMS.

.. contents::
   :depth: 3



Requirements
============

* `Django <https://www.djangoproject.com/>`_ (tested with 1.4)
* `django-CMS <https://www.django-cms.org/>`_ (tested with 2.3)



Installation
============

#. ``[sudo] pip install cmsplugin-footnote``
#. Add ``'cmsplugin_footnote',`` to your ``INSTALLED_APPS``
#. ``./manage.py syncdb``
#. ``./manage.py collectstatic``
#. Add ``{% load footnote %}`` and one or several
   ``{% footnote_list 'placeholder_name' %}`` to your CMS template(s).



Translations
============

Status
------

.. image::
   https://www.transifex.com/projects/p/cmsplugin-footnote/resource/core/chart/image_png

Write your translation
----------------------

Localization is done directly on
`our Transifex page <https://www.transifex.com/projects/p/cmsplugin-footnote/>`_.
There is no access restriction, so feel free to spend two minutes translating
cmsplugin-footnote to your language :o)


Get & Compile
-------------

#. Make sure you have
   `transifex-client <http://pypi.python.org/pypi/transifex-client/>`_
   installed: ``[sudo] pip install transifex-client``
#. Pull all translations from Transifex: ``tx pull -a``
#. Compile them: ``cd cmsplugin_footnote && django-admin.py compilemessages``
