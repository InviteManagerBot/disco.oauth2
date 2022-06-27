.. disco.oauth2 documentation master file, created by
   sphinx-quickstart on Sun Jun 26 23:17:26 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================
Welcome to disco.oauth2
==================

An asynchronous discord OAuth2 API wrapper written in Python.

Key Features
-----------
- Modern Pythonic API using ``async``\/``await`` syntax.
- Easy to use with an object oriented design.
- Sane rate limit handling that prevents 429s.
- Optimised for both speed and memory

Library Installation
--------------------
.. code-block:: bash

   $ pip install disco.oauth2

Getting Started
---------------
Quick example
~~~~~~~~~~~~~~
.. code-block:: py

   from disco_oauth2 import Client

   client = Client(
      client_id=my_client_id_here,
      client_secret="client_secret_here",
      redirect_uri="redirect_uri_here",
      scopes=["identify", "guilds", "email", "connections"],
   )


   async def main():
      # Exchange a code that I received from callback to redirect url.
      access_token = await client.exchange_code("my_code")

      # Fetch user's information with access token.
      user = await client.fetch_user(access_token)

      # Fetch user's connections.
      connections = await user.fetch_connections()

      # Fetch guilds that the user is member of.
      guilds = await user.fetch_guilds()

      print(f"{user!r} | {connections!r}")

      for guild in guilds:
         print(f"`{user.name}` member of {guild!r}")

Contributing
-------------
All contributions are welcome ;)

Table Of Contents
-----------------

.. toctree::
   :maxdepth: 2

   api.rst