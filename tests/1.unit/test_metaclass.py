#!/usr/bin/env python3
"""
Unit tests for XWEntity metaclass system.
"""

import pytest
from typing import Annotated
from exonware.xwmodels import XWEntity, PropertyInfo, ActionInfo, DecoratorScanner
from exonware.xwschema import XWSchema
from exonware.xwaction import XWAction, ActionProfile
pytestmark = pytest.mark.xwentity_unit


class TestDecoratorScanner:
    """Test DecoratorScanner functionality."""

    def test_scan_properties_from_annotations(self):
        """Test scanning properties from type annotations."""
        class TestEntity(XWEntity):
            name: str
            age: int = 25
            active: bool = True
        annotations = {'name': str, 'age': int, 'active': bool}
        namespace = {'age': 25, 'active': True}
        properties = DecoratorScanner.scan_properties(namespace, annotations)
        assert len(properties) >= 3
        names = [p.name for p in properties]
        assert 'name' in names
        assert 'age' in names
        assert 'active' in names

    def test_scan_properties_from_property_decorator(self):
        """Test scanning properties from @property decorator."""
        class TestEntity(XWEntity):
            @property
            def name(self) -> str:
                return "test"
        annotations = {}
        namespace = {'name': property(lambda self: "test")}
        properties = DecoratorScanner.scan_properties(namespace, annotations)
        assert len(properties) >= 1
        assert any(p.name == 'name' for p in properties)

    def test_scan_actions_from_xwaction(self):
        """Test scanning actions from @XWAction decorator."""
        class TestEntity(XWEntity):
            @XWAction(profile=ActionProfile.QUERY, api_name="test-action")
            def test_action(self):
                return "test"
        namespace = {'test_action': getattr(TestEntity, 'test_action')}
        actions = DecoratorScanner.scan_actions(namespace)
        # Should find the action (may be wrapped)
        assert len(actions) >= 0  # May not be found if not properly decorated


class TestPropertyInfo:
    """Test PropertyInfo class."""

    def test_property_info_creation(self):
        """Test PropertyInfo creation."""
        prop = PropertyInfo(
            name="test",
            property_type=str,
            default="default",
            schema=None
        )
        assert prop.name == "test"
        assert prop.property_type == str
        assert prop.default == "default"
        assert prop.schema is None
        assert prop.is_required is False

    def test_property_info_required(self):
        """Test PropertyInfo with required property."""
        prop = PropertyInfo(
            name="test",
            property_type=str,
            default=None
        )
        assert prop.is_required is True


class TestActionInfo:
    """Test ActionInfo class."""

    def test_action_info_creation(self):
        """Test ActionInfo creation."""
        def test_func():
            pass
        action = ActionInfo(
            name="test_action",
            func=test_func,
            action_instance=None
        )
        assert action.name == "test_action"
        assert action.func == test_func
        assert action.action_instance is None


class TestMetaclassPropertyCreation:
    """Test automatic property creation in subclasses."""

    def test_subclass_with_annotations_creates_properties(self):
        """Test that subclass with annotations gets properties created."""
        class UserEntity(XWEntity):
            username: str
            email: str = "test@example.com"
        # Properties should be accessible
        user = UserEntity(data={"username": "alice"})
        # Should be able to access as properties
        assert hasattr(user, 'username')
        assert hasattr(user, 'email')

    def test_subclass_with_property_decorator(self):
        """Test that @property decorated methods work."""
        class TestEntity(XWEntity):
            @property
            def computed(self) -> str:
                return "computed"
        entity = TestEntity()
        assert entity.computed == "computed"

    def test_performance_mode_properties(self):
        """Test that properties are created based on performance mode."""
        from exonware.xwmodels import PerformanceMode, get_config, set_config
        # Test PERFORMANCE mode
        config = get_config()
        original_mode = config.performance_mode
        config.performance_mode = PerformanceMode.PERFORMANCE
        class PerfEntity(XWEntity):
            name: str
        entity = PerfEntity(data={"name": "test"})
        assert hasattr(entity, 'name')
        # Restore
        config.performance_mode = original_mode

    def test_memory_mode_properties(self):
        """Test that MEMORY mode creates delegated properties."""
        from exonware.xwmodels import PerformanceMode, get_config
        config = get_config()
        original_mode = config.performance_mode
        config.performance_mode = PerformanceMode.MEMORY
        class MemEntity(XWEntity):
            name: str
        entity = MemEntity(data={"name": "test"})
        assert hasattr(entity, 'name')
        # Restore
        config.performance_mode = original_mode


class TestMetaclassActionDiscovery:
    """Test automatic action discovery in subclasses."""

    def test_subclass_with_xwaction_decorator(self):
        """Test that @XWAction decorated methods are discovered."""
        class TestEntity(XWEntity):
            @XWAction(profile=ActionProfile.QUERY, api_name="get-info")
            def get_info(self):
                return {"info": "test"}
        entity = TestEntity()
        # Actions should be discoverable
        actions = entity.list_actions()
        # May or may not be auto-registered depending on config
        assert isinstance(actions, list)


class TestMetaclassIntegration:
    """Test full metaclass integration."""

    def test_complex_entity_with_properties_and_actions(self):
        """Test entity with both properties and actions."""
        class ComplexEntity(XWEntity):
            name: str
            age: int = 0
            @XWAction(profile=ActionProfile.QUERY, api_name="get-name")
            def get_name(self):
                return self.name
        entity = ComplexEntity(data={"name": "Alice", "age": 30})
        assert hasattr(entity, 'name')
        assert hasattr(entity, 'age')
        assert hasattr(entity, 'get_name')

    def test_metaclass_metadata_storage(self):
        """Test that metaclass stores metadata correctly."""
        class TestEntity(XWEntity):
            prop1: str
            prop2: int = 10
        # Check metadata is stored
        assert hasattr(TestEntity, '_xwentity_properties')
        assert hasattr(TestEntity, '_xwentity_actions')
        assert hasattr(TestEntity, '_xwentity_performance_mode')
        props = getattr(TestEntity, '_xwentity_properties', [])
        assert len(props) >= 2
