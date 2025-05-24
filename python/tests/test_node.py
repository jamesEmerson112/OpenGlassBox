"""
Test suite for the Node class implementation.

This file covers:
- Creation and initialization of Node objects
- Connection management between nodes
- Unit attachment and management
- Node position operations and translation
- Way finding and node relationship operations
"""

import pytest
from ..node import Node
from ..vector import Vector3D as Vector3f


class TestNode:
    """Tests for the Node class implementation."""

    def test_constructor(self):
        """Test Node initialization with ID and position."""
        node_id = 42
        position = Vector3f(1.0, 2.0, 3.0)
        node = Node(node_id, position)

        assert node.id() == node_id
        assert node.position() is position
        assert node.m_ways == []
        assert node.m_units == []

    def test_add_unit(self):
        """Test unit attachment to node."""
        node = Node(1, Vector3f(0.0, 0.0, 0.0))
        mock_unit = "mock_unit"  # In real tests this would be a Unit instance

        node.add_unit(mock_unit)
        assert len(node.m_units) == 1
        assert node.m_units[0] == mock_unit

        # Test C++ compatibility alias
        node2 = Node(2, Vector3f(0.0, 0.0, 0.0))
        node2.addUnit(mock_unit)
        assert len(node2.m_units) == 1
        assert node2.m_units[0] == mock_unit

    def test_has_ways(self):
        """Test detection of connected ways."""
        node = Node(1, Vector3f(0.0, 0.0, 0.0))
        assert not node.has_ways()

        # Add a mock way
        mock_way = "mock_way"  # In real tests this would be a Way instance
        node.m_ways.append(mock_way)
        assert node.has_ways()

        # Test C++ compatibility alias
        assert node.hasWays()

    def test_translate(self):
        """Test node translation and way magnitude updates."""
        node = Node(1, Vector3f(1.0, 2.0, 3.0))

        class MockWay:
            def update_magnitude(self):
                self.updated = True

        mock_way = MockWay()
        node.m_ways.append(mock_way)

        node.translate(Vector3f(2.0, 3.0, 4.0))
        assert node.position() == Vector3f(3.0, 5.0, 7.0)
        assert hasattr(mock_way, 'updated')
        assert mock_way.updated

    def test_get_way_to_node(self):
        """Test finding a way between two nodes."""
        node1 = Node(1, Vector3f(0.0, 0.0, 0.0))
        node2 = Node(2, Vector3f(1.0, 1.0, 1.0))

        # No way yet
        assert node1.get_way_to_node(node2) is None

        # Add a mock way
        class MockWay:
            def __init__(self, from_node, to_node):
                self.m_from = from_node
                self.m_to = to_node

        way = MockWay(node1, node2)
        node1.m_ways.append(way)
        node2.m_ways.append(way)

        # Test finding the way
        assert node1.get_way_to_node(node2) is way
        assert node2.get_way_to_node(node1) is way

        # Test C++ compatibility alias
        assert node1.getWayToNode(node2) is way

    def test_unit_accessors(self):
        """Test unit access methods."""
        node = Node(1, Vector3f(0.0, 0.0, 0.0))
        unit1 = "unit1"
        unit2 = "unit2"

        node.add_unit(unit1)
        node.add_unit(unit2)

        assert node.units() == [unit1, unit2]
        assert node.unit(0) == unit1
        assert node.unit(1) == unit2
        assert node.unit(2) is None  # Out of bounds check

    def test_find_nearest_node(self):
        """Test finding the nearest node from a list."""
        node = Node(1, Vector3f(0.0, 0.0, 0.0))
        node2 = Node(2, Vector3f(1.0, 0.0, 0.0))
        node3 = Node(3, Vector3f(0.5, 0.0, 0.0))
        node4 = Node(4, Vector3f(2.0, 0.0, 0.0))

        # Empty list
        assert node.find_nearest_node([]) is None

        # Single node
        assert node.find_nearest_node([node2]) is node2

        # Multiple nodes
        assert node.find_nearest_node([node2, node3, node4]) is node3
        assert node.find_nearest_node([node2, node4]) is node2

    def test_connect_to(self):
        """Test connecting nodes with ways."""
        node1 = Node(1, Vector3f(0.0, 0.0, 0.0))
        node2 = Node(2, Vector3f(1.0, 0.0, 0.0))

        class MockWayType:
            pass

        class MockPath:
            def add_way(self, way_type, from_node, to_node):
                self.way_type = way_type
                self.from_node = from_node
                self.to_node = to_node
                # Create a mock way
                class MockWay:
                    def __init__(self, from_node, to_node):
                        self.m_from = from_node
                        self.m_to = to_node
                way = MockWay(from_node, to_node)
                from_node.m_ways.append(way)
                to_node.m_ways.append(way)
                return way

        way_type = MockWayType()
        path = MockPath()

        # Connect the nodes
        way = node1.connect_to(node2, way_type, path)
        assert way.m_from is node1
        assert way.m_to is node2
        assert path.way_type is way_type
        assert path.from_node is node1
        assert path.to_node is node2

        # Check that the nodes are connected
        assert node1.get_way_to_node(node2) is way
        assert node2.get_way_to_node(node1) is way

        # Check that connecting again returns the existing way
        way2 = node1.connect_to(node2, way_type, path)
        assert way2 is way

    def test_disconnect_from(self):
        """Test disconnecting nodes."""
        node1 = Node(1, Vector3f(0.0, 0.0, 0.0))
        node2 = Node(2, Vector3f(1.0, 0.0, 0.0))

        # Create a mock way
        class MockWay:
            def __init__(self, from_node, to_node):
                self.m_from = from_node
                self.m_to = to_node

        way = MockWay(node1, node2)
        node1.m_ways.append(way)
        node2.m_ways.append(way)

        # Check that the way exists
        assert node1.get_way_to_node(node2) is way

        # Disconnect the nodes
        node1.disconnect_from(node2)

        # Check that the way is gone
        assert node1.get_way_to_node(node2) is None
        assert node2.get_way_to_node(node1) is None
        assert way not in node1.m_ways
        assert way not in node2.m_ways

    def test_color(self):
        """Test node color method."""
        node = Node(1, Vector3f(0.0, 0.0, 0.0))
        assert isinstance(node.color(), int)
        assert node.color() == 0xAAAAAA  # Default color for nodes
