"""
Tests for TestAgent parametrize and fixture features.

Inspired by pytest's mark/structures.py and fixtures.py.
"""

class TestParametrize:
    """Test @mark.parametrize decorator."""
    
    def test_parametrize_basic(self):
        """Test basic parametrize with single argument."""
        from testagent import mark
        
        results = []
        
        @mark.parametrize("x", [1, 2, 3])
        def test_func(x):
            results.append(x)
            return x * 2
        
        # Execute the parametrized test
        test_func()
        
        assert results == [1, 2, 3]
    
    def test_parametrize_multiple_args(self):
        """Test parametrize with multiple arguments."""
        from testagent import mark
        
        results = []
        
        @mark.parametrize("x, y", [(1, 2), (3, 4), (5, 6)])
        def test_func(x, y):
            results.append((x, y))
            return x + y
        
        test_func()
        
        assert results == [(1, 2), (3, 4), (5, 6)]
    
    def test_parametrize_with_ids(self):
        """Test parametrize with custom IDs."""
        from testagent import mark, param
        
        results = []
        
        @mark.parametrize("x", [
            param(1, id="one"),
            param(2, id="two"),
        ])
        def test_func(x):
            results.append(x)
        
        test_func()
        
        assert results == [1, 2]
    
    def test_parametrize_metadata(self):
        """Test parametrize stores metadata on function."""
        from testagent import mark
        
        @mark.parametrize("x", [1, 2, 3])
        def test_func(x):
            pass
        
        assert hasattr(test_func, '_testagent_parametrize')
        assert test_func._testagent_parametrize['argnames'] == ['x']
        assert test_func._testagent_parametrize['argvalues'] == [1, 2, 3]


class TestParam:
    """Test param() function for parameter sets."""
    
    def test_param_basic(self):
        """Test basic param creation."""
        from testagent import param
        
        p = param(1, 2, 3)
        assert p.values == (1, 2, 3)
        assert p.id is None
    
    def test_param_with_id(self):
        """Test param with custom ID."""
        from testagent import param
        
        p = param(1, 2, id="test_case")
        assert p.values == (1, 2)
        assert p.id == "test_case"
    
    def test_param_with_marks(self):
        """Test param with marks."""
        from testagent import param, mark
        
        p = param(1, marks=mark.skip(reason="skip this"))
        assert p.values == (1,)
        assert len(p.marks) == 1


class TestFixture:
    """Test @fixture decorator."""
    
    def test_fixture_basic(self):
        """Test basic fixture."""
        from testagent import fixture
        
        @fixture
        def my_fixture():
            return "fixture_value"
        
        # Fixture should be callable
        assert my_fixture() == "fixture_value"
    
    def test_fixture_with_scope(self):
        """Test fixture with scope."""
        from testagent import fixture
        
        @fixture(scope="session")
        def session_fixture():
            return "session_value"
        
        assert session_fixture() == "session_value"
        assert session_fixture._testagent_fixture_scope == "session"
    
    def test_fixture_generator(self):
        """Test fixture with setup/teardown."""
        from testagent import fixture
        
        setup_called = []
        teardown_called = []
        
        @fixture
        def my_fixture():
            setup_called.append(True)
            yield "value"
            teardown_called.append(True)
        
        # Use the fixture
        gen = my_fixture()
        value = next(gen)
        assert value == "value"
        assert setup_called == [True]
        
        # Teardown
        try:
            next(gen)
        except StopIteration:
            pass
        assert teardown_called == [True]
    
    def test_fixture_metadata(self):
        """Test fixture stores metadata."""
        from testagent import fixture
        
        @fixture(scope="module")
        def my_fixture():
            return 42
        
        assert my_fixture._testagent_fixture is True
        assert my_fixture._testagent_fixture_scope == "module"
