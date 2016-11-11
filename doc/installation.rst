..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _installation:

************
Installation
************

.. highlight:: bash

Installing Clique is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install clique

If the Cheeseshop (a.k.a. PyPI) is down, you can also install Clique from one
of the mirrors::

    $ pip install --use-mirrors clique

Alternatively, you may wish to download manually from Gitlab where Clique
is `actively developed <https://gitlab.com/4degrees/clique>`_.

You can clone the public repository::

    $ git clone git@gitlab.com:4degrees/clique.git

Or download an appropriate
`zipball
<https://gitlab.com/4degrees/clique/repository/archive.zip?ref=master>`_

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages::

    $ python setup.py install

Dependencies
============

* `Python <http://python.org>`_ >= 2.6, < 3

For testing:

* `Pytest <http://pytest.org>`_  >= 2.3.5
