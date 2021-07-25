@client.event
async def on_ready():
    """Příkazy vykonané po spuštění"""

    print(f"Online | {round(client.latency * 1000)} ms | {client.user}")
    await client.change_presence(activity=Game(name=load_cfg("description")))
