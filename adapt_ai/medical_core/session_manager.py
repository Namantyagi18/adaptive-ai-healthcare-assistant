"""Session and Multi-turn Conversation Management for ADAPT-AI."""

import time
import uuid
from typing import Dict, List, Optional
from threading import Lock
from adapt_ai.models.schemas import ChatMessage, ChatRole


class SessionManager:
    """Thread-safe session store maintaining conversation history across turns."""

    def __init__(self, max_idle_seconds: float = 3600.0, max_messages_per_session: int = 20):
        self.max_idle_seconds = max_idle_seconds
        self.max_messages = max_messages_per_session
        self._sessions: Dict[str, List[ChatMessage]] = {}
        self._last_active: Dict[str, float] = {}
        self._lock = Lock()

    def get_or_create_session_id(self, session_id: Optional[str] = None) -> str:
        """Validates or generates a unique session UUID."""
        with self._lock:
            if not session_id or session_id not in self._sessions:
                new_id = session_id or str(uuid.uuid4())
                self._sessions[new_id] = []
                self._last_active[new_id] = time.time()
                return new_id
            self._last_active[session_id] = time.time()
            return session_id

    def add_message(self, session_id: str, role: ChatRole, content: str) -> None:
        """Appends a new turn to the session history, pruning oldest if capacity is exceeded."""
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = []
            
            history = self._sessions[session_id]
            history.append(ChatMessage(role=role, content=content))
            
            if len(history) > self.max_messages:
                # Keep the latest messages
                self._sessions[session_id] = history[-self.max_messages:]
            self._last_active[session_id] = time.time()

    def get_history(self, session_id: str) -> List[ChatMessage]:
        """Returns the conversation history for a given session."""
        with self._lock:
            return list(self._sessions.get(session_id, []))

    def prune_stale_sessions(self) -> int:
        """Removes sessions that have been inactive longer than max_idle_seconds."""
        now = time.time()
        pruned = 0
        with self._lock:
            stale_keys = [
                s_id for s_id, last_t in self._last_active.items()
                if (now - last_t) > self.max_idle_seconds
            ]
            for s_id in stale_keys:
                del self._sessions[s_id]
                del self._last_active[s_id]
                pruned += 1
        return pruned

    def clear(self) -> None:
        """Flushes all session history."""
        with self._lock:
            self._sessions.clear()
            self._last_active.clear()


# Global singleton instance
session_manager = SessionManager()

