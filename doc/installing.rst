..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _installing:

**********
Installing
**********

.. highlight:: bash

.. note::

    Using :term:`Virtualenv` is recommended when evaluating or running locally.

Installation is simple with :term:`pip`::

    pip install clique

Installing from source
======================

You can also build and install manually from the source for more control.

First obtain a copy of the source by either `downloading
<https://gitlab.com/4degrees/clique/repository/archive.zip?ref=master>`_ or
cloning the public repository::

    git clone git@gitlab.com:4degrees/clique.git

Then build and install the package into your current Python environment::

    pip install .

If actively developing, perform an :ref:`editable <pip:editable-installs>`
install instead. This will link the installed package to the project source
reflecting any local changes made::

    pip install -e .

.. note::

    To also enable building documentation and running tests from source, use the
    following command to ensure that the relevant 'extra' packages are
    installed::

        pip install -e ".[dev]"

Alternatively, just build locally and manage yourself::

    python setup.py build

Building documentation from source
----------------------------------

Ensure the 'extra' packages required for building the documentation are
installed::

    pip install -e ".[doc]"

Then build the documentation::

    python setup.py build_sphinx

View the result in your browser::

    file:///path/to/clique/build/doc/html/index.html

Running tests against the source
--------------------------------

Ensure the 'extra' packages required for running the tests are installed::

    pip install -e ".[test]"

Then run the tests as follows::

    python setup.py -q test

A coverage report can also be generated when running tests::

    python setup.py -q test --addopts "--cov --cov-report=html"

View the generated report at::

    file:///path/to/clique/htmlcov/index.html
