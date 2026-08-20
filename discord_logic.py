import discord
import json
from discord.ext import commands
from unit_analysis import analyze_text_for_units
from calling import call

class DiscordSelfBot():
    def __init__(self):
        with open("config.json") as f:
            config = json.load(f)

        self.token = config.get("Token")
        intents = discord.Intents.all()
        self.client = commands.Bot(
            command_prefix="!",
            intents=intents,
            self_bot=False
        )
        self._setup_events()
        self.on_or_off = True
    def _setup_events(self):
        @self.client.event
        async def on_ready():
            ready_message = f"Logged in as {self.client.user.name}"
            print(ready_message)

        @self.client.event
        async def on_message(message):
            await self.client.process_commands(message)

            source_channel_id = [1104477384838758633, 1259607738040979489] 
            command_channel_id = 1350105898298769479
            if message.channel.id in source_channel_id and self.on_or_off:
                print("message detected!")
                try:
                    async for latest_message in message.channel.history(limit=1):
                        content_description = []
                        message_to_process = None

                        if hasattr(latest_message, 'reference') and latest_message.reference:
                            original_channel = self.client.get_channel(latest_message.reference.channel_id)
                            if original_channel:
                                async for hist_message in original_channel.history(limit=100):
                                    if hist_message.id == latest_message.reference.message_id:
                                        print("Found original message!")
                                        message_to_process = hist_message #this will be the most recent dubclub message
                                        break
                        else:
                            message_to_process = latest_message
                            print("latest message method used")
                        if message_to_process:
                            if message_to_process.content:
                                content = message_to_process.content
                                first_line = next((line.strip() for line in content.splitlines() if line.strip()), "")
                                if "league" in first_line.lower():
                                    return
                                content_description.append(f"{content}")
                            print("content description: ", content_description)
                            result = (analyze_text_for_units(content_description))
                            nuke_detected = result.lower() == 'true'
                            if nuke_detected:
                                print("Large Unit Detected")
                                call()
                            else:
                                print("Not nuke play")
                        else:
                            print("message_to_process false")
                except Exception as e:
                    print(f"Error in message processing: {str(e)}")
                    import traceback
                    print(f"Full error: {traceback.format_exc()}")
            elif message.channel.id == command_channel_id:
                content = message.content.lower().strip()

                if content == "off":
                    self.on_or_off = False
                    print("Bot disabled")
                elif content == "on":
                    self.on_or_off = True
                    print("Bot enabled")

    def run(self):
        try:
            self.client.run(self.token, bot=False)
        except discord.LoginFailure:
            raise ValueError("Invalid token in config.json")
        except Exception as e:
            raise Exception(f"Failed to start bot: {str(e)}")
