"""
Main entry point for the CLI Chatbot.
"""

import os
import sys
from chatbot import ChatBot, Config
from utils.formatting import format_error


def main():
    """Main function to run the chatbot."""
    try:
        # Load configuration from environment
        config = Config.from_env()

        # Create and run the chatbot
        bot = ChatBot(config)
        bot.run()

    except ValueError as e:
        format_error(str(e))
        print("\nPlease set up your environment variables:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Run the chatbot again")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
        sys.exit(0)

    except Exception as e:
        format_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()