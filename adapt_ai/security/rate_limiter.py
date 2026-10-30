"""Configurable sliding-window rate limiter for the ADAPT-AI platform.

Prevents denial-of-service, upstream quota exhaustion, and abusive requests.
Tracks client requests per time window with burst tolerance.
"""

import time
from collections import defaultdict
from typing import Dict, List, Tuple


class RateLimiter:
    """In-memory sliding window rate limiter."""
    
    def __init__(self, requests_per_minute: int = 60, burst_allowance: int = 10):
        self.limit = requests_per_minute
        self.burst = burst_allowance
        self.window_seconds = 60.0
        # Maps client_id -> list of float timestamps
        self._history: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> Tuple[bool, int, float]:
        """Evaluates whether the client request is permitted under rate limits.
        
        Returns:
            Tuple[bool, int, float]:
                - allowed: True if request is allowed, False if rejected
                - remaining: remaining requests available in window
                - reset_time: seconds remaining until window resets
        """
        now = time.time()
        cutoff = now - self.window_seconds
        
        # Clean timestamps older than sliding window
        timestamps = [ts for ts in self._history[client_id] if ts > cutoff]
        self._history[client_id] = timestamps
        
        effective_capacity = self.limit + self.burst
        
        if len(timestamps) < effective_capacity:
            timestamps.append(now)
            remaining = max(0, self.limit - len(timestamps))
            return True, remaining, 0.0
        else:
            oldest = timestamps[0]
            retry_after = max(0.1, round(self.window_seconds - (now - oldest), 2))
            return False, 0, retry_after

    def reset_client(self, client_id: str) -> None:
        """Clears request history for a specific client."""
        if client_id in self._history:
            del self._history[client_id]

    def clear(self) -> None:
        """Flushes all rate limiting records."""
        self._history.clear()


# Global rate limiter instance initialized with settings
from adapt_ai.config import settings
rate_limiter = RateLimiter(
    requests_per_minute=settings.RATE_LIMIT_PER_MINUTE,
    burst_allowance=settings.RATE_LIMIT_BURST
)

