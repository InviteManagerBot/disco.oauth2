from disco_oauth2 import Client

client = Client(
    client_id=123, # my_client_id_here
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