"""
Unit class for OpenGlassBox simulation engine.

This module defines the Unit class which represents stationary entities in the simulation
such as buildings, factories, and other fixed structures. Units are placed at Nodes in
the Path network, store resources, and execute rules that can create Agents.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

from vector import Vector3f
from resources import Resources


@dataclass
class RuleContext:
    """Context information for rule execution."""
    unit: Optional['Unit'] = None
    city: Optional[Any] = None
    locals: Optional[Resources] = None
    globals: Optional[Resources] = None
    u: int = 0  # Map grid U coordinate
    v: int = 0  # Map grid V coordinate
    radius: int = 0


@dataclass
class UnitType:
    """Type definition for Units in the simulation."""
    name: str
    color: int = 0xFFFFFF
    radius: int = 1
    resources: Resources = field(default_factory=Resources)
    rules: List[Any] = field(default_factory=list)
    targets: List[str] = field(default_factory=list)


class Unit:
    """
    Stationary entity in the simulation that manages resources and rules.

    Units represent buildings, factories, and other fixed structures in the simulation.
    They are placed at Nodes in the Path network, store resources, and execute rules
    that can create Agents.
    """

    def __init__(self, unit_type: UnitType, node: Any, city: Any):
        """
        Create a new Unit instance.

        Args:
            unit_type: The type of unit defining its behavior and properties
            node: The Path Node where this unit is located
            city: The City that contains this unit
        """
        self.m_type = unit_type
        self.m_node = node

        # Clone resources from the unit type
        self.m_resources = Resources()
        for resource in self.m_type.resources.container():
            self.m_resources.add_resource(resource.type(), resource.amount())

        # Register the unit with the node
        self.m_node.addUnit(self)

        # Initialize the rule context
        self.m_context = RuleContext(
            unit=self,
            city=city,
            locals=self.m_resources,
            globals=city.globals(),
            radius=unit_type.radius
        )

        # Calculate grid position
        u_out = []
        v_out = []
        city.world2mapPosition(self.m_node.position(), u_out, v_out)
        self.m_context.u = u_out[0]
        self.m_context.v = v_out[0]

        # Initialize tick counter
        self.m_ticks = 0

    def execute_rules(self):
        """
        Execute simulation rules for this unit.

        Increments the tick counter and executes rules when the tick count
        matches the rule's rate.
        """
        self.m_ticks += 1

        # Execute rules in reverse order (as in the C++ implementation)
        for i in range(len(self.m_type.rules) - 1, -1, -1):
            rule = self.m_type.rules[i]

            # Execute rule if tick counter matches rule rate
            if self.m_ticks % rule.rate() == 0:
                rule.execute(self.m_context)

    def accepts(self, search_target: str, resources_to_try: Resources) -> bool:
        """
        Check if this unit can accept the given resources for the specified target.

        Args:
            search_target: The target type to check against this unit's targets
            resources_to_try: The resources to check for acceptance

        Returns:
            True if the unit accepts the resources for this target, False otherwise
        """
        # Check if the unit accepts this target type
        if search_target not in self.m_type.targets:
            return False

        # Check if the unit can add any of these resources
        return self.m_resources.can_add_some_resources(resources_to_try)

    def type(self) -> str:
        """Get the type name of the unit."""
        return self.m_type.name

    def resources(self) -> Resources:
        """Get the resources owned by this unit."""
        return self.m_resources

    def position(self) -> Vector3f:
        """Get the position of this unit in world coordinates."""
        return self.m_node.position()

    def color(self) -> int:
        """Get the color identifier for rendering."""
        return self.m_type.color

    def node(self):
        """Get the Path Node where this unit is located."""
        return self.m_node

    def id(self) -> int:
        """Get the unique identifier of this unit."""
        return self.m_node.id()

    def has_ways(self) -> bool:
        """
        Check if this unit's node has connected ways.

        Units should be placed at nodes with ways, otherwise agents
        cannot move to or from the unit.
        """
        return self.m_node.has_ways()
