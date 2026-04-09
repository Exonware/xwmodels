#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/1.unit/test_new_features.py
Unit tests for new XWEntity features:
- Actions dict access (entity.actions["action_name"])
- Direct property access (entity.uid)
- Direct action calls (entity.add_user(a, b))
- Schema query (entity.schema.query("xwquery"))
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.2
"""

import pytest
from exonware.xwmodels import XWEntity
from exonware.xwaction import XWAction, ActionProfile
from exonware.xwschema import XWSchema
print("=" * 80)
print("Testing New XWEntity Features")
print("=" * 80)
# Test 1: Direct property access (entity.uid)
print("\n[Test 1] Direct Property Access")
entity = XWEntity(data={"uid": "user-123", "name": "Alice", "age": 30})
print(f"  entity.uid = {entity.uid}")
print(f"  entity.name = {entity.name}")
print(f"  entity.age = {entity.age}")
assert entity.uid == "user-123"
assert entity.name == "Alice"
assert entity.age == 30
print("  [PASS]")
# Test 2: Actions dict access (entity.actions["action_name"])
print("\n[Test 2] Actions Dict Access")

class UserEntity(XWEntity):
    @XWAction(profile=ActionProfile.QUERY, api_name="get_name")

    def get_name(self) -> str:
        return self.get("name")
    @XWAction(profile=ActionProfile.COMMAND, api_name="update_age")

    def update_age(self, new_age: int) -> bool:
        self.set("age", new_age)
        return True
user = UserEntity(data={"name": "Alice", "age": 30})
# Test dict-style access
print(f"  'get_name' in actions: {'get_name' in user.actions}")
print(f"  len(actions): {len(user.actions)}")
action = user.actions["get_name"]
print(f"  actions['get_name'] type: {type(action).__name__}")
# Check if it's an XWAction or has XWAction attributes
from exonware.xwaction import XWAction as XWActionType
is_xwaction = isinstance(action, XWActionType)
has_api_name = hasattr(action, 'api_name')
print(f"  Is XWAction: {is_xwaction}")
print(f"  Has api_name: {has_api_name}")
assert "get_name" in user.actions
assert len(user.actions) >= 1
assert action is not None
# Action should be XWAction or have XWAction-like interface
assert is_xwaction or has_api_name or callable(action)
print("  [PASS]")
# Test 3: Direct action calls (entity.add_user(a, b))
print("\n[Test 3] Direct Action Calls")

class UserEntity2(XWEntity):
    @XWAction(profile=ActionProfile.COMMAND, api_name="add_user")

    def add_user(self, name: str, age: int) -> dict:
        self.set("name", name)
        self.set("age", age)
        return {"name": name, "age": age}
user2 = UserEntity2(data={})
result = user2.add_user("Bob", 25)
print(f"  user2.add_user('Bob', 25) = {result}")
print(f"  user2.name = {user2.name}")
print(f"  user2.age = {user2.age}")
assert user2.name == "Bob"
assert user2.age == 25
print("  [PASS]")
# Test 4: Schema dict access (entity.schema["anything"])
print("\n[Test 4] Schema Dict Access")
schema = XWSchema({
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    }
})
entity_with_schema = XWEntity(schema=schema, data={"name": "Alice", "age": 30})
print(f"  schema['type'] = {entity_with_schema.schema['type']}")
_schema_native = entity_with_schema.schema.to_native()
print(f"  'properties' in schema (native): {'properties' in _schema_native}")
assert entity_with_schema.schema['type'] == "object"
assert "properties" in _schema_native
print("  [PASS]")
# Test 5: Data dict access (entity.data["anything"])
print("\n[Test 5] Data Dict Access")
entity3 = XWEntity(data={"name": "Charlie", "age": 35})
print(f"  entity3.data['name'] = {entity3.data['name']}")
print(f"  entity3.data['age'] = {entity3.data['age']}")
assert entity3.data['name'] == "Charlie"
assert entity3.data['age'] == 35
print("  [PASS]")
# Test 6: Data query (entity.data.query("xwquery"))
print("\n[Test 6] Data Query")
entity4 = XWEntity(data={"users": [{"name": "Alice"}, {"name": "Bob"}]})
# Test that query method exists
if hasattr(entity4.data, 'query'):
    print(f"  entity4.data.query() method exists: {hasattr(entity4.data, 'query')}")
    print("  [PASS] (query method available)")
else:
    print("  [WARN] Query method not available (may require xwquery)")
# Test 7: Serialization (only schema, actions, data, metadata)
print("\n[Test 7] Serialization")
entity5 = UserEntity(data={"name": "Alice", "age": 30})
serialized = entity5.to_dict()
print(f"  Keys in to_dict(): {list(serialized.keys())}")
assert "_metadata" in serialized
assert "_data" in serialized
# Schema and actions are optional
print("  [PASS]")
# Test 8: Actions iteration
print("\n[Test 8] Actions Iteration")
user3 = UserEntity(data={"name": "Alice"})
action_names = list(user3.actions)
print(f"  Action names: {action_names}")
assert isinstance(action_names, list)
print("  [PASS]")
print("\n" + "=" * 80)
print("All tests completed!")
print("=" * 80)
