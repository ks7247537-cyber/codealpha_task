"""Intent handler functions for the Basic Chatbot."""

import random
from datetime import datetime
from typing import Tuple

from src.utils.validators import validate_expression


def handle_greeting(username: str = "Friend") -> str:
    """
    Respond to greeting intents.

    Args:
        username: Stored user name for personalization.

    Returns:
        Greeting response string.
    """
    greetings = [
        f"Hello, {username}! Welcome to Basic Chatbot.",
        f"Hi there, {username}! How can I assist you today?",
        f"Hey {username}! Great to see you. Type 'help' to see what I can do.",
    ]
    return random.choice(greetings)


def handle_how_are_you(username: str = "Friend") -> str:
    """
    Respond to 'how are you' queries.

    Args:
        username: Stored user name for personalization.

    Returns:
        Status response string.
    """
    responses = [
        f"I'm doing great, {username}! Ready to help you.",
        "I'm functioning perfectly! How can I help you today?",
        "All systems operational! What would you like to know?",
    ]
    return random.choice(responses)


def handle_farewell(username: str = "Friend") -> str:
    """
    Respond to farewell intents.

    Args:
        username: Stored user name for personalization.

    Returns:
        Farewell response string.
    """
    farewells = [
        f"Goodbye, {username}! Have a wonderful day!",
        f"See you later, {username}! It was nice chatting with you.",
        f"Bye, {username}! Come back anytime.",
    ]
    return random.choice(farewells)


def handle_help() -> str:
    """
    Display available commands and usage instructions.

    Returns:
        Help message string.
    """
    return (
        "\n--- Available Commands ---\n"
        "  hello / hi          - Greet the chatbot\n"
        "  how are you         - Ask how the bot is doing\n"
        "  time                - Get the current time\n"
        "  date                - Get today's date\n"
        "  help                - Show this help message\n"
        "  joke                - Hear a random joke\n"
        "  quote               - Get a motivational quote\n"
        "  calculator          - Perform basic math calculations\n"
        "  my name is <name>   - Set your display name\n"
        "  bye                 - End the session\n"
        "----------------------------\n"
    )


def handle_date_query() -> str:
    """
    Return the current date.

    Returns:
        Formatted date string.
    """
    today = datetime.now()
    formatted = today.strftime("%A, %B %d, %Y")
    return f"Today's date is {formatted}."


def handle_time_query() -> str:
    """
    Return the current time.

    Returns:
        Formatted time string.
    """
    now = datetime.now()
    formatted = now.strftime("%I:%M:%S %p")
    return f"The current time is {formatted}."


def handle_calculator(expression: str = "") -> str:
    """
    Evaluate a basic mathematical expression safely.

    Args:
        expression: Mathematical expression to evaluate.

    Returns:
        Result string or error message.
    """
    if not expression:
        return (
            "Calculator mode activated.\n"
            "Enter an expression (e.g., 25 + 17 * 2): "
        )

    is_valid, result = validate_expression(expression)
    if not is_valid:
        return f"Calculator error: {result}"

    try:
        # Restricted eval: only digits and operators pass validation.
        answer = eval(result, {"__builtins__": {}}, {})  # noqa: S307
        return f"Result: {expression.strip()} = {answer}"
    except ZeroDivisionError:
        return "Calculator error: Division by zero is not allowed."
    except (SyntaxError, TypeError, NameError):
        return "Calculator error: Invalid expression. Please try again."
    except Exception as exc:
        return f"Calculator error: {exc}"


def handle_motivational_quote() -> str:
    """
    Return a random motivational quote.

    Returns:
        Motivational quote string.
    """
    quotes = [
        "The only way to do great work is to love what you do. — Steve Jobs",
        "Believe you can and you're halfway there. — Theodore Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to "
        "continue that counts. — Winston Churchill",
        "It always seems impossible until it's done. — Nelson Mandela",
        "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
        "The future belongs to those who believe in the beauty of their "
        "dreams. — Eleanor Roosevelt",
        "Start where you are. Use what you have. Do what you can. — "
        "Arthur Ashe",
    ]
    return f"Motivational Quote:\n  \"{random.choice(quotes)}\""


def handle_joke() -> str:
    """
    Return a random joke.

    Returns:
        Joke string.
    """
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the Python programmer not respond? Because they were stuck "
        "in an infinite loop!",
        "How do you comfort a JavaScript bug? You console it.",
        "Why do Java developers wear glasses? Because they don't C#.",
        "A SQL query walks into a bar, walks up to two tables and asks: "
        "'Can I join you?'",
        "There are only 10 types of people: those who understand binary "
        "and those who don't.",
    ]
    return f"Here's a joke for you:\n  {random.choice(jokes)}"


def handle_unknown(user_input: str) -> str:
    """
    Handle unrecognized user input.

    Args:
        user_input: The unrecognized input string.

    Returns:
        Fallback response string.
    """
    return (
        f"I'm not sure how to respond to \"{user_input}\".\n"
        "Type 'help' to see available commands."
    )


def detect_intent(user_input: str) -> Tuple[str, str]:
    """
    Map user input to an intent label and optional payload.

    Args:
        user_input: Cleaned user input string.

    Returns:
        Tuple of (intent_name, payload).
    """
    normalized = user_input.lower().strip()

    intent_map = {
        "hello": "greeting",
        "hi": "greeting",
        "hey": "greeting",
        "how are you": "how_are_you",
        "how are you?": "how_are_you",
        "time": "time",
        "what time is it": "time",
        "what's the time": "time",
        "date": "date",
        "what's the date": "date",
        "what is the date": "date",
        "help": "help",
        "joke": "joke",
        "tell me a joke": "joke",
        "quote": "quote",
        "motivation": "quote",
        "motivational quote": "quote",
        "calculator": "calculator",
        "calc": "calculator",
        "bye": "farewell",
        "goodbye": "farewell",
        "exit": "farewell",
        "quit": "farewell",
    }

    if normalized in intent_map:
        return intent_map[normalized], ""

    if normalized.startswith("my name is "):
        name = user_input[11:].strip().title()
        return "set_name", name

    if normalized.startswith("calculate "):
        return "calculator", user_input[10:].strip()

    # Treat numeric expressions as calculator input when in calculator flow
    # or when input looks like math.
    math_chars = set("0123456789+-*/(). ")
    if normalized and all(c in math_chars for c in normalized):
        return "calculator", user_input.strip()

    return "unknown", user_input
