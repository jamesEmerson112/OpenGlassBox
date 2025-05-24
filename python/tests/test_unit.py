"""
Test suite for the Unit class and resource management logic.

This file covers:
- Construction and initialization of Unit objects and their context.
- Verification of member variables, resource setup, and linkage to City and Node.
- The accepts method: logic for determining if a Unit can accept a set of resources for a given target.
- Edge cases for resource matching and target validation.
- Rule execution based on tick count and validation results.
- Failure callbacks when rules fail validation.

The tests ensure that Unit objects, their resource acceptance logic, and rule execution
behave as expected, matching the simulation's requirements for unit interactions.
"""

import pytest
from unittest.mock import Mock, call

class Vector3f:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

class Node:
    def __init__(self, id, position):
        self.m_id = id
        self.m_position = position
        self.m_units = []

    def position(self):
        return self.m_position

    def add_unit(self, unit):
        self.m_units.append(unit)

class Resources:
    def __init__(self):
        self.m_bin = []

    def addResource(self, name, amount):
        r = Resource(name, amount)
        self.m_bin.append(r)
        return r

    def getAmount(self, name):
        for r in self.m_bin:
            if r.type() == name:
                return r.m_amount
        return 0

    def getCapacity(self, name):
        for r in self.m_bin:
            if r.type() == name:
                return r.m_capacity
        return 0

    def hasResource(self, name):
        for r in self.m_bin:
            if r.type() == name:
                return True
        return False

    def can_add_some_resources(self, resources):
        if not resources.m_bin:
            return False
        found = False
        for r in resources.m_bin:
            if self.hasResource(r.type()):
                found = True
        return found

class Resource:
    MAX_CAPACITY = 2**32 - 1
    def __init__(self, name, amount=0):
        self._type = name
        self.m_type = name
        self.m_amount = amount
        self.m_capacity = Resource.MAX_CAPACITY

    def type(self):
        return self._type

    def amount(self):
        return self.m_amount

class UnitType:
    def __init__(self, name):
        self.name = name
        self.color = None
        self.radius = None
        self.resources = Resources()
        self.rules = []
        self.targets = []

class City:
    def __init__(self, name, u, v):
        self._name = name
        self._u = u
        self._v = v
        self._globals = Resources()

    def globals(self):
        return self._globals

    def world2mapPosition(self, position, u_out, v_out):
        # Simple mock implementation - in real code this would convert world coords to map coords
        u_out.append(1)
        v_out.append(2)

class RuleContext:
    def __init__(self, city, unit, locals_, globals_, u, v, radius):
        self.city = city
        self.unit = unit
        self.locals = locals_
        self.globals = globals_
        self.u = u
        self.v = v
        self.radius = radius

class Unit:
    def __init__(self, unit_type, node, city):
        self.m_type = unit_type
        self.m_node = node
        self.m_resources = Resources()
        for r in unit_type.resources.m_bin:
            self.m_resources.addResource(r.type(), r.m_amount)

        # Register the unit with the node
        self.m_node.add_unit(self)

        # Initialize the context
        self.m_context = RuleContext(
            city=city,
            unit=self,
            locals_=self.m_resources,
            globals_=city.globals(),
            u=1,  # From world2mapPosition
            v=2,  # From world2mapPosition
            radius=unit_type.radius
        )
        self.m_ticks = 0

    def type(self):
        return self.m_type.name

    def color(self):
        return self.m_type.color

    def node(self):
        return self.m_node

    def position(self):
        return self.m_node.position()

    def resources(self):
        return self.m_resources

    def accepts(self, target, resources):
        # Check if the unit accepts this target type
        if target not in self.m_type.targets:
            return False

        # Check if the unit can add any of these resources
        return self.m_resources.can_add_some_resources(resources)

    def execute_rules(self):
        """Execute simulation rules for this unit."""
        self.m_ticks += 1

        # Execute rules in reverse order (as in the C++ implementation)
        for i in range(len(self.m_type.rules) - 1, -1, -1):
            rule = self.m_type.rules[i]

            # Execute rule if tick counter matches rule rate
            if self.m_ticks % rule.rate() == 0:
                if hasattr(rule, 'validate') and callable(rule.validate):
                    # Command rule with validation
                    if rule.validate(self.m_context):
                        rule.execute(self.m_context)
                    elif hasattr(rule, 'on_fail') and rule.on_fail is not None:
                        rule.on_fail.execute(self.m_context)
                else:
                    # Simple rule without validation
                    rule.execute(self.m_context)

# Mock classes for testing rule execution
class MockCommand:
    def __init__(self, validate_result=True):
        self.validate = Mock(return_value=validate_result)
        self.execute = Mock()
        self.on_fail = None

    def rate(self):
        return 4  # Default rate for testing

class MockRule:
    def __init__(self, rate_value=4):
        self.execute = Mock()
        self._rate = rate_value

    def rate(self):
        return self._rate

