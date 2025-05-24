"""
Test suite for the Dijkstra pathfinding algorithm.

This file covers:
- Basic pathfinding between nodes
- Finding nodes with units that accept specific resources
- Handling cases where no path exists
- Path selection when multiple paths are available
- Random fallback when no target is found
"""

import pytest
from unittest.mock import MagicMock, patch

from ..dijkstra import Dijkstra
from ..node import Node
from ..vector import Vector3D
from ..resources import Resources


class MockWay:
    """Mock Way class for testing."""

    def __init__(self, from_node, to_node, magnitude_value=1.0):
        self.m_from = from_node
        self.m_to = to_node
        self._magnitude = magnitude_value

        # Ensure this way is registered with both nodes
        if self not in from_node.m_ways:
            from_node.m_ways.append(self)
        if self not in to_node.m_ways:
            to_node.m_ways.append(self)

    def from_(self):
        return self.m_from

    def to(self):
        return self.m_to

    def magnitude(self):
        return self._magnitude


class MockUnit:
    """Mock Unit class for testing."""

    def __init__(self, accepts_resources=None):
        self.acceptable_resources = accepts_resources or []

    def accepts(self, target, resources):
        """Mock accepts method."""
        return target in self.acceptable_resources


def test_init():
    """Test the initialization of the Dijkstra class."""
    d = Dijkstra()
    assert d.m_closed_set == set()
    assert d.m_open_set == []
    assert d.m_came_from == {}
    assert d.m_score_from_start == {}
    assert d.m_score_plus_heuristic_from_start == {}


def test_basic_pathfinding():
    """Test basic pathfinding between nodes."""
    # Create a simple path: A -- B -- C
    node_a = Node(1, Vector3D(0, 0, 0))
    node_b = Node(2, Vector3D(1, 0, 0))
    node_c = Node(3, Vector3D(2, 0, 0))

    # Add a unit to node C that accepts "resource1"
    unit_c = MockUnit(["resource1"])
    node_c.add_unit(unit_c)

    # Create ways between nodes
    way_ab = MockWay(node_a, node_b)
    way_bc = MockWay(node_b, node_c)

    # Create resources
    resources = Resources()
    resources.addResource("resource1", 1)

    # Test pathfinding from A to C (should return B as next step)
    d = Dijkstra()
    next_node = d.find_next_point(node_a, "resource1", resources)
    assert next_node is node_b


def test_direct_target():
    """Test when the starting node has the target unit."""
    # Create a node with a unit that accepts "resource1"
    node_a = Node(1, Vector3D(0, 0, 0))
    unit_a = MockUnit(["resource1"])
    node_a.add_unit(unit_a)

    # Create resources
    resources = Resources()
    resources.addResource("resource1", 1)

    # Test pathfinding from A (should return A since it already has the target)
    d = Dijkstra()
    next_node = d.find_next_point(node_a, "resource1", resources)
    assert next_node is node_a


def test_multiple_paths():
    """Test when multiple paths to the target exist."""
    # Create a diamond-shaped network: A -- B -- D
    #                                   \       /
    #                                    -- C --
    node_a = Node(1, Vector3D(0, 0, 0))
    node_b = Node(2, Vector3D(1, 1, 0))
    node_c = Node(3, Vector3D(1, -1, 0))
    node_d = Node(4, Vector3D(2, 0, 0))

    # Add a unit to node D that accepts "resource1"
    unit_d = MockUnit(["resource1"])
    node_d.add_unit(unit_d)

    # Create ways between nodes
    way_ab = MockWay(node_a, node_b)
    way_ac = MockWay(node_a, node_c)
    way_bd = MockWay(node_b, node_d, 2.0)  # Longer path through B
    way_cd = MockWay(node_c, node_d, 1.0)  # Shorter path through C

    # Create resources
    resources = Resources()
    resources.addResource("resource1", 1)

    # Test pathfinding from A to D (should choose the shorter path through C)
    d = Dijkstra()
    next_node = d.find_next_point(node_a, "resource1", resources)
    assert next_node is node_c


def test_no_path():
    """Test when no path to a target exists."""
    # Create disconnected nodes
    node_a = Node(1, Vector3D(0, 0, 0))
    node_b = Node(2, Vector3D(1, 0, 0))

    # Add a unit to node B that accepts "resource1"
    unit_b = MockUnit(["resource1"])
    node_b.add_unit(unit_b)

    # Create resources
    resources = Resources()
    resources.addResource("resource1", 1)

    # Test pathfinding from A to B (should return None as there's no path)
    d = Dijkstra()
    next_node = d.find_next_point(node_a, "resource1", resources)
    assert next_node is None


def test_random_fallback():
    """Test random fallback when no target is found."""
    # Create a network with no target units
    node_a = Node(1, Vector3D(0, 0, 0))
    node_b = Node(2, Vector3D(1, 0, 0))
    node_c = Node(3, Vector3D(0, 1, 0))

    # Create ways connecting to multiple neighbors
    way_ab = MockWay(node_a, node_b)
    way_ac = MockWay(node_a, node_c)

    # Create resources
    resources = Resources()
    resources.addResource("resource1", 1)

    # Mock random.choice to return a consistent result for testing
    with patch("random.choice", return_value=way_ab):
        d = Dijkstra()
        next_node = d.find_next_point(node_a, "resource1", resources)
        assert next_node is node_b


def test_long_path():
    """Test pathfinding with a longer, more complex path."""
    # Create a more complex path: A -- B -- C -- D -- E -- F
    nodes = [Node(i, Vector3D(i, 0, 0)) for i in range(6)]

    # Connect nodes in sequence
    ways = []
    for i in range(5):
        ways.append(MockWay(nodes[i], nodes[i+1]))

    # Add a unit to the last node that accepts "resource1"
    unit_f = MockUnit(["resource1"])
    nodes[5].add_unit(unit_f)

    # Create resources
    resources = Resources()
    resources.addResource("resource1", 1)

    # Test pathfinding from A to F (should return B as next step)
    d = Dijkstra()
    next_node = d.find_next_point(nodes[0], "resource1", resources)
    assert next_node is nodes[1]


def test_heuristic_calculation():
    """Test the heuristic calculation used by Dijkstra."""
    node_a = Node(1, Vector3D(0, 0, 0))
    node_b = Node(2, Vector3D(3, 4, 0))

    d = Dijkstra()
    # Distance should be sqrt(3^2 + 4^2) = 5, and heuristic should be 25 (squared)
    assert d._heuristic(node_a, node_b) == 25
