"""
Test suite for the Path, Node, and Way classes (graph structure).

This file covers:
- Construction and initialization of Node and Way objects.
- Path construction, node/way addition, and graph relationships.
- Verification of member variables, connectivity, and geometric properties.
- Unit addition to nodes and cross-reference validation.
- Path splitting, modification, and node movement.
- Graph traversal and relationship verification.

The tests ensure that the graph structure for paths, nodes, and ways is correctly
set up and that their behavior matches expectations from the original C++ simulation engine.
"""

import pytest
import math
from python.path import Path, Node, Way, PathType, WayType
from python.vector import Vector3f
from python.node import Node

# Mock classes for testing
class MockUnitType:
    def __init__(self, name):
        self.name = name
        self.color = 0xFF00FF
        self.radius = 2
        self.resources = MockResources()

    def __str__(self):
        return self.name

class MockResources:
    def __init__(self):
        self.capacities = {}
        self.amounts = {}

    def setCapacity(self, name, capacity):
        self.capacities[name] = capacity

    def addResource(self, name, amount):
        self.amounts[name] = amount

class MockUnit:
    def __init__(self, unit_type, node, city):
        self.m_type = unit_type
        self.m_node = node
        self.m_city = city
        node.addUnit(self)

    def type(self):
        return self.m_type.name

class MockCity:
    def __init__(self, name, grid_size_u, grid_size_v):
        self.m_name = name
        self.m_gridSizeU = grid_size_u
        self.m_gridSizeV = grid_size_v
        self.m_position = Vector3f(0, 0, 0)

def test_node_constructor():
    """Test Node constructor and initial state."""
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

def test_node_add_unit():
    """Test adding Units to Nodes."""
    # Create two Nodes
    n1 = Node(42, Vector3f(1.0, 2.0, 3.0))
    n2 = Node(43, Vector3f(2.0, 3.0, 4.0))
    assert len(n1.units()) == 0
    assert len(n2.units()) == 0

    # Create an Unit "house" holding resources "people" attached to Node1
    city = MockCity("Paris", 1, 1)
    unit_type = MockUnitType("house")
    unit_type.resources.setCapacity("people", 10)
    unit_type.resources.addResource("people", 10)
    u1 = MockUnit(unit_type, n1, city)

    # Check one Unit has been added to Node1
    assert len(n1.units()) == 1
    assert n1.m_units[0] is u1
    assert n1.units()[0] is u1
    assert n1.unit(0) is u1
    assert u1.m_node is n1
    assert u1.type() == "house"

    # Add Unit1 to Node2
    n2.addUnit(u1)
    assert len(n2.units()) == 1
    assert n2.m_units[0] is u1
    assert n2.units()[0] is u1
    assert n2.m_units[0].m_node is n1
    assert n2.m_units[0].type() == "house"

    # Add Unit2 to Node1
    u2 = MockUnit(unit_type, n2, city)
    n1.addUnit(u2)
    assert len(n1.m_units) == 2
    assert n1.m_units[0] is u1
    assert n1.m_units[1] is u2
    assert n1.units()[0] is u1
    assert n1.units()[1] is u2
    assert n1.m_units[0].type() == "house"
    assert n1.m_units[1].type() == "house"
    assert n1.m_units[0].m_node is n1
    assert n1.m_units[1].m_node is n2

def test_way_constructor():
    """Test Way constructor and initial state."""
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

def test_way_to_node():
    """Test finding Ways between Nodes."""
    # Create a path with several Nodes and Ways
    n1 = Node(42, Vector3f(1.0, 1.0, 0.0))
    n2 = Node(43, Vector3f(2.0, 2.0, 0.0))
    n3 = Node(44, Vector3f(3.0, 3.0, 0.0))
    n4 = Node(45, Vector3f(3.0, 4.0, 0.0))

    way_type = WayType("road")
    s1 = Way(55, way_type, n1, n2)
    s2 = Way(56, way_type, n1, n3)

    # Check that n1 has two neighboring Ways
    assert n1.getWayToNode(n2) is s1
    assert n1.getWayToNode(n3) is s2

    # Check that n4 has no neighboring Ways
    assert n4.getWayToNode(n3) is None

    # Check that n4 has no Way starting and leaving from it
    assert n4.getWayToNode(n4) is None

    # Add a loop Way
    s3 = Way(57, way_type, n4, n4)
    assert n4.getWayToNode(n4) is s3

    # Check that n1 has no Way starting and leaving from it
    assert n1.getWayToNode(n1) is None

def test_path_constructor():
    """Test Path constructor and initial state."""
    path_type = PathType("route")
    p = Path(path_type)
    assert p.type() == "route"
    assert len(p.m_nodes) == 0
    assert len(p.m_ways) == 0
    assert p.m_nextNodeId == 0
    assert p.m_nextWayId == 0

