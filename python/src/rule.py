"""
Defines the Rule classes for OpenGlassBox simulation engine.

Rules define how simulation entities interact with each other and how resources
flow through the simulation. Each rule has a set of conditions and commands.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field

from rule_command import RuleCommand
from rule_value import IRuleValue as RuleValue


class Rule:
    """
    Rule that defines how simulation entities interact.

    A rule has conditions that determine when it should be triggered,
    and commands that define what actions should be taken when triggered.
    """

    def __init__(self, rule_type: str):
        """
        Initialize a rule with the specified type.

        Args:
            rule_type: The type of the rule (e.g., "Production", "Consumption")
        """
        self.rule_type = rule_type
        self.commands: List[RuleCommand] = []
        self.conditions: Dict[str, RuleValue] = {}
        self.frequency = 1.0  # How often the rule executes (1.0 = every tick)
        self.probability = 1.0  # Probability of execution when conditions are met

    def add_command(self, command: RuleCommand) -> None:
        """
        Add a command to the rule.

        Args:
            command: The command to add
        """
        self.commands.append(command)

    def add_condition(self, name: str, value: RuleValue) -> None:
        """
        Add a condition to the rule.

        Args:
            name: The name of the condition
            value: The value of the condition
        """
        self.conditions[name] = value

    def get_condition(self, name: str) -> Optional[RuleValue]:
        """
        Get a condition by name.

        Args:
            name: The name of the condition to retrieve

        Returns:
            The condition value, or None if not found
        """
        return self.conditions.get(name)

    def has_condition(self, name: str) -> bool:
        """
        Check if the rule has a specific condition.

        Args:
            name: The name of the condition to check

        Returns:
            True if the condition exists, False otherwise
        """
        return name in self.conditions

    def commands_count(self) -> int:
        """
        Get the number of commands in the rule.

        Returns:
            The number of commands
        """
        return len(self.commands)

    def get_command(self, index: int) -> Optional[RuleCommand]:
        """
        Get a command by index.

        Args:
            index: The index of the command to retrieve

        Returns:
            The command at the specified index, or None if out of bounds
        """
        if 0 <= index < len(self.commands):
            return self.commands[index]
        return None

    def type(self) -> str:
        """
        Get the rule type.

        Returns:
            The rule type string
        """
        return self.rule_type

    def set_frequency(self, frequency: float) -> None:
        """
        Set how often the rule should be executed.

        Args:
            frequency: How often the rule executes (1.0 = every tick)
        """
        self.frequency = max(0.0, min(1.0, frequency))

    def get_frequency(self) -> float:
        """
        Get the rule execution frequency.

        Returns:
            The rule execution frequency
        """
        return self.frequency

    def set_probability(self, probability: float) -> None:
        """
        Set the probability of the rule executing when conditions are met.

        Args:
            probability: Execution probability (0.0 to 1.0)
        """
        self.probability = max(0.0, min(1.0, probability))

    def get_probability(self) -> float:
        """
        Get the rule execution probability.

        Returns:
            The rule execution probability
        """
        return self.probability

    def check_conditions(self, context: Dict[str, Any]) -> bool:
        """
        Check if all conditions of the rule are satisfied.

        Args:
            context: The execution context (simulation, city, unit, etc.)

        Returns:
            True if all conditions are satisfied, False otherwise
        """
        for name, value in self.conditions.items():
            if not value.evaluate(context):
                return False
        return True

    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Execute the rule if conditions are met.

        Args:
            context: The execution context (simulation, city, unit, etc.)

        Returns:
            True if execution succeeded, False otherwise
        """
        if not self.check_conditions(context):
            return False

        # Execute all commands
        success = True
        for command in self.commands:
            if not command.execute(context):
                success = False

        return success


@dataclass
class RuleMapType:
    """Type definition for map rules."""
    name: str
    rate: int = 0
    randomTiles: bool = False
    randomTilesPercent: int = 0
    commands: List[Any] = field(default_factory=list)


@dataclass
class RuleUnitType:
    """Type definition for unit rules."""
    name: str
    rate: int = 0
    commands: List[Any] = field(default_factory=list)


class RuleMap(Rule):
    """
    Rule specific to maps, such as resource generation or transformation.
    """

    def __init__(self, rule_type: RuleMapType):
        """
        Initialize a map rule with the specified type.

        Args:
            rule_type: The type definition for the map rule
        """
        super().__init__(rule_type.name)
        self.rule_type_def = rule_type

    def type(self) -> str:
        """
        Get the rule type.

        Returns:
            The rule type string
        """
        return self.rule_type_def.name


class RuleUnit(Rule):
    """
    Rule specific to units, such as resource production or consumption.
    """

    def __init__(self, rule_type: RuleUnitType):
        """
        Initialize a unit rule with the specified type.

        Args:
            rule_type: The type definition for the unit rule
        """
        super().__init__(rule_type.name)
        self.rule_type_def = rule_type

    def type(self) -> str:
        """
        Get the rule type.

        Returns:
            The rule type string
        """
        return self.rule_type_def.name
