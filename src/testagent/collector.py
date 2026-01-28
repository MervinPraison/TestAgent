"""
Test discovery for TestAgent - inspired by pytest's collection system.

Discovers AI tests in files matching test_*.py pattern.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Callable, Any, Dict
import fnmatch


@dataclass
class TestAgentItem:
    """
    Represents a single AI test item.
    
    Similar to pytest's Item node.
    """
    nodeid: str
    name: str
    path: Path
    function: Optional[Callable] = None
    markers: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self) -> str:
        return f"<TestAgentItem {self.nodeid}>"


@dataclass
class TestAgentModule:
    """
    Represents a test module (file).
    
    Similar to pytest's Module node.
    """
    path: Path
    items: List[TestAgentItem] = field(default_factory=list)
    
    @property
    def nodeid(self) -> str:
        return str(self.path)
    
    def __repr__(self) -> str:
        return f"<TestAgentModule {self.path.name} ({len(self.items)} tests)>"


class Collector:
    """
    Test collector for TestAgent.
    
    Discovers test functions in Python files matching patterns.
    Inspired by pytest's collection system for speed and robustness.
    
    Example:
        >>> collector = Collector()
        >>> items = collector.collect(Path("tests/"))
        >>> for item in items:
        ...     print(item.nodeid)
    """
    
    # Default patterns (like pytest)
    DEFAULT_FILE_PATTERNS = ["test_*.py", "*_test.py"]
    DEFAULT_FUNC_PATTERNS = ["test_*", "*_test"]
    DEFAULT_CLASS_PATTERNS = ["Test*"]
    
    def __init__(
        self,
        file_patterns: Optional[List[str]] = None,
        func_patterns: Optional[List[str]] = None,
        class_patterns: Optional[List[str]] = None,
    ):
        """
        Initialize collector.
        
        Args:
            file_patterns: Glob patterns for test files
            func_patterns: Patterns for test function names
            class_patterns: Patterns for test class names
        """
        self.file_patterns = file_patterns or self.DEFAULT_FILE_PATTERNS
        self.func_patterns = func_patterns or self.DEFAULT_FUNC_PATTERNS
        self.class_patterns = class_patterns or self.DEFAULT_CLASS_PATTERNS
    
    def collect(self, path: Path) -> List[TestAgentItem]:
        """
        Collect all test items from path.
        
        Args:
            path: File or directory to collect from
            
        Returns:
            List of TestAgentItem objects
        """
        path = Path(path)
        
        if path.is_file():
            return self._collect_file(path)
        elif path.is_dir():
            return self._collect_directory(path)
        else:
            return []
    
    def collect_only(self, path: Path) -> List[TestAgentModule]:
        """
        Collect modules without loading functions (fast).
        
        Args:
            path: File or directory to collect from
            
        Returns:
            List of TestAgentModule objects
        """
        path = Path(path)
        modules = []
        
        if path.is_file():
            module = self._collect_module_fast(path)
            if module:
                modules.append(module)
        elif path.is_dir():
            for file_path in self._find_test_files(path):
                module = self._collect_module_fast(file_path)
                if module:
                    modules.append(module)
        
        return modules
    
    def _find_test_files(self, directory: Path) -> List[Path]:
        """Find all test files in directory."""
        test_files = []
        
        for pattern in self.file_patterns:
            test_files.extend(directory.rglob(pattern))
        
        # Remove duplicates and sort
        return sorted(set(test_files))
    
    def _collect_directory(self, directory: Path) -> List[TestAgentItem]:
        """Collect all tests from a directory."""
        items = []
        
        for file_path in self._find_test_files(directory):
            items.extend(self._collect_file(file_path))
        
        return items
    
    def _collect_file(self, file_path: Path) -> List[TestAgentItem]:
        """Collect tests from a single file."""
        items = []
        
        try:
            # Parse AST first (fast, no execution)
            with open(file_path, 'r') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(file_path))
            
            # Find test functions and classes at module level only
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    if self._is_test_function(node.name):
                        item = TestAgentItem(
                            nodeid=f"{file_path}::{node.name}",
                            name=node.name,
                            path=file_path,
                            markers=self._extract_markers(node),
                        )
                        items.append(item)
                
                elif isinstance(node, ast.ClassDef):
                    if self._is_test_class(node.name):
                        # Collect methods from test class
                        for child in node.body:
                            if isinstance(child, ast.FunctionDef):
                                if self._is_test_function(child.name):
                                    item = TestAgentItem(
                                        nodeid=f"{file_path}::{node.name}::{child.name}",
                                        name=f"{node.name}.{child.name}",
                                        path=file_path,
                                        markers=self._extract_markers(child),
                                    )
                                    items.append(item)
        
        except (SyntaxError, IOError):
            # Log error but continue
            pass
        
        return items
    
    def _collect_module_fast(self, file_path: Path) -> Optional[TestAgentModule]:
        """Collect module info without loading (AST only)."""
        items = self._collect_file(file_path)
        
        if items:
            return TestAgentModule(path=file_path, items=items)
        return None
    
    def _is_test_function(self, name: str) -> bool:
        """Check if function name matches test patterns."""
        for pattern in self.func_patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        return False
    
    def _is_test_class(self, name: str) -> bool:
        """Check if class name matches test patterns."""
        for pattern in self.class_patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        return False
    
    def _extract_markers(self, node: ast.FunctionDef) -> List[str]:
        """Extract marker names from decorators."""
        markers = []
        
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    # @mark.skip(), @mark.criteria()
                    if decorator.func.attr:
                        markers.append(decorator.func.attr)
            elif isinstance(decorator, ast.Attribute):
                # @mark.skip (without call)
                if decorator.attr:
                    markers.append(decorator.attr)
        
        return markers


def collect(path: Path) -> List[TestAgentItem]:
    """
    Convenience function to collect tests.
    
    Args:
        path: File or directory to collect from
        
    Returns:
        List of TestAgentItem objects
    """
    collector = Collector()
    return collector.collect(path)


__all__ = ['Collector', 'TestAgentItem', 'TestAgentModule', 'collect']