def test_path_adding():
    """Test adding Nodes and Ways to a Path."""
    path_type = PathType("route")
    p = Path(path_type)

    # Add 1st node to the path
    n1 = p.addNode(Vector3f(1.0, 1.0, 0.0))
    assert len(p.m_nodes) == 1
    assert p.m_nodes[0] is n1
    assert p.m_nodes[0].id() == 0
    assert len(p.m_ways) == 0
    assert p.m_nextNodeId == 1
    assert p.m_nextWayId == 0

    # Add 2nd node to the path
    n2 = p.addNode(Vector3f(2.0, 2.0, 0.0))
    assert len(p.m_nodes) == 2
    assert p.m_nodes[0] is n1
    assert p.m_nodes[1] is n2
    assert p.m_nodes[0].id() == 0
    assert p.m_nodes[1].id() == 1
    assert len(p.m_ways) == 0
    assert p.m_nextNodeId == 2
    assert p.m_nextWayId == 0

    # Add 1st Way to the path
    way_type = WayType("Dirt", 0xAAAAAA)
    s1 = p.addWay(way_type, n1, n2)
    assert len(p.m_nodes) == 2
    assert p.m_nodes[0].id() == 0
    assert p.m_nodes[1].id() == 1
    assert len(p.m_ways) == 1
    assert p.m_ways[0] is s1
    assert p.m_ways[0].id() == 0
    assert p.m_nextNodeId == 2
    assert p.m_nextWayId == 1

    # Add 2nd Way to the path
    s2 = p.addWay(way_type, n1, n2)
    assert len(p.m_nodes) == 2
    assert p.m_nodes[0].id() == 0
    assert p.m_nodes[1].id() == 1
    assert len(p.m_ways) == 2
    assert p.m_ways[0] is s1
    assert p.m_ways[1] is s2
    assert p.m_ways[0].id() == 0
    assert p.m_ways[1].id() == 1
    assert p.m_nextNodeId == 2
    assert p.m_nextWayId == 2

def test_path_split_way():
    """Test splitting a Way at a specific point."""
    path_type = PathType("route")
    p = Path(path_type)

    # Create a simple path with two nodes and a way
    n1 = p.addNode(Vector3f(1.0, 1.0, 0.0))
    n2 = p.addNode(Vector3f(1.0, 3.0, 0.0))
    way_type = WayType("Dirt", 0xAAAAAA)
    s1 = p.addWay(way_type, n1, n2)

    assert len(p.m_nodes) == 2
    assert len(p.m_ways) == 1

    # Split way at the beginning (0.0)
    # This should return the first node and not create new nodes or ways
    n3 = p.splitWay(s1, 0.0)
    assert n3 is n1
    assert len(p.m_nodes) == 2
    assert len(p.m_ways) == 1

    # Split way at the end (1.0)
    # This should return the second node and not create new nodes or ways
    n4 = p.splitWay(s1, 1.0)
    assert n4 is n2
    assert len(p.m_nodes) == 2
    assert len(p.m_ways) == 1

    # Split way in the middle (0.5)
    # This should create a new node and a new way
    n5 = p.splitWay(s1, 0.5)

    # Verify new node position
    assert n5 is not n1
    assert n5 is not n2
    assert n5.position().x == 1.0
    assert n5.position().y == 2.0
    assert n5.position().z == 0.0

    # Verify we now have 3 nodes and 2 ways
    assert len(p.m_nodes) == 3
    assert len(p.m_ways) == 2

def test_path_move_node():
    """Test moving a Node and verifying Way magnitudes update."""
    path_type = PathType("route")
    p = Path(path_type)

    # Create three nodes at the same position
    n1 = p.addNode(Vector3f(0.0, 0.0, 0.0))
    n2 = p.addNode(Vector3f(0.0, 0.0, 0.0))
    n3 = p.addNode(Vector3f(0.0, 0.0, 0.0))

    # Create two Ways with Node1 as a common node
    way_type = WayType("Dirt", 0xAAAAAA)
    s1 = p.addWay(way_type, n1, n2)
    s2 = p.addWay(way_type, n1, n3)

    # Check ways have zero magnitude initially
    assert math.isclose(s1.magnitude(), 0.0)
    assert math.isclose(s2.magnitude(), 0.0)

    # Move nodes
    n2.translate(Vector3f(1.0, 1.0, 0.0))
    n3.translate(Vector3f(-1.0, -1.0, 0.0))

    # Check that way magnitudes have been updated
    assert math.isclose(s1.magnitude(), math.sqrt(2.0))
    assert math.isclose(s2.magnitude(), math.sqrt(2.0))
