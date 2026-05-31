"""Conversation history management and persistence."""

import os
from datetime import datetime
from typing import List, Dict, Optional


class HistoryManager:
    """Manages in-session conversation history and file persistence."""

    def __init__(self, filepath: str = "chat_history.txt") -> None:
        """
        Initialize the history manager.

        Args:
            filepath: Path to the chat history output file.
        """
        self.filepath = filepath
        self.history: List[Dict[str, str]] = []

    def add_entry(
        self,
        sender: str,
        message: str,
        intent: Optional[str] = None,
    ) -> None:
        """
        Add a message to the conversation history.

        Args:
            sender: 'User' or 'Bot'.
            message: Message content.
            intent: Detected intent label, if applicable.
        """
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": sender,
            "message": message,
            "intent": intent or "N/A",
        }
        self.history.append(entry)

    def get_history(self) -> List[Dict[str, str]]:
        """Return a copy of the conversation history."""
        return list(self.history)

    def get_message_count(self) -> int:
        """Return total number of messages exchanged."""
        return len(self.history)

    def save_to_file(
        self,
        username: str,
        session_start: datetime,
        session_end: datetime,
    ) -> None:
        """
        Persist chat history and session summary to a text file.

        Args:
            username: Name of the user for this session.
            session_start: Session start datetime.
            session_end: Session end datetime.
        """
        duration = session_end - session_start
        duration_str = self._format_duration(duration)

        lines = [
            "=" * 60,
            "BASIC CHATBOT - SESSION SUMMARY",
            "=" * 60,
            f"User Name          : {username}",
            f"Session Start      : {session_start.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Session End        : {session_end.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Session Duration   : {duration_str}",
            f"Total Messages     : {self.get_message_count()}",
            "=" * 60,
            "CONVERSATION LOG",
            "=" * 60,
            "",
        ]

        for entry in self.history:
            lines.append(f"[{entry['timestamp']}] {entry['sender']} ({entry['intent']})")
            lines.append(f"  {entry['message']}")
            lines.append("")

        lines.append("=" * 60)
        lines.append("End of Session")
        lines.append("=" * 60)

        output_dir = os.path.dirname(self.filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(self.filepath, "a", encoding="utf-8") as file:
            file.write("\n".join(lines))
            file.write("\n\n")

    @staticmethod
    def _format_duration(duration) -> str:
        """Format a timedelta object into a human-readable string."""
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        return " ".join(parts)
