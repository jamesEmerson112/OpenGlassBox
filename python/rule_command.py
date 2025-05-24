"""
Rule command implementation for OpenGlassBox simulation engine.

This module implements various rule commands that are used in the simulation:
- RuleCommandAdd: Adds resources to a target
- RuleCommandRemove: Removes resources from a target
- RuleCommandTest: Tests resource conditions
- RuleCommandAgent: Creates an agent with specified properties

These commands are executed by rules during simulation steps and form the
core behavior mechanism of the simulation.
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional, Dict, List, Any
from .agent import AgentType
from .resources import Resources


class RuleContext:
    """
    Structure holding all information needed to execute simulation rules.

    This class provides context for rule execution, including references to
    city, unit, resources, and location information.
    """

    def __init__(self):
        """Initialize an empty rule context."""
        self.city = None  # Reference to city
        self.unit = None  # Reference to unit
        self.locals = None  # Local resources (of Map or Unit)
        self.globals = None  # Global resources
        self.u = 0  # Position on grid (U)
        self.v = 0  # Position on grid (V)
        self.radius = 0  # Radius action on Map resources


class IRuleCommand(ABC):
    """
    Base class interfacing commands defined from simulation scripts.

    This abstract base class defines the interface for all rule commands.
    """

    @abstractmethod
    def validate(self, context: RuleContext) -> bool:
        """
        Return true if this command can be applied in the current context.

        Args:
            context: The rule execution context

        Returns:
            True if the command can be executed, False otherwise
        """
        pass

    @abstractmethod
    def execute(self, context: RuleContext) -> None:
        """
        Apply the command on the current context.

        Args:
            context: The rule execution context
        """
        pass

    @abstractmethod
    def type(self) -> str:
        """
        Get a string description of this command.

        Returns:
            A string describing the command
        """
        pass


class RuleCommandAdd(IRuleCommand):
    """
    Command to add resources to a target.

    Example in script syntax:
    map Grass add 1
    """

    def __init__(self, target, amount: int):
        """
        Initialize the add command.

        Args:
            target: The resource value target to add to
            amount: The amount to add
        """
        self.m_target = target
        self.m_amount = amount

    def validate(self, context: RuleContext) -> bool:
        """
        Can be applied if the amount of resource has not reached the capacity.

        Args:
            context: The rule execution context

        Returns:
            True if there is capacity to add resources, False otherwise
        """
        return self.m_target.get(context) < self.m_target.capacity(context)

    def execute(self, context: RuleContext) -> None:
        """
        Increase the amount of resource of the target.

        Args:
            context: The rule execution context
        """
        self.m_target.add(context, self.m_amount)

    def type(self) -> str:
        """
        Get a string description of this command.

        Returns:
            A string describing the command
        """
        return f"Add {self.m_amount} Resources {self.m_target.type()}"


class RuleCommandRemove(IRuleCommand):
    """
    Command to remove resources from a target.

    Example in script syntax:
    local People remove 1
    """

    def __init__(self, target, amount: int):
        """
        Initialize the remove command.

        Args:
            target: The resource value target to remove from
            amount: The amount to remove
        """
        self.m_target = target
        self.m_amount = amount

    def validate(self, context: RuleContext) -> bool:
        """
        Can be applied if the amount of resource is enough.

        Args:
            context: The rule execution context

        Returns:
            True if there are enough resources to remove, False otherwise
        """
        return self.m_target.get(context) >= self.m_amount

    def execute(self, context: RuleContext) -> None:
        """
        Decrease the amount of resource of the target.

        Args:
            context: The rule execution context
        """
        self.m_target.remove(context, self.m_amount)

    def type(self) -> str:
        """
        Get a string description of this command.

        Returns:
            A string describing the command
        """
        return f"Remove {self.m_amount} Resources {self.m_target.type()}"


class Comparison(Enum):
    """Enum for comparison operations in RuleCommandTest."""
    EQUALS = auto()
    GREATER = auto()
    LESS = auto()


class RuleCommandTest(IRuleCommand):
    """
    Command to test resource values against a condition.

    Example in script syntax:
    map Water greater 300
    """

    def __init__(self, target, comparison: Comparison, amount: int):
        """
        Initialize the test command.

        Args:
            target: The resource value target to test
            comparison: The comparison type (EQUALS, GREATER, LESS)
            amount: The amount to compare against
        """
        self.m_target = target
        self.m_comparison = comparison
        self.m_amount = amount

    def validate(self, context: RuleContext) -> bool:
        """
        Check if the resource value meets the test condition.

        Args:
            context: The rule execution context

        Returns:
            True if the test passes, False otherwise
        """
        value = self.m_target.get(context)

        if self.m_comparison == Comparison.EQUALS:
            return value == self.m_amount
        elif self.m_comparison == Comparison.GREATER:
            return value > self.m_amount
        elif self.m_comparison == Comparison.LESS:
            return value < self.m_amount
        else:
            raise ValueError(f"Unknown comparison type: {self.m_comparison}")

    def execute(self, context: RuleContext) -> None:
        """
        Test commands don't modify anything in execution.

        Args:
            context: The rule execution context
        """
        # Do nothing - this command only validates
        pass

    def type(self) -> str:
        """
        Get a string description of this command.

        Returns:
            A string describing the command
        """
        description = ""
        if self.m_comparison == Comparison.EQUALS:
            description = "Test Equal "
        elif self.m_comparison == Comparison.GREATER:
            description = "Test Greater "
        elif self.m_comparison == Comparison.LESS:
            description = "Test Less "

        return f"{description}{self.m_amount} Resources {self.m_target.type()}"


class RuleCommandAgent(IRuleCommand, AgentType):
    """
    Command to create a new agent with specified properties.

    Example in script syntax:
    agent People color 0xFFFF00 speed 10
    """

    def __init__(self, agent_type: AgentType, target: str, resources: Resources):
        """
        Initialize the agent command.

        Args:
            agent_type: The agent type properties (name, speed, radius, color)
            target: The target resource type for the agent
            resources: Resources for the agent to carry
        """
        AgentType.__init__(self,
                          name=agent_type.name,
                          speed=agent_type.speed,
                          radius=agent_type.radius,
                          color=agent_type.color)
        self.m_target = target
        self.m_resources = resources

    def validate(self, context: RuleContext) -> bool:
        """
        Agent commands can always be validated.

        Args:
            context: The rule execution context

        Returns:
            True, always
        """
        return True

    def execute(self, context: RuleContext) -> None:
        """
        Add a new agent in the city.

        Args:
            context: The rule execution context
        """
        if context.unit.has_ways():
            context.city.add_agent(self, context.unit, self.m_resources, self.m_target)
        # In debug mode, we would print a warning here if the unit has no ways

    def type(self) -> str:
        """
        Get a string description of this command.

        Returns:
            A string describing the command
        """
        return "Add Agent"
