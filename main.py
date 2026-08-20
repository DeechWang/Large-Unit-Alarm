from discord_logic import DiscordSelfBot


def main():
    bot = DiscordSelfBot()
    try:
        # Run the bot
        print("Starting Discord bot...")
        bot.run()
    except Exception as e:
        print(f"Error running bot: {e}")


if __name__ == "__main__":
    main()
