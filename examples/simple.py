from discord_oauth2.client import AsyncClient

a = AsyncClient(client_id=123, client_secret="*", redirect_uri="https://google.pt")


async def main():
    ...
