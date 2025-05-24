"""
Defines the RuleCommand classes for OpenGlassBox simulation engine.

Rule commands represent specific actions that a rule can take, such as
transferring resources, spawning agents, or manipulating units.
"""

from typing import Dict, List, Optional, Any
from enum import Enum, auto
from abc import ABC, abstractmethod


class Comparison(Enum):
    """Comparison types for rule test commands."""
    EQUALS = auto()
    GREATER = auto()
    LESS = auto()


class IRuleCommand(ABC):
    """
    Abstract base class for rule commands.

    Commands represent specific operations that rules can perform within
    the simulation, such as resource transfers, agent spawning, and more.
    """

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Execute the command in the given context.

        Args:
            context: The execution context (simulation, city, unit, etc.)

        Returns:
            True if execution succeeded, False otherwise
        """
        pass


class RuleCommand(IRuleCommand):
    """
    Basic rule command implementation.

    Commands represent specific operations that rules can perform within
    the simulation, such as resource transfers, agent spawning, and more.
    """

    def __init__(self, command_type: str):
        """
        Initialize a rule command with the specified type.

        Args:
            command_type: The type of command (e.g., "Transfer", "Spawn", etc.)
        """
        self.command_type = command_type
        self.params: Dict[str, Any] = {}

    def add_param(self, name: str, value: Any) -> None:
        """
        Add a parameter to the command.

        Args:
            name: Parameter name
            value: Parameter value
        """
        self.params[name] = value

    def get_param(self, name: str) -> Optional[Any]:
        """
        Get a parameter by name.

        Args:
            name: The parameter name to retrieve

        Returns:
            The parameter value, or None if not found
        """
        return self.params.get(name)

    def has_param(self, name: str) -> bool:
        """
        Check if the command has a specific parameter.

        Args:
            name: The parameter name to check

        Returns:
            True if the parameter exists, False otherwise
        """
        return name in self.params

    def type(self) -> str:
        """
        Get the command type.

        Returns:
            The command type string
        """
        return self.command_type

    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Execute the command in the given context.

        Args:
            context: The execution context (simulation, city, unit, etc.)

        Returns:
            True if execution succeeded, False otherwise
        """
        # This is a base implementation; derived classes should override
        # with specific execution logic
        return True


class RuleCommandAdd(IRuleCommand):
    """Command to add resources to a target."""

    def __init__(self, target, amount: int):
        """
        Initialize an add command.

        Args:
            target: The target to add resources to
            amount: The amount to add
        """
        self.target = target
        self.amount = amount

    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Execute the add command.

        Args:
            context: The execution context

        Returns:
            True if execution succeeded, False otherwise
        """
        self.target.add(context, self.amount)
        return True


class RuleCommandRemove(IRuleCommand):
    """Command to remove resources from a target."""

    def __init__(self, target, amount: int):
        """
        Initialize a remove command.

        Args:
            target: The target to remove resources from
            amount: The amount to remove
        """
        self.target = target
        self.amount = amount

    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Execute the remove command.

        Args:
            context: The execution context

        Returns:
            True if execution succeeded, False otherwise
        """
        self.target.remove(context, self.amount)
        return True


class RuleCommandTest(IRuleCommand):
    """Command to test a condition on a target."""

    def __init__(self, target, comparison: Comparison, value: int):
        """
        Initialize a test command.

        Args:
            target: The target to test
            comparison: The comparison operation to perform
            value: The value to compare against
        """
        self.target = target
        self.comparison = comparison
        self.value = value

    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Execute the test command.

        Args:
            context: The execution context

        Returns:
            True if the test passes, False otherwise
        """
        target_value = self.target.get(context)

        if self.comparison == Comparison.EQUALS:
            return target_value == self.value
        elif self.comparison == Comparison.GREATER:
            return target_value > self.value
        elif self.comparison == Comparison.LESS:
            return target_value < self.value

        return False


class RuleCommandAgent(IRuleCommand):
    """Command to spawn or manipulate an agent."""

    def __init__(self, agent_type, search_target: str, resources):
        """
        Initialize an agent command.

        Args:
            agent_type: The type of agent to use
            search_target: The target for the agent to search for
            resources: Resources to give to the agent
        """
        self.agent_type = agent_type
        self.search_target = search_target
        self.resources = resources

    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Execute the agent command.

        Args:
            context: The execution context

        Returns:
            True if execution succeeded, False otherwise
        """
        # In a real implementation, this would spawn an agent
        # with the given resources and search target
        return True
