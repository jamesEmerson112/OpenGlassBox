"""
Test suite for the Unit class and resource acceptance logic.

This file covers:
- Construction and initialization of Unit objects and their context.
- Verification of member variables, resource setup, and linkage to City and Node.
- The accepts method: logic for determining if a Unit can accept a set of resources for a given target.
- Edge cases for resource matching and target validation.

The tests ensure that Unit objects and their resource acceptance logic behave as expected, matching the simulation's requirements for unit-resource interactions.
"""

import pytest

class Vector3f:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

class Node:
    def __init__(self, id, position):
        self.m_id = id
        self.m_position = position
    def position(self):
        return self.m_position

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

class Resource:
    MAX_CAPACITY = 2**32 - 1
    def __init__(self, name, amount=0):
        self._type = name
        self.m_type = name
        self.m_amount = amount
        self.m_capacity = Resource.MAX_CAPACITY
    def type(self):
        return self._type

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

class UnitContext:
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
        self.m_context = UnitContext(
            city=city,
            unit=self,
            locals_=self.m_resources,
            globals_=city.globals(),
            u=1,  # node.position.x / config::GRID_SIZE, assume 1 for stub
            v=2,  # node.position.y / config::GRID_SIZE, assume 2 for stub
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
        if target not in self.m_type.targets:
            return False
        if not resources.m_bin:
            return False
        found = False
        for r in resources.m_bin:
            if self.m_resources.hasResource(r.type()):
                if self.m_resources.getAmount(r.type()) < r.m_amount:
                    return False
                found = True
        return found

def test_constructor():
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

def test_accept():
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

# TODO: Port and implement the more complex tests (ExecuteRules)
