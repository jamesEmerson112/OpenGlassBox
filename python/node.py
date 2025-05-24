"""
Node module for OpenGlassBox simulation engine.

This module defines the Node class which represents connection points in the transportation
network. Nodes are positioned in world space, connect Ways together, and may have
Units attached to them (like buildings, factories, etc).
"""

from typing import List, Dict, Optional, Any, Tuple
import math

from .vector import Vector3D as Vector3f


class Node:
    """
    Node class representing vertices in the path graph.

    Nodes define connection points in the transportation network.
    They store their position in the world, track connected Ways,
    and may have Units attached to them.
    """

    def __init__(self, node_id: int, position: Vector3f):
        """
        Initialize a node with ID and position.

        Args:
            node_id: Unique identifier for this node
            position: The node's position in world space
        """
        self.m_id = node_id
        self.m_position = position
        self.m_ways: List[Any] = []  # Will be populated with references to Way instances
        self.m_units: List[Any] = []  # Will be populated with references to Unit instances

    def add_unit(self, unit: Any) -> None:
        """
        Attach a Unit to this node.

        Args:
            unit: The Unit to attach to this node
        """
        self.m_units.append(unit)

    # Alias for C++ compatibility
    addUnit = add_unit

    def translate(self, direction: Vector3f) -> None:
        """
        Move the node by the specified direction vector.

        Args:
            direction: Vector representing the direction and magnitude of movement
        """
        self.m_position += direction
        # Update magnitude of all connected ways
        for way in self.m_ways:
            way.update_magnitude()

    def get_way_to_node(self, other_node: 'Node') -> Optional[Any]:
        """
        Find a way connecting this node to another specified node.

        Args:
            other_node: The node to find a connection to

        Returns:
            The Way object connecting the nodes, or None if no connection exists
        """
        for way in self.m_ways:
            if (way.m_from is other_node and way.m_to is self) or \
               (way.m_to is other_node and way.m_from is self):
                return way
        return None

    # Alias for C++ compatibility
    getWayToNode = get_way_to_node

    def has_ways(self) -> bool:
        """
        Check if this node has any ways connected to it.

        Returns:
            True if the node has at least one connected Way, False otherwise
        """
        return len(self.m_ways) > 0

    # Alias for C++ compatibility
    hasWays = has_ways

    def get_map_position(self, grid_size_u: int, grid_size_v: int) -> Tuple[int, int]:
        """
        Convert world position to map coordinates.

        Args:
            grid_size_u: The grid size in the U direction
            grid_size_v: The grid size in the V direction

        Returns:
            Tuple of (u, v) map coordinates
        """
        # Import config here to avoid circular imports
        from . import config

        # Calculate grid coordinates from world position
        u = int(self.m_position.x / config.GRID_SIZE)
        v = int(self.m_position.y / config.GRID_SIZE)

        # Clamp to grid boundaries
        u = max(0, min(u, grid_size_u - 1))
        v = max(0, min(v, grid_size_v - 1))

        return u, v

    # Alias for C++ compatibility
    getMapPosition = get_map_position

    def id(self) -> int:
        """
        Get the node's unique identifier.

        Returns:
            The node's ID
        """
        return self.m_id

    def position(self) -> Vector3f:
        """
        Get the node's position in world space.

        Returns:
            The node's position as a Vector3f
        """
        return self.m_position

    def ways(self) -> List[Any]:
        """
        Get the list of ways connected to this node.

        Returns:
            List of connected Way objects
        """
        return self.m_ways

    def units(self) -> List[Any]:
        """
        Get the list of units attached to this node.

        Returns:
            List of attached Unit objects
        """
        return self.m_units

    def unit(self, index: int) -> Any:
        """
        Get a specific unit by index.

        Args:
            index: The index of the unit to retrieve

        Returns:
            The Unit at the specified index
        """
        if 0 <= index < len(self.m_units):
            return self.m_units[index]
        return None

    @staticmethod
    def color() -> int:
        """
        Get the global color for nodes.

        Returns:
            The color value as an integer
        """
        return 0xAAAAAA

    def find_nearest_node(self, nodes: List['Node']) -> Optional['Node']:
        """
        Find the nearest node from a list of nodes.

        Args:
            nodes: List of nodes to search

        Returns:
            The nearest node or None if the list is empty
        """
        if not nodes:
            return None

        nearest_node = nodes[0]
        min_distance = (self.m_position - nearest_node.m_position).magnitude()

        for node in nodes[1:]:
            distance = (self.m_position - node.m_position).magnitude()
            if distance < min_distance:
                min_distance = distance
                nearest_node = node

        return nearest_node

    def connect_to(self, other_node: 'Node', way_type: Any, path: Any) -> Any:
        """
        Create a Way connecting this node to another node.

        Args:
            other_node: The node to connect to
            way_type: The type of way to create
            path: The path to add the way to

        Returns:
            The newly created Way
        """
        # Check if the nodes are already connected
        existing_way = self.get_way_to_node(other_node)
        if existing_way:
            return existing_way

        # Create a new way between the nodes
        return path.add_way(way_type, self, other_node)

    def disconnect_from(self, other_node: 'Node') -> None:
        """
        Remove any Way connecting this node to another node.

        Args:
            other_node: The node to disconnect from
        """
        way = self.get_way_to_node(other_node)
        if way:
            # Remove the way from both nodes
            self.m_ways.remove(way)
            other_node.m_ways.remove(way)

            # If the way is part of a path, it should be removed from there too
            # This would typically be handled by the Path class
