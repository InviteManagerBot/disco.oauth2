# Discord OAuth2
A modern, easy to use discord OAuth2 API wrapper written in Python.

## Installing
To install [Python >3.8](https://www.python.org/downloads/release/python-370/) is required.
You can run the following command to install the library:
```bash
# Linux/FreeBSD
python3 -m pip install -U disco.oauth2

# Windows
py -3 -m pip install -U disco.oauth2
```
To install the development version (lastest), do the following:
```bash
# Linux/FreeBSD
python3 -m pip install -U https://github.com/InviteManagerBot/disco.oauth2

# Windows
py -3 -m pip install -U https://github.com/InviteManagerBot/disco.oauth2
```
## Getting started
### Quick Example
```py
from disco_oauth2.client import Client

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
```

## Requirements
- aiohttp > = 3.7.4, < 4

Optionally you may install the [`orjson`](https://github.com/ijl/orjson) libraries (highly recommended for sake of speed).

## License
`discord_oauth2` was written by martimartins <martim13artins13@gmail.com>, licensed under the [MIT](https://opensource.org/licenses/MIT) license.

## Contributing
All contributions are welcome ;)