"""
Configuration for TestAgent.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import os


@dataclass
class TestConfig:
    """
    Configuration for AI tests.
    
    Attributes:
        model: LLM model to use (default: gpt-4o-mini)
        temperature: Temperature for LLM calls (default: 0.1)
        threshold: Score threshold for passing (default: 7.0)
        verbose: Whether to print verbose output
        cache_enabled: Whether to enable caching (default: True)
        cache_dir: Directory for cache storage (default: .testagent_cache)
        fail_fast: Exit on first failure (default: False)
        max_fail: Maximum failures before exit (default: 0 = unlimited)
    """
    model: Optional[str] = None
    temperature: float = 0.1
    threshold: float = 7.0
    verbose: bool = False
    cache_enabled: bool = True
    cache_dir: Optional[str] = None
    fail_fast: bool = False
    max_fail: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.model is None:
            self.model = os.getenv("AITEST_MODEL", os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"))
        if self.cache_dir is None:
            self.cache_dir = os.getenv("AITEST_CACHE_DIR", ".testagent_cache")


# Global default config
_default_config: Optional[TestConfig] = None


def get_config() -> TestConfig:
    """Get the global default config."""
    global _default_config
    if _default_config is None:
        _default_config = TestConfig()
    return _default_config


def set_config(config: TestConfig) -> None:
    """Set the global default config."""
    global _default_config
    _default_config = config


__all__ = ['TestConfig', 'get_config', 'set_config']
