"""Command-line interface for the Basic Chatbot."""

import sys

from src.core.session import ChatSession


BANNER = """
+======================================================+
|          BASIC CHATBOT - CodeAlpha Project           |
|         Rule-Based Intelligent Assistant             |
+======================================================+
"""

WELCOME_MESSAGE = (
    "Welcome! I'm your rule-based assistant.\n"
    "Type 'help' to see available commands or 'bye' to exit.\n"
    "Tip: Set your name with  my name is <YourName>"
)


def get_username() -> str:
    """
    Prompt the user for their name at session start.

    Returns:
        User's chosen display name.
    """
    print("\n--- Session Setup ---")
    while True:
        name = input("Enter your name (or press Enter for 'Friend'): ").strip()
        if not name:
            return "Friend"
        if len(name) > 50:
            print("Name is too long. Please use 50 characters or fewer.")
            continue
        if name.replace(" ", "").isalpha() or " " in name:
            return name.title()
        print("Please enter a valid name using letters only.")


def print_bot(response: str) -> None:
    """Display a bot response with consistent formatting."""
    print(f"\nBot: {response}")


def run_chatbot() -> None:
    """Main entry point for the CLI chatbot application."""
    print(BANNER)
    username = get_username()
    session = ChatSession(username=username)

    print(f"\nHello, {username}! Your session has started.")
    print(WELCOME_MESSAGE)

    try:
        while session.is_running:
            try:
                user_input = input(f"\n{session.username}: ").strip()
            except EOFError:
                print("\n\nEnd of input detected. Closing session...")
                break

            if not user_input:
                print("Bot: Please type a message or 'help' for commands.")
                continue

            response = session.process_input(user_input)
            print_bot(response)

    except KeyboardInterrupt:
        print("\n\nSession interrupted. Saving history...")
    except Exception as exc:
        print(f"\nAn unexpected error occurred: {exc}")
        print("Saving session data before exit...")
    finally:
        session.end_session()
        print(session.get_session_summary())


def main() -> None:
    """Script entry point."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stdin.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    run_chatbot()
    sys.exit(0)


if __name__ == "__main__":
    main()
