"""
In-memory response cache for the scouting agent.

Keys   : normalized player names (lowercase, stripped).
Values : serialized AgentResponse dicts.

Avoids re-running the expensive LangGraph + LLM chain when the same
player is requested more than once. Cache lives for the lifetime of the
server process. Swap the dict for Redis or a JSON file for persistence.
"""

# from typing import Optional

from typing import Any

# Use Any or a more specific type - AgentResponse has a known structure
_cache: dict[str, dict[str, Any]] = {}

def _normalize(player_name: str) -> str:
    """Return a canonical cache key for a player name."""
    return player_name.strip().lower()

def get_cached(player_name: str) -> dict[str, Any] | None:
    """Return cached AgentResponse dict, or None on a miss."""
    # Using the | None syntax is the modern way to write Optional
    return _cache.get(_normalize(player_name))

def set_cached(player_name: str, response: dict[str, Any]) -> None:
    """Store an AgentResponse dict in the cache."""
    _cache[_normalize(player_name)] = response

def cache_size() -> int:
    """Return the number of entries currently in the cache."""
    return len(_cache)

def clear_cache() -> None:
    """Wipe all cached entries (useful for testing or admin endpoints)."""
    _cache.clear()