def test_constructor():
    """Test Unit constructor and initialization."""
    city = City("Paris", 4, 4)
    node = Node(42, Vector3f(3.0, 4.0, 5.0))
    unit_type = UnitType("unit")
    unit_type.color = 42
    unit_type.radius = 2
    unit_type.resources.addResource("car", 5)
    unit_type.targets.append("foo")

    u = Unit(unit_type, node, city)

    assert u.m_type.name == "unit"
    assert u.m_type.color == 42
    assert u.m_type.radius == 2
    assert len(u.m_type.resources.m_bin) == 1
    assert u.m_type.resources.m_bin[0].type() == "car"
    assert u.m_type.resources.m_bin[0].m_amount == 5
    assert len(u.m_type.rules) == 0
    assert len(u.m_type.targets) == 1
    assert u.m_type.targets[0] == "foo"
    assert u.m_node is node
    assert len(u.m_resources.m_bin) == 1
    assert u.m_resources.m_bin[0].type() == "car"
    assert u.m_resources.m_bin[0].m_amount == 5
    assert u.m_context.city is city
    assert u.m_context.unit is u
    assert u.m_context.locals is u.m_resources
    assert u.m_context.globals is city.globals()
    assert u.m_context.u == 1
    assert u.m_context.v == 2
    assert u.m_context.radius == 2
    assert u.m_ticks == 0

    assert u.type() == "unit"
    assert u.color() == 42
    assert u.node() is node
    assert int(u.position().x) == int(node.position().x)
    assert int(u.position().y) == int(node.position().y)
    assert int(u.position().z) == int(node.position().z)
    assert u.m_type.resources.getAmount("car") == 5
    assert len(u.m_resources.m_bin) == 1
    assert u.resources().getAmount("car") == 5

    # Verify unit is registered with node
    assert u in node.m_units

def test_accept():
    """Test the accepts method for resource acceptance logic."""
    city = City("Paris", 4, 4)
    node = Node(42, Vector3f(3.0, 4.0, 5.0))
    unit_type = UnitType("unit")
    unit_type.resources.addResource("car", 5)
    unit_type.targets.append("foo")
    u = Unit(unit_type, node, city)

    r0 = Resources()
    r1 = Resources(); r1.addResource("car", 5)
    r2 = Resources(); r2.addResource("oil", 5)

    assert u.accepts("foo", r0) is False
    assert u.accepts("foo", r1) is True
    assert u.accepts("bar", r1) is False
    assert u.accepts("foo", r2) is False

    r2.addResource("car", 5)
    assert u.accepts("foo", r2) is True

def test_execute_rules():
    """Test rule execution based on tick count and validation results."""
    city = City("Paris", 4, 4)
    node = Node(42, Vector3f(3.0, 4.0, 5.0))

    # Case 1: OnFail callback is None
    cmd1 = MockCommand()
    unit_type1 = UnitType("unit1")
    unit_type1.rules.append(cmd1)
    u1 = Unit(unit_type1, node, city)

    # Ticks don't match rule rate yet
    u1.m_ticks = 2
    u1.execute_rules()
    assert u1.m_ticks == 3
    cmd1.validate.assert_not_called()
    cmd1.execute.assert_not_called()

    # Ticks match rate but validation fails
    u1.m_ticks = 3
    cmd1.validate.return_value = False
    u1.execute_rules()
    assert u1.m_ticks == 4
    cmd1.validate.assert_called_once()
    cmd1.execute.assert_not_called()

    # Reset mocks
    cmd1.validate.reset_mock()
    cmd1.execute.reset_mock()

    # Ticks match rate and validation succeeds
    u1.m_ticks = 3
    cmd1.validate.return_value = True
    u1.execute_rules()
    assert u1.m_ticks == 4
    cmd1.validate.assert_called_once()
    cmd1.execute.assert_called_once()

    # Case 2: OnFail callback is provided
    cmd2 = MockCommand(validate_result=False)
    on_fail = MockRule()
    cmd2.on_fail = on_fail
    unit_type2 = UnitType("unit2")
    unit_type2.rules.append(cmd2)
    u2 = Unit(unit_type2, node, city)

    # Ticks match rate but validation fails, should call on_fail
    u2.m_ticks = 3
    u2.execute_rules()
    assert u2.m_ticks == 4
    cmd2.validate.assert_called_once()
    cmd2.execute.assert_not_called()
    on_fail.execute.assert_called_once()

    # Case 3: Multiple rules with different rates
    rule1 = MockRule(rate_value=2)
    rule2 = MockRule(rate_value=3)
    unit_type3 = UnitType("unit3")
    unit_type3.rules.append(rule1)
    unit_type3.rules.append(rule2)
    u3 = Unit(unit_type3, node, city)

    # Tick 1: No rules execute
    u3.m_ticks = 0
    u3.execute_rules()
    assert u3.m_ticks == 1
    rule1.execute.assert_not_called()
    rule2.execute.assert_not_called()

    # Tick 2: Rule1 executes (rate=2)
    u3.execute_rules()
    assert u3.m_ticks == 2
    rule1.execute.assert_called_once()
    rule2.execute.assert_not_called()

    # Reset mocks
    rule1.execute.reset_mock()
    rule2.execute.reset_mock()

    # Tick 3: Rule2 executes (rate=3)
    u3.execute_rules()
    assert u3.m_ticks == 3
    rule1.execute.assert_not_called()
    rule2.execute.assert_called_once()

    # Reset mocks
    rule1.execute.reset_mock()
    rule2.execute.reset_mock()

    # Tick 4: Rule1 executes (rate=2)
    u3.execute_rules()
    assert u3.m_ticks == 4
    rule1.execute.assert_called_once()
    rule2.execute.assert_not_called()

    # Reset mocks
    rule1.execute.reset_mock()
    rule2.execute.reset_mock()

    # Tick 6: Both rules execute (rate=2 and rate=3 both divide 6)
    u3.m_ticks = 5
    u3.execute_rules()
    assert u3.m_ticks == 6
    rule1.execute.assert_called_once()
    rule2.execute.assert_called_once()
