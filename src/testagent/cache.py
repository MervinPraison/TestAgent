"""
Caching system for TestAgent - prevents redundant LLM calls.

Inspired by pytest's cacheprovider.py for speed optimization.
"""

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Any, Dict


@dataclass
class CacheKey:
    """
    Cache key for AI test results.
    
    Uses content hashing for deterministic cache lookups.
    """
    output: str = field(repr=False)
    criteria: Optional[str] = field(default=None, repr=False)
    expected: Optional[str] = field(default=None, repr=False)
    model: str = "gpt-4o-mini"
    
    # Computed hashes
    output_hash: str = field(init=False)
    criteria_hash: str = field(init=False)
    expected_hash: str = field(init=False)
    
    def __post_init__(self):
        self.output_hash = self._hash(self.output)
        self.criteria_hash = self._hash(self.criteria or "")
        self.expected_hash = self._hash(self.expected or "")
    
    @staticmethod
    def _hash(content: str) -> str:
        """Create SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def to_string(self) -> str:
        """Convert to string for file storage."""
        return f"{self.model}_{self.output_hash}_{self.criteria_hash}_{self.expected_hash}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "output_hash": self.output_hash,
            "criteria_hash": self.criteria_hash,
            "expected_hash": self.expected_hash,
            "model": self.model,
        }


class TestAgentCache:
    """
    Cache for AI test results.
    
    Stores results in JSON files under .testagent_cache/ directory.
    Similar to pytest's .pytest_cache/ for --lf and --ff.
    
    Example:
        >>> cache = TestAgentCache()
        >>> key = CacheKey(output="test", criteria="correct", model="gpt-4o-mini")
        >>> cache.set(key, result)
        >>> cached = cache.get(key)
    """
    
    # Sub-directory for cached values
    _CACHE_PREFIX = "v"
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize cache.
        
        Args:
            cache_dir: Cache directory path. Defaults to .testagent_cache/
        """
        if cache_dir is None:
            cache_dir = Path.cwd() / ".testagent_cache"
        
        self.cache_dir = Path(cache_dir)
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self) -> None:
        """Create cache directory if it doesn't exist."""
        cache_values_dir = self.cache_dir / self._CACHE_PREFIX
        cache_values_dir.mkdir(parents=True, exist_ok=True)
        
        # Create README
        readme_path = self.cache_dir / "README.md"
        if not readme_path.exists():
            readme_path.write_text(
                "# TestAgent Cache Directory\n\n"
                "This directory contains cached AI test results.\n"
                "Use `--cache-clear` to clear the cache.\n\n"
                "**Do not** commit this to version control.\n"
            )
        
        # Create .gitignore
        gitignore_path = self.cache_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text("*\n")
    
    def _get_cache_path(self, key: CacheKey) -> Path:
        """Get file path for cache key."""
        return self.cache_dir / self._CACHE_PREFIX / f"{key.to_string()}.json"
    
    def get(self, key: CacheKey) -> Optional[Any]:
        """
        Get cached result.
        
        Args:
            key: Cache key
            
        Returns:
            TestResult if cached, None otherwise
        """
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
            
            # Reconstruct TestResult
            from .results import TestResult
            return TestResult(
                score=data.get("score", 0.0),
                passed=data.get("passed", False),
                reasoning=data.get("reasoning", ""),
                criteria=data.get("criteria"),
                expected=data.get("expected"),
                output=data.get("output"),
                metadata=data.get("metadata", {}),
            )
        except (json.JSONDecodeError, KeyError, IOError):
            return None
    
    def set(self, key: CacheKey, result: Any) -> None:
        """
        Store result in cache.
        
        Args:
            key: Cache key
            result: TestResult to cache
        """
        cache_path = self._get_cache_path(key)
        
        try:
            data = result.to_dict() if hasattr(result, 'to_dict') else {
                "score": getattr(result, 'score', 0.0),
                "passed": getattr(result, 'passed', False),
                "reasoning": getattr(result, 'reasoning', ""),
                "criteria": getattr(result, 'criteria', None),
                "expected": getattr(result, 'expected', None),
                "output": getattr(result, 'output', None),
            }
            
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass  # Silently fail on cache write errors
    
    def clear(self) -> None:
        """Clear all cached values."""
        cache_values_dir = self.cache_dir / self._CACHE_PREFIX
        if cache_values_dir.exists():
            import shutil
            shutil.rmtree(cache_values_dir)
            cache_values_dir.mkdir(parents=True, exist_ok=True)
    
    def stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        cache_values_dir = self.cache_dir / self._CACHE_PREFIX
        if not cache_values_dir.exists():
            return {"entries": 0, "size_bytes": 0}
        
        entries = list(cache_values_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in entries)
        
        return {
            "entries": len(entries),
            "size_bytes": total_size,
        }


# Global cache instance (lazy loaded)
_global_cache: Optional[TestAgentCache] = None


def get_cache(cache_dir: Optional[Path] = None) -> TestAgentCache:
    """Get or create global cache instance."""
    global _global_cache
    if _global_cache is None or (cache_dir and _global_cache.cache_dir != cache_dir):
        _global_cache = TestAgentCache(cache_dir=cache_dir)
    return _global_cache


__all__ = ['CacheKey', 'TestAgentCache', 'get_cache']
