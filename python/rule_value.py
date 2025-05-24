"""
Rule Value module for OpenGlassBox simulation engine.

This module implements rule value classes that allow accessing and manipulating
resources in different contexts within the simulation.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from python.resource import Resource


class RuleContext:
    """
    Structure holding all information needed to execute simulation rules.
    """

    def __init__(self):
        """Initialize an empty rule context."""
        self.city = None  # City object
        self.unit = None  # Unit object
        self.locals = None  # Local resources (of Map or Unit)
        self.globals = None  # Global resources
        self.u: int = 0  # X position on the grid of the Map
        self.v: int = 0  # Y position on the grid of the Map
        self.radius: int = 0  # Radius action on Map resources


class IRuleValue(ABC):
    """
    Abstract base class for rule values.

    Rule values provide access to resources in different contexts (global, local, map)
    and allow rules to get, add, and remove resources.
    """

    @abstractmethod
    def get(self, context: RuleContext) -> int:
        """
        Get the amount of the resource in the given context.

        Args:
            context: The rule context containing reference to resources

        Returns:
            The amount of the resource
        """
        pass

    @abstractmethod
    def capacity(self, context: RuleContext) -> int:
        """
        Get the capacity of the resource in the given context.

        Args:
            context: The rule context containing reference to resources

        Returns:
            The capacity of the resource
        """
        pass

    @abstractmethod
    def add(self, context: RuleContext, to_add: int) -> None:
        """
        Add the specified amount to the resource in the given context.

        Args:
            context: The rule context containing reference to resources
            to_add: The amount to add
        """
        pass

    @abstractmethod
    def remove(self, context: RuleContext, to_remove: int) -> None:
        """
        Remove the specified amount from the resource in the given context.

        Args:
            context: The rule context containing reference to resources
            to_remove: The amount to remove
        """
        pass

    @abstractmethod
    def type(self) -> str:
        """
        Get the type (name) of the resource.

        Returns:
            The resource type string
        """
        pass


class RuleValueGlobal(IRuleValue):
    """
    Rule value for accessing and manipulating global resources.
    """

    def __init__(self, resource: Resource):
        """
        Initialize with a resource.

        Args:
            resource: The resource to use for identifying the global resource
        """
        self.resource = resource

    def get(self, context: RuleContext) -> int:
        """
        Get the amount of the global resource.

        Args:
            context: The rule context containing reference to resources

        Returns:
            The amount of the global resource
        """
        return context.globals.getAmount(self.resource.type())

    def capacity(self, context: RuleContext) -> int:
        """
        Get the capacity of the global resource.

        Args:
            context: The rule context containing reference to resources

        Returns:
            The capacity of the global resource
        """
        return context.globals.getCapacity(self.resource.type())

    def add(self, context: RuleContext, to_add: int) -> None:
        """
        Add the specified amount to the global resource.

        Args:
            context: The rule context containing reference to resources
            to_add: The amount to add
        """
        r = context.globals.findResource(self.resource.type())
        if r:
            r.m_amount += to_add
            # Ensure we don't exceed capacity
            if r.m_amount > r.m_capacity:
                r.m_amount = r.m_capacity

    def remove(self, context: RuleContext, to_remove: int) -> None:
        """
        Remove the specified amount from the global resource.

        Args:
            context: The rule context containing reference to resources
            to_remove: The amount to remove
        """
        r = context.globals.findResource(self.resource.type())
        if r:
            r.m_amount = max(0, r.m_amount - to_remove)

    def type(self) -> str:
        """
        Get the type (name) of the resource.

        Returns:
            The resource type string
        """
        return self.resource.type()


class RuleValueLocal(IRuleValue):
    """
    Rule value for accessing and manipulating local resources.
    """

    def __init__(self, resource: Resource):
        """
        Initialize with a resource.

        Args:
            resource: The resource to use for identifying the local resource
        """
        self.resource = resource

    def get(self, context: RuleContext) -> int:
        """
        Get the amount of the local resource.

        Args:
            context: The rule context containing reference to resources

        Returns:
            The amount of the local resource
        """
        return context.locals.getAmount(self.resource.type())

    def capacity(self, context: RuleContext) -> int:
        """
        Get the capacity of the local resource.

        Args:
            context: The rule context containing reference to resources

        Returns:
            The capacity of the local resource
        """
        return context.locals.getCapacity(self.resource.type())

    def add(self, context: RuleContext, to_add: int) -> None:
        """
        Add the specified amount to the local resource.

        Args:
            context: The rule context containing reference to resources
            to_add: The amount to add
        """
        r = context.locals.findResource(self.resource.type())
        if r:
            r.m_amount += to_add
            # Ensure we don't exceed capacity
            if r.m_amount > r.m_capacity:
                r.m_amount = r.m_capacity

    def remove(self, context: RuleContext, to_remove: int) -> None:
        """
        Remove the specified amount from the local resource.

        Args:
            context: The rule context containing reference to resources
            to_remove: The amount to remove
        """
        r = context.locals.findResource(self.resource.type())
        if r:
            r.m_amount = max(0, r.m_amount - to_remove)

    def type(self) -> str:
        """
        Get the type (name) of the resource.

        Returns:
            The resource type string
        """
        return self.resource.type()


class RuleValueMap(IRuleValue):
    """
    Rule value for accessing and manipulating map resources.
    """

    def __init__(self, map_id: str):
        """
        Initialize with a map ID.

        Args:
            map_id: The ID of the map to access
        """
        self.map_id = map_id

    def get(self, context: RuleContext) -> int:
        """
        Get the amount of the map resource at the specified location.

        Args:
            context: The rule context containing reference to resources

        Returns:
            The amount of the map resource
        """
        return context.city.getMap(self.map_id).getResource(context.u, context.v, context.radius)

    def capacity(self, context: RuleContext) -> int:
        """
        Get the capacity of the map resource.

        Args:
            context: The rule context containing reference to resources

        Returns:
            The capacity of the map resource
        """
        return context.city.getMap(self.map_id).getCapacity()

    def add(self, context: RuleContext, to_add: int) -> None:
        """
        Add the specified amount to the map resource at the specified location.

        Args:
            context: The rule context containing reference to resources
            to_add: The amount to add
        """
        context.city.getMap(self.map_id).addResource(
            context.u, context.v, context.radius, to_add
        )

    def remove(self, context: RuleContext, to_remove: int) -> None:
        """
        Remove the specified amount from the map resource at the specified location.

        Args:
            context: The rule context containing reference to resources
            to_remove: The amount to remove
        """
        context.city.getMap(self.map_id).removeResource(
            context.u, context.v, context.radius, to_remove
        )

    def type(self) -> str:
        """
        Get the type (name) of the map.

        Returns:
            The map ID
        """
        return self.map_id
