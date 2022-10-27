def init(client):
    @client.tree.command(name="ping", description="Ping the bot")
    async def ping(interaction):
        await interaction.response.send_message(
            f"Pong! {round(client.latency * 1000)}ms"
        )