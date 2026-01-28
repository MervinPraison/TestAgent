"""
Tests for TestAgent collector (test discovery).
"""

import tempfile
from pathlib import Path


class TestTestAgentItem:
    """Test TestAgentItem class."""
    
    def test_item_creation(self):
        """Test creating a test item."""
        from testagent.collector import TestAgentItem
        
        item = TestAgentItem(
            nodeid="tests/test_example.py::test_foo",
            name="test_foo",
            path=Path("tests/test_example.py"),
        )
        
        assert item.nodeid == "tests/test_example.py::test_foo"
        assert item.name == "test_foo"
    
    def test_item_repr(self):
        """Test item string representation."""
        from testagent.collector import TestAgentItem
        
        item = TestAgentItem(
            nodeid="test.py::test_foo",
            name="test_foo",
            path=Path("test.py"),
        )
        
        assert "TestAgentItem" in repr(item)
        assert "test.py::test_foo" in repr(item)


class TestTestAgentModule:
    """Test TestAgentModule class."""
    
    def test_module_creation(self):
        """Test creating a test module."""
        from testagent.collector import TestAgentModule
        
        module = TestAgentModule(path=Path("tests/test_example.py"))
        
        assert module.path == Path("tests/test_example.py")
        assert len(module.items) == 0
    
    def test_module_nodeid(self):
        """Test module nodeid property."""
        from testagent.collector import TestAgentModule
        
        module = TestAgentModule(path=Path("tests/test_example.py"))
        
        assert "test_example.py" in module.nodeid


class TestCollector:
    """Test Collector class."""
    
    def test_collector_init(self):
        """Test collector initialization."""
        from testagent.collector import Collector
        
        collector = Collector()
        
        assert collector.file_patterns == ["test_*.py", "*_test.py"]
        assert collector.func_patterns == ["test_*", "*_test"]
    
    def test_collector_custom_patterns(self):
        """Test collector with custom patterns."""
        from testagent.collector import Collector
        
        collector = Collector(
            file_patterns=["check_*.py"],
            func_patterns=["check_*"],
        )
        
        assert collector.file_patterns == ["check_*.py"]
        assert collector.func_patterns == ["check_*"]
    
    def test_collect_file(self):
        """Test collecting from a single file."""
        from testagent.collector import Collector
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_example.py"
            test_file.write_text("""
def test_foo():
    pass

def test_bar():
    pass

def helper():
    pass
""")
            
            collector = Collector()
            items = collector.collect(test_file)
            
            assert len(items) == 2
            assert any("test_foo" in item.name for item in items)
            assert any("test_bar" in item.name for item in items)
            # helper should not be collected
            assert not any("helper" in item.name for item in items)
    
    def test_collect_class(self):
        """Test collecting from test classes."""
        from testagent.collector import Collector
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_example.py"
            test_file.write_text("""
class TestFoo:
    def test_one(self):
        pass
    
    def test_two(self):
        pass
    
    def helper(self):
        pass

class Helper:
    def test_should_not_collect(self):
        pass
""")
            
            collector = Collector()
            items = collector.collect(test_file)
            
            assert len(items) == 2
            assert any("TestFoo.test_one" in item.name for item in items)
            assert any("TestFoo.test_two" in item.name for item in items)
    
    def test_collect_directory(self):
        """Test collecting from a directory."""
        from testagent.collector import Collector
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            (Path(tmpdir) / "test_one.py").write_text("def test_a(): pass")
            (Path(tmpdir) / "test_two.py").write_text("def test_b(): pass")
            (Path(tmpdir) / "helper.py").write_text("def test_c(): pass")  # Should not match
            
            collector = Collector()
            items = collector.collect(Path(tmpdir))
            
            assert len(items) == 2
            assert any("test_a" in item.name for item in items)
            assert any("test_b" in item.name for item in items)
    
    def test_collect_only(self):
        """Test collect_only for fast discovery."""
        from testagent.collector import Collector
        
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "test_example.py").write_text("""
def test_foo(): pass
def test_bar(): pass
""")
            
            collector = Collector()
            modules = collector.collect_only(Path(tmpdir))
            
            assert len(modules) == 1
            assert len(modules[0].items) == 2
    
    def test_collect_nonexistent(self):
        """Test collecting from nonexistent path."""
        from testagent.collector import Collector
        
        collector = Collector()
        items = collector.collect(Path("/nonexistent/path"))
        
        assert items == []


class TestCollectFunction:
    """Test the collect convenience function."""
    
    def test_collect_function(self):
        """Test the collect() function."""
        from testagent.collector import collect
        
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "test_example.py").write_text("def test_foo(): pass")
            
            items = collect(Path(tmpdir))
            
            assert len(items) == 1
            assert "test_foo" in items[0].name
