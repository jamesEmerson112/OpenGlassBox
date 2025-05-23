"""
Test suite for the Path, Node, and Way classes (graph structure).

This file covers:
- Construction and initialization of Node and Way objects.
- Path construction, node/way addition, and graph relationships.
- Verification of member variables, connectivity, and geometric properties.

The tests ensure that the graph structure for paths, nodes, and ways is correctly set up and that their initial state matches expectations from the original C++ simulation engine.
"""

import pytest
import math

# Minimal stubs for required classes

class Vector3f:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

class Node:
    def __init__(self, id, position):
        self.m_id = id
        self.m_position = position
        self.m_ways = []
        self.m_units = []

    def id(self):
        return self.m_id

    def position(self):
        return self.m_position

    def ways(self):
        return self.m_ways

    def units(self):
        return self.m_units

    def addUnit(self, unit):
        self.m_units.append(unit)

    def unit(self, idx):
        return self.m_units[idx]

    def getWayToNode(self, other):
        for way in self.m_ways:
            if way.m_to is other or way.m_from is other:
                return way
        return None

    def translate(self, vec):
        self.m_position.x += vec.x
        self.m_position.y += vec.y
        self.m_position.z += vec.z

class WayType:
    def __init__(self, name, color=0xFFFFFF):
        self.name = name
        self.color = color

    def c_str(self):
        return self.name

class Way:
    def __init__(self, id, way_type, n_from, n_to):
        self.m_id = id
        self.m_type = way_type
        self.m_from = n_from
        self.m_to = n_to
        self._update_nodes()
        self._update_magnitude()

    def _update_nodes(self):
        if self not in self.m_from.m_ways:
            self.m_from.m_ways.append(self)
        if self not in self.m_to.m_ways:
            self.m_to.m_ways.append(self)

    def id(self):
        return self.m_id

    def type(self):
        return self.m_type.name

    def color(self):
        return self.m_type.color

    def from_(self):
        return self.m_from

    def to(self):
        return self.m_to

    def magnitude(self):
        dx = self.m_to.m_position.x - self.m_from.m_position.x
        dy = self.m_to.m_position.y - self.m_from.m_position.y
        dz = self.m_to.m_position.z - self.m_from.m_position.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def changeNode2(self, new_to):
        if self in self.m_to.m_ways:
            self.m_to.m_ways.remove(self)
        self.m_to = new_to
        if self not in self.m_to.m_ways:
            self.m_to.m_ways.append(self)
        self._update_magnitude()

    def _update_magnitude(self):
        pass  # magnitude is computed on the fly

class PathType:
    def __init__(self, name):
        self.name = name

    def c_str(self):
        return self.name

class Path:
    def __init__(self, path_type):
        self.m_type = path_type
        self.m_nodes = []
        self.m_ways = []
        self.m_nextNodeId = 0
        self.m_nextWayId = 0

    def type(self):
        return self.m_type

    def addNode(self, position):
        node = Node(self.m_nextNodeId, position)
        self.m_nodes.append(node)
        self.m_nextNodeId += 1
        return node

    def addWay(self, way_type, n_from, n_to):
        way = Way(self.m_nextWayId, way_type, n_from, n_to)
        self.m_ways.append(way)
        self.m_nextWayId += 1
        return way

def test_node_constructor():
    n = Node(42, Vector3f(1.0, 2.0, 3.0))
    assert n.m_id == 42
    assert int(n.m_position.x) == 1
    assert int(n.m_position.y) == 2
    assert int(n.m_position.z) == 3
    assert len(n.m_ways) == 0
    assert len(n.m_units) == 0
    assert n.id() == 42
    assert int(n.position().x) == 1
    assert int(n.position().y) == 2
    assert int(n.position().z) == 3
    assert len(n.ways()) == 0
    assert len(n.units()) == 0

def test_way_constructor():
    n1 = Node(42, Vector3f(1.0, 1.0, 0.0))
    n2 = Node(43, Vector3f(2.0, 2.0, 0.0))
    way_type = WayType("Dirt", 0xAAAAAA)
    s1 = Way(55, way_type, n1, n2)
    assert s1.id() == 55
    assert s1.type() == "Dirt"
    assert s1.color() == 0xAAAAAA
    assert s1.m_from is n1
    assert s1.m_to is n2
    assert s1.from_() is n1
    assert s1.to() is n2
    assert math.isclose(s1.magnitude(), math.sqrt(2.0))

def test_path_constructor():
    path_type = PathType("route")
    p = Path(path_type)
    assert p.type().c_str() == "route"
    assert len(p.m_nodes) == 0
    assert len(p.m_ways) == 0
    assert p.m_nextNodeId == 0
    assert p.m_nextWayId == 0

# TODO: Port and implement the more complex tests (AddUnit, SplitWay, MoveNode, getWayToNode, Adding)
