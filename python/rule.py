"""
Rule implementation for OpenGlassBox simulation engine.

This module implements the Rule classes that define behavior logic for the simulation:
- IRule: Base rule interface
- RuleMap: Rules that operate on map cells
- RuleUnit: Rules that operate on units

Rules evaluate conditions and execute commands during simulation steps,
forming the core behavior mechanism of the simulation.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from abc import ABC

# Forward declarations
from .rule_command import IRuleCommand, RuleContext


class IRule:
    """
    Base class for all rules in the simulation.

    Rules define behavior in the simulation by executing commands when conditions are met.
    """

    def __init__(self, name: str, rate: int, commands: List[IRuleCommand]):
        """
        Initialize the rule.

        Args:
            name: Rule name/type
            rate: Rule execution rate
            commands: List of commands to execute
        """
        self.m_type = name
        self.m_rate = rate
        self.m_commands = commands

    def execute(self, context: RuleContext) -> bool:
        """
        Execute the rule in the given context.

        First validates all commands, then executes them if all validations pass.

        Args:
            context: The execution context with references to simulation elements

        Returns:
            True if the rule successfully executed, False otherwise
        """
        # Validate all commands
        for command in reversed(self.m_commands):
            if not command.validate(context):
                return False

        # Execute all commands
        for command in reversed(self.m_commands):
            command.execute(context)

        return True

    def type(self) -> str:
        """
        Get the rule type/name.

        Returns:
            The rule type string
        """
        return self.m_type

    def rate(self) -> int:
        """
        Get the rule execution rate.

        Returns:
            The rule rate value
        """
        return self.m_rate

    def commands(self) -> List[IRuleCommand]:
        """
        Get the rule commands.

        Returns:
            The list of commands for this rule
        """
        return self.m_commands


@dataclass
class RuleMapType:
    """Data structure defining a map rule type."""
    name: str
    rate: int = 1
    commands: List[IRuleCommand] = field(default_factory=list)
    randomTiles: bool = False
    randomTilesPercent: int = 100


class RuleMap(IRule):
    """
    Rule that operates on map cells.

    Map rules can affect specific areas of the map grid and can
    optionally apply to random tiles within the area.
    """

    def __init__(self, rule_type: RuleMapType):
        """
        Initialize the map rule.

        Args:
            rule_type: The map rule type definition
        """
        super().__init__(rule_type.name, rule_type.rate, rule_type.commands)
        self.m_randomTiles = rule_type.randomTiles
        self.m_randomTilesPercent = min(100, rule_type.randomTilesPercent)

    def is_random(self) -> bool:
        """
        Check if this rule uses randomized values.

        Returns:
            True if the rule applies to random tiles, False otherwise
        """
        return self.m_randomTiles

    def percent(self, value) -> float:
        """
        Compute the percent of the given value based on the rule's percent setting.

        Args:
            value: The value to calculate a percentage of

        Returns:
            The calculated percentage value
        """
        return value * self.m_randomTilesPercent / 100


@dataclass
class RuleUnitType:
    """Data structure defining a unit rule type."""
    name: str
    rate: int = 1
    commands: List[IRuleCommand] = field(default_factory=list)
    onFail: Optional['RuleUnit'] = None


class RuleUnit(IRule):
    """
    Rule that operates on units.

    Unit rules define behavior for production units and can have
    fallback rules that execute if the main rule fails.
    """

    def __init__(self, rule_type: RuleUnitType):
        """
        Initialize the unit rule.

        Args:
            rule_type: The unit rule type definition
        """
        super().__init__(rule_type.name, rule_type.rate, rule_type.commands)
        self.m_onFail = rule_type.onFail

    def execute(self, context: RuleContext) -> bool:
        """
        Execute the rule and fallback if needed.

        If the base rule execution fails and there is a fallback rule,
        the fallback rule is executed.

        Args:
            context: The execution context

        Returns:
            True if the rule or its fallback executed successfully, False otherwise
        """
        if super().execute(context):
            return True
        elif self.m_onFail is not None:
            return self.m_onFail.execute(context)
        else:
            return False
