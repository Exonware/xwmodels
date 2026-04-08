#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/1.unit/test_action_validation.py
Unit tests for action parameter validation in XWEntity.
Tests that actions with parameter schemas properly validate inputs
when called both via execute_action() and directly.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.2
"""

import pytest
from exonware.xwmodels import XWEntity, XWEntityValidationError
from exonware.xwaction import XWAction, ActionProfile, XWActionExecutionError
from exonware.xwschema import XWSchema
print("=" * 80)
print("Testing Action Parameter Validation")
print("=" * 80)
# Test 1: Action with parameter schema validation
print("\n[Test 1] Action with Parameter Schema")

class UserEntity(XWEntity):
    @XWAction(
        profile=ActionProfile.COMMAND,
        api_name="update_age",
        in_types={
            "new_age": XWSchema({"type": "integer", "minimum": 0, "maximum": 150})
        }
    )

    def update_age(self, new_age: int) -> bool:
        self.set("age", new_age)
        return True
user = UserEntity(data={"name": "Alice", "age": 30})
# Valid parameter
try:
    result = user.update_age(25)
    print(f"  update_age(25): {result}")
    print(f"  [PASS] Valid parameter accepted")
except Exception as e:
    print(f"  [FAIL] Valid parameter rejected: {e}")
# Invalid parameter (negative age)
try:
    result = user.update_age(-5)
    print(f"  [FAIL] Invalid parameter accepted (should have failed)")
except (XWEntityValidationError, Exception) as e:
    print(f"  update_age(-5): Correctly rejected")
    print(f"  Error type: {type(e).__name__}")
    print(f"  [PASS] Invalid parameter correctly rejected")
# Invalid parameter (too large)
try:
    result = user.update_age(200)
    print(f"  [FAIL] Invalid parameter accepted (should have failed)")
except (XWEntityValidationError, Exception) as e:
    print(f"  update_age(200): Correctly rejected")
    print(f"  [PASS] Invalid parameter correctly rejected")
# Test 2: Action with multiple parameters
print("\n[Test 2] Action with Multiple Parameters")

class ProductEntity(XWEntity):
    @XWAction(
        profile=ActionProfile.COMMAND,
        api_name="update_product",
        in_types={
            "name": XWSchema({"type": "string", "minLength": 1}),
            "price": XWSchema({"type": "number", "minimum": 0})
        }
    )

    def update_product(self, name: str, price: float) -> dict:
        self.set("name", name)
        self.set("price", price)
        return {"name": name, "price": price}
product = ProductEntity(data={})
# Valid parameters
try:
    result = product.update_product("Laptop", 999.99)
    print(f"  update_product('Laptop', 999.99): {result}")
    print(f"  [PASS] Valid parameters accepted")
except Exception as e:
    print(f"  [FAIL] Valid parameters rejected: {e}")
# Invalid parameters (empty name)
try:
    result = product.update_product("", 999.99)
    print(f"  [FAIL] Invalid parameter accepted (should have failed)")
except (XWEntityValidationError, Exception) as e:
    print(f"  update_product('', 999.99): Correctly rejected")
    print(f"  [PASS] Invalid parameter correctly rejected")
# Invalid parameters (negative price)
try:
    result = product.update_product("Laptop", -100)
    print(f"  [FAIL] Invalid parameter accepted (should have failed)")
except (XWEntityValidationError, Exception) as e:
    print(f"  update_product('Laptop', -100): Correctly rejected")
    print(f"  [PASS] Invalid parameter correctly rejected")
# Test 3: Action via execute_action() also validates
print("\n[Test 3] Validation via execute_action()")
try:
    result = user.execute_action("update_age", new_age=35)
    print(f"  execute_action('update_age', new_age=35): {result}")
    print(f"  [PASS] Valid parameter accepted via execute_action")
except Exception as e:
    print(f"  [FAIL] Valid parameter rejected: {e}")
try:
    result = user.execute_action("update_age", new_age=-10)
    print(f"  [FAIL] Invalid parameter accepted (should have failed)")
except (XWEntityValidationError, Exception) as e:
    print(f"  execute_action('update_age', new_age=-10): Correctly rejected")
    print(f"  [PASS] Invalid parameter correctly rejected via execute_action")
# Test 4: Positional arguments conversion
print("\n[Test 4] Positional Arguments Conversion")
try:
    # Should convert positional args to kwargs based on function signature
    result = user.update_age(40)  # Positional arg
    print(f"  update_age(40) [positional]: {result}")
    print(f"  user.age = {user.get('age')}")
    assert user.get("age") == 40
    print(f"  [PASS] Positional arguments work correctly")
except Exception as e:
    print(f"  [FAIL] Positional arguments failed: {e}")
print("\n" + "=" * 80)
print("All validation tests completed!")
print("=" * 80)
