"""Session management for the Basic Chatbot."""

from datetime import datetime
from typing import Optional

from src.core.intents import (
    detect_intent,
    handle_calculator,
    handle_date_query,
    handle_farewell,
    handle_greeting,
    handle_help,
    handle_how_are_you,
    handle_joke,
    handle_motivational_quote,
    handle_time_query,
    handle_unknown,
)
from src.utils.history_manager import HistoryManager
from src.utils.validators import validate_user_input


class ChatSession:
    """Manages a single chatbot conversation session."""

    def __init__(
        self,
        username: str = "Friend",
        history_file: str = "chat_history.txt",
    ) -> None:
        """
        Initialize a new chat session.

        Args:
            username: Default display name for the user.
            history_file: Path for persisting chat history.
        """
        self.username = username
        self.history = HistoryManager(filepath=history_file)
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.is_running = True
        self.calculator_mode = False
        self._last_intent = "session_start"

    def process_input(self, user_input: str) -> str:
        """
        Process user input and return the bot response.

        Args:
            user_input: Raw input from the user.

        Returns:
            Bot response string.
        """
        is_valid, cleaned = validate_user_input(user_input)

        if not is_valid:
            return "Please enter a valid message. Input cannot be empty."

        self.history.add_entry("User", cleaned)

        if self.calculator_mode:
            response = self._handle_calculator_flow(cleaned)
        else:
            response = self._route_intent(cleaned)

        self.history.add_entry("Bot", response, intent=self._last_intent)
        return response

    def _route_intent(self, user_input: str) -> str:
        """Route input to the appropriate intent handler."""
        intent, payload = detect_intent(user_input)
        self._last_intent = intent

        if intent == "greeting":
            return handle_greeting(self.username)

        if intent == "how_are_you":
            return handle_how_are_you(self.username)

        if intent == "farewell":
            self.is_running = False
            return handle_farewell(self.username)

        if intent == "help":
            return handle_help()

        if intent == "date":
            return handle_date_query()

        if intent == "time":
            return handle_time_query()

        if intent == "joke":
            return handle_joke()

        if intent == "quote":
            return handle_motivational_quote()

        if intent == "calculator":
            self.calculator_mode = True
            return handle_calculator()

        if intent == "set_name":
            if payload:
                self.username = payload
                return f"Nice to meet you, {self.username}! How can I help you?"
            return "Please provide a name. Example: my name is Alex"

        return handle_unknown(user_input)

    def _handle_calculator_flow(self, user_input: str) -> str:
        """Handle input while calculator mode is active."""
        normalized = user_input.lower().strip()

        if normalized in ("exit", "quit", "bye", "back"):
            self.calculator_mode = False
            self._last_intent = "calculator_exit"
            return "Exited calculator mode. Type 'help' for other commands."

        self._last_intent = "calculator"
        result = handle_calculator(user_input)

        if result.startswith("Calculator error"):
            return result

        return result + "\nEnter another expression or type 'back' to exit."

    def end_session(self) -> None:
        """Mark session as ended and persist history."""
        self.end_time = datetime.now()
        self.history.save_to_file(
            username=self.username,
            session_start=self.start_time,
            session_end=self.end_time,
        )

    def get_session_summary(self) -> str:
        """
        Build a formatted session summary string.

        Returns:
            Session summary for display.
        """
        end = self.end_time or datetime.now()
        duration = end - self.start_time
        duration_str = HistoryManager._format_duration(duration)

        return (
            "\n"
            + "=" * 50
            + "\n"
            + "           SESSION SUMMARY\n"
            + "=" * 50
            + f"\n  User Name            : {self.username}"
            + f"\n  Total Messages       : {self.history.get_message_count()}"
            + f"\n  Session Duration     : {duration_str}"
            + f"\n  Chat History Saved   : {self.history.filepath}"
            + "\n"
            + "=" * 50
            + "\n  Thank you for using Basic Chatbot!\n"
            + "=" * 50
        )
