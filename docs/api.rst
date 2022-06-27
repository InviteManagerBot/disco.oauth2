.. currentmodule:: disco_oauth2

API Reference
==============
The following section outlines the API of disco_oauth2.

.. note::

    This module uses the Python logging module to log diagnostic and errors
    in an output independent way.  If the logging module is not configured,
    these logs will not be output anywhere.

.. toctree::
   :maxdepth: 4

Client
~~~~~~~

.. autoclass:: Client
    :members:

AccessToken
~~~~~~~~~~~

.. autoclass:: AccessToken()
    :members:

Discord Models
--------------
User
~~~~

.. autoclass:: User()
    :members:

Guild
~~~~~~~~

.. autoclass:: Guild()
    :members:

Member
~~~~~~~~

.. autoclass:: Member()
    :members:

Connection
~~~~~~~~~~

.. autoclass:: Connection()
    :members:

Integrations
------------

.. autoclass:: ServerIntegration()
    :members:

.. autoclass:: IntegrationAccount()
    :members:

.. autoclass:: ExpireBehavior()
    :members:

.. autoclass:: IntegrationApp()
    :members:

.. autoclass:: ExpireBehavior()
    :members:

Flags
------
Permissions
~~~~~~~~~~~~

.. autoclass:: Permissions
    :members:

UserFlags
~~~~~~~~~~~~

.. autoclass:: UserFlags
    :members:
