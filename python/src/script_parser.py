"""
Script parser implementation for OpenGlassBox simulation engine.

This module implements the parsing functionality for simulation configuration scripts:
- Resource definitions
- Path definitions
- Agent definitions
- Map definitions
- Unit definitions
- Rule definitions and commands

The Script class parses and stores these elements for use in the simulation.
"""

import os
from typing import Dict, List, Optional, Any, Tuple, TextIO
from dataclasses import dataclass, field
from enum import Enum

from resource import Resource
from resources import Resources
from agent import AgentType
from rule import RuleMap, RuleUnit, RuleMapType, RuleUnitType
from rule_command import (
    IRuleCommand, RuleCommandAdd, RuleCommandRemove,
    RuleCommandTest, RuleCommandAgent, Comparison
)
from rule_value import (
    IRuleValue, RuleValueLocal, RuleValueGlobal,
    RuleValueMap
)


@dataclass
class PathType:
    """Path type definition from script."""
    name: str
    color: int = 0


@dataclass
class WayType:
    """Way type definition from script."""
    name: str
    color: int = 0


@dataclass
class MapType:
    """Map type definition from script."""
    name: str
    color: int = 0
    capacity: int = 0
    rules: List[RuleMap] = field(default_factory=list)


@dataclass
class UnitType:
    """Unit type definition from script."""
    name: str
    color: int = 0
    radius: int = 0
    targets: List[str] = field(default_factory=list)
    rules: List[RuleUnit] = field(default_factory=list)
    resources: Optional[Resources] = None


class Script:
    """
    Parse a simulation script and store internally all types and simulation rules.

    This class reads a simulation script file and extracts all the definitions
    for resources, paths, units, maps, agents, and rules.
    """

    def __init__(self):
        """Initialize an empty script parser."""
        self.m_resources: Dict[str, Resource] = {}
        self.m_pathTypes: Dict[str, PathType] = {}
        self.m_segmentTypes: Dict[str, WayType] = {}
        self.m_agentTypes: Dict[str, AgentType] = {}
        self.m_ruleMaps: Dict[str, RuleMap] = {}
        self.m_ruleUnits: Dict[str, RuleUnit] = {}
        self.m_unitTypes: Dict[str, UnitType] = {}
        self.m_mapTypes: Dict[str, MapType] = {}
        self.m_file: Optional[TextIO] = None
        self.m_token: str = ""
        self.m_success: bool = False

    def parse(self, filename: str) -> bool:
        """
        Parse the simulation file and fill its internal states.

        Args:
            filename: Path to the simulation script file

        Returns:
            True if parsing succeeded, False otherwise
        """
        print(f"Parsing script '{filename}'")

        try:
            if not os.path.exists(filename):
                print(f"Failed opening '{filename}': File not found")
                self.m_success = False
                return False

            with open(filename, 'r') as self.m_file:
                try:
                    self.parseScript()
                    self.m_success = True
                    print("  done")
                except Exception as e:
                    print(f"Failed parsing script '{filename}' at token '{self.m_token}' Reason was: {str(e)}")
                    self.m_success = False
        except Exception as e:
            print(f"Failed opening '{filename}' Reason: {str(e)}")
            self.m_success = False

        return self.m_success

    def nextToken(self) -> str:
        """
        Get the next token from the script file.

        Returns:
            The next token as a string
        """
        if self.m_file is None:
            self.m_token = ""
            return self.m_token

        tokens = []
        while True:
            char = self.m_file.read(1)
            if not char:
                break

            # Skip whitespace between tokens
            if char.isspace():
                if tokens:
                    break
                continue

            tokens.append(char)

        self.m_token = ''.join(tokens)
        return self.m_token

    def parseScript(self) -> None:
        """
        Parse the entire script, processing all section types.

        Raises:
            RuntimeError: If the script has invalid syntax
        """
        while True:
            empty = (len(self.m_token) == 0)
            token = self.nextToken()

            if token == "resources":
                self.parseResources()
            elif token == "rules":
                self.parseRules()
            elif token == "maps":
                self.parseMaps()
            elif token == "paths":
                self.parsePaths()
            elif token == "segments":
                self.parseWays()
            elif token == "agents":
                self.parseAgents()
            elif token == "units":
                self.parseUnits()
            elif token == "":
                if not empty:
                    return
                # Empty file detection
                raise RuntimeError("Empty file")
            else:
                raise RuntimeError(f"Unknown section: {token}")

    def parseResources(self) -> None:
        """
        Parse the resources section of the script.

        Raises:
            RuntimeError: If the section has invalid syntax
        """
        while True:
            token = self.nextToken()
            if token == "end":
                return
            elif token == "resource":
                self.parseResource()
            else:
                raise RuntimeError(f"Expected 'end' or 'resource', got '{token}'")

    def parseResource(self) -> None:
        """
        Parse a single resource definition.

        Raises:
            RuntimeError: If the resource definition has invalid syntax
        """
        name = self.nextToken()
        self.m_resources[name] = Resource(name)

    def parseResourcesArray(self, resources: Resources) -> None:
        """
        Parse an array of resource definitions.

        Args:
            resources: Resources object to populate

        Raises:
            RuntimeError: If the array has invalid syntax
        """
        token = self.nextToken()
        if token != "[":
            raise RuntimeError("Expected '['")

        while True:
            token = self.nextToken()
            if token == "]":
                return

            resource = self.getResource(token)
            amount = self._toUint(self.nextToken())
            resources.addResource(resource.type(), amount)

    def parseCapacitiesArray(self, resources: Resources) -> None:
        """
        Parse an array of capacity definitions.

        Args:
            resources: Resources object to populate with capacities

        Raises:
            RuntimeError: If the array has invalid syntax
        """
        token = self.nextToken()
        if token != "[":
            raise RuntimeError("Expected '['")

        while True:
            token = self.nextToken()
            if token == "]":
                return

            resource = self.getResource(token)
            capacity = self._toUint(self.nextToken())
            resources.setCapacity(resource.type(), capacity)

    def parsePaths(self) -> None:
        """
        Parse the paths section of the script.

        Raises:
            RuntimeError: If the section has invalid syntax
        """
        while True:
            token = self.nextToken()
            if token == "end":
                return
            elif token == "path":
                self.parsePath()
            else:
                raise RuntimeError(f"Expected 'end' or 'path', got '{token}'")

    def parsePath(self) -> None:
        """
        Parse a single path definition.

        Raises:
            RuntimeError: If the path definition has invalid syntax
        """
        name = self.nextToken()
        path = PathType(name=name)
        self.m_pathTypes[path.name] = path

        while True:
            token = self.nextToken()
            if token == "color":
                path.color = self._toColor(self.nextToken())
                return
            else:
                raise RuntimeError(f"Expected 'color', got '{token}'")

    def parseWays(self) -> None:
        """
        Parse the ways/segments section of the script.

        Raises:
            RuntimeError: If the section has invalid syntax
        """
        while True:
            token = self.nextToken()
            if token == "end":
                return
            elif token == "segment":
                self.parseWay()
            else:
                raise RuntimeError(f"Expected 'end' or 'segment', got '{token}'")

    def parseWay(self) -> None:
        """
        Parse a single way/segment definition.

        Raises:
            RuntimeError: If the way definition has invalid syntax
        """
        name = self.nextToken()
        seg = WayType(name=name)
        self.m_segmentTypes[seg.name] = seg

        while True:
            token = self.nextToken()
            if token == "color":
                seg.color = self._toColor(self.nextToken())
                return
            else:
                raise RuntimeError(f"Expected 'color', got '{token}'")

    def parseAgents(self) -> None:
        """
        Parse the agents section of the script.

        Raises:
            RuntimeError: If the section has invalid syntax
        """
        while True:
            token = self.nextToken()
            if token == "end":
                return
            elif token == "agent":
                self.parseAgent()
            else:
                raise RuntimeError(f"Expected 'end' or 'agent', got '{token}'")

    def parseAgent(self) -> None:
        """
        Parse a single agent definition.

        Raises:
            RuntimeError: If the agent definition has invalid syntax
        """
        name = self.nextToken()
        agent = AgentType(name=name, speed=0, radius=0, color=0)
        self.m_agentTypes[agent.name] = agent

        while True:
            token = self.nextToken()
            if token == "color":
                agent.color = self._toColor(self.nextToken())
            elif token == "speed":
                agent.speed = self._toFloat(self.nextToken())
                return
            else:
                raise RuntimeError(f"Expected 'color' or 'speed', got '{token}'")

    def parseRules(self) -> None:
        """
        Parse the rules section of the script.

        Raises:
            RuntimeError: If the section has invalid syntax
        """
        while True:
            token = self.nextToken()
            if token == "end":
                return
            elif token == "mapRule":
                self.parseRuleMap()
            elif token == "unitRule":
                self.parseRuleUnit()
            else:
                raise RuntimeError(f"Expected 'end', 'mapRule', or 'unitRule', got '{token}'")

    def parseRuleMap(self) -> None:
        """
        Parse a map rule definition.

        Raises:
            RuntimeError: If the rule definition has invalid syntax
        """
        name = self.nextToken()
        type_def = RuleMapType(name=name)

        while True:
            token = self.nextToken()
            if token == "end":
                rule = RuleMap(type_def)
                self.m_ruleMaps[rule.type()] = rule
                return
            elif token == "rate":
                type_def.rate = self._toUint(self.nextToken())
            elif token == "randomTiles":
                type_def.randomTiles = self._toBool(self.nextToken())
            elif token == "randomTilesPercent":
                type_def.randomTiles = True
                type_def.randomTilesPercent = self._toUint(self.nextToken())
            else:
                type_def.commands.append(self.parseCommand(token))

    def parseRuleUnit(self) -> None:
        """
        Parse a unit rule definition.

        Raises:
            RuntimeError: If the rule definition has invalid syntax
        """
        name = self.nextToken()
        type_def = RuleUnitType(name=name)

        while True:
            token = self.nextToken()
            if token == "end":
                rule = RuleUnit(type_def)
                self.m_ruleUnits[rule.type()] = rule
                return
            elif token == "rate":
                type_def.rate = self._toUint(self.nextToken())
            # TODO: Handle onFail
            # elif token == "onFail":
            #    pass
            else:
                type_def.commands.append(self.parseCommand(token))

    def parseCommand(self, token: str) -> IRuleCommand:
        """
        Parse a command definition.

        Args:
            token: The first token of the command

        Returns:
            The parsed command object

        Raises:
            RuntimeError: If the command has invalid syntax
        """
        target = None
        command = None

        if token == "local":
            resource = self.getResource(self.nextToken())
            target = RuleValueLocal(resource)
        elif token == "global":
            resource = self.getResource(self.nextToken())
            target = RuleValueGlobal(resource)
        elif token == "map":
            target = RuleValueMap(self.nextToken())
        elif token == "agent":
            name = self.nextToken()
            search_target = ""
            resources = Resources()

            while True:
                cmd = self.nextToken()
                if cmd == "to":
                    search_target = self.nextToken()
                elif cmd == "add":
                    self.parseResourcesArray(resources)
                    break
                else:
                    raise RuntimeError(f"Expected 'to' or 'add', got '{cmd}'")

            command = RuleCommandAgent(self.getAgentType(name), search_target, resources)
        else:
            raise RuntimeError(f"Unknown command type: {token}")

        if target is not None:
            cmd = self.nextToken()
            if cmd == "add":
                command = RuleCommandAdd(target, self._toUint(self.nextToken()))
            elif cmd == "remove":
                command = RuleCommandRemove(target, self._toUint(self.nextToken()))
            elif cmd == "greater":
                command = RuleCommandTest(target, Comparison.GREATER, self._toUint(self.nextToken()))
            elif cmd == "less":
                command = RuleCommandTest(target, Comparison.LESS, self._toUint(self.nextToken()))
            elif cmd == "equals":
                command = RuleCommandTest(target, Comparison.EQUALS, self._toUint(self.nextToken()))
            else:
                raise RuntimeError(f"Unknown command action: {cmd}")

        return command

    def parseMaps(self) -> None:
        """
        Parse the maps section of the script.

        Raises:
            RuntimeError: If the section has invalid syntax
        """
        while True:
            token = self.nextToken()
            if token == "end":
                return
            elif token == "map":
                self.parseMap()
            else:
                raise RuntimeError(f"Expected 'end' or 'map', got '{token}'")

    def parseMap(self) -> None:
        """
        Parse a map definition.

        Raises:
            RuntimeError: If the map definition has invalid syntax
        """
        name = self.nextToken()
        map_type = MapType(name=name)
        self.m_mapTypes[map_type.name] = map_type

        while True:
            token = self.nextToken()
            if token == "color":
                map_type.color = self._toColor(self.nextToken())
            elif token == "capacity":
                map_type.capacity = self._toUint(self.nextToken())
            elif token == "rules":
                self.parseRuleMapArray(map_type.rules)
                return
            else:
                raise RuntimeError(f"Expected 'color', 'capacity', or 'rules', got '{token}'")

    def parseUnits(self) -> None:
        """
        Parse the units section of the script.

        Raises:
            RuntimeError: If the section has invalid syntax
        """
        while True:
            token = self.nextToken()
            if token == "end":
                return
            elif token == "unit":
                self.parseUnit()
            else:
                raise RuntimeError(f"Expected 'end' or 'unit', got '{token}'")

    def parseUnit(self) -> None:
        """
        Parse a unit definition.

        Raises:
            RuntimeError: If the unit definition has invalid syntax
        """
        name = self.nextToken()
        unit = UnitType(name=name, resources=Resources())
        self.m_unitTypes[unit.name] = unit

        caps = Resources()
        resources = Resources()

        while True:
            token = self.nextToken()
            if token == "color":
                unit.color = self._toColor(self.nextToken())
            elif token == "mapRadius":
                unit.radius = self._toUint(self.nextToken())
            elif token == "rules":
                self.parseRuleUnitArray(unit.rules)
            elif token == "targets":
                self.parseStringArray(unit.targets)
            elif token == "caps":
                self.parseCapacitiesArray(caps)
                unit.resources.setCapacities(caps)
            elif token == "resources":
                self.parseResourcesArray(resources)
                unit.resources.addResources(resources)
                return
            else:
                raise RuntimeError(f"Unexpected token in unit definition: {token}")

    def parseStringArray(self, vec: List[str]) -> None:
        """
        Parse an array of strings.

        Args:
            vec: List to populate with strings

        Raises:
            RuntimeError: If the array has invalid syntax
        """
        token = self.nextToken()
        if token != "[":
            raise RuntimeError("Expected '['")

        while True:
            token = self.nextToken()
            if token == "]":
                return
            vec.append(token)

    def parseRuleMapArray(self, rules: List[RuleMap]) -> None:
        """
        Parse an array of map rule references.

        Args:
            rules: List to populate with rule references

        Raises:
            RuntimeError: If the array has invalid syntax
        """
        token = self.nextToken()
        if token != "[":
            raise RuntimeError("Expected '['")

        while True:
            token = self.nextToken()
            if token == "]":
                return
            rules.append(self.m_ruleMaps[token])

    def parseRuleUnitArray(self, rules: List[RuleUnit]) -> None:
        """
        Parse an array of unit rule references.

        Args:
            rules: List to populate with rule references

        Raises:
            RuntimeError: If the array has invalid syntax
        """
        token = self.nextToken()
        if token != "[":
            raise RuntimeError("Expected '['")

        while True:
            token = self.nextToken()
            if token == "]":
                return
            rules.append(self.m_ruleUnits[token])

    # Accessor methods

    def getResource(self, id: str) -> Resource:
        """
        Get a resource type by name.

        Args:
            id: Resource type name

        Returns:
            The resource type

        Raises:
            KeyError: If the resource is not found
        """
        return self.m_resources[id]

    def getPathType(self, id: str) -> PathType:
        """
        Get a path type by name.

        Args:
            id: Path type name

        Returns:
            The path type

        Raises:
            KeyError: If the path type is not found
        """
        return self.m_pathTypes[id]

    def getWayType(self, id: str) -> WayType:
        """
        Get a way/segment type by name.

        Args:
            id: Way type name

        Returns:
            The way type

        Raises:
            KeyError: If the way type is not found
        """
        return self.m_segmentTypes[id]

    def getAgentType(self, id: str) -> AgentType:
        """
        Get an agent type by name.

        Args:
            id: Agent type name

        Returns:
            The agent type

        Raises:
            KeyError: If the agent type is not found
        """
        return self.m_agentTypes[id]

    def getRuleMap(self, id: str) -> RuleMap:
        """
        Get a map rule by name.

        Args:
            id: Map rule name

        Returns:
            The map rule

        Raises:
            KeyError: If the map rule is not found
        """
        return self.m_ruleMaps[id]

    def getRuleUnit(self, id: str) -> RuleUnit:
        """
        Get a unit rule by name.

        Args:
            id: Unit rule name

        Returns:
            The unit rule

        Raises:
            KeyError: If the unit rule is not found
        """
        return self.m_ruleUnits[id]

    def getUnitType(self, id: str) -> UnitType:
        """
        Get a unit type by name.

        Args:
            id: Unit type name

        Returns:
            The unit type

        Raises:
            KeyError: If the unit type is not found
        """
        return self.m_unitTypes[id]

    def getMapType(self, id: str) -> MapType:
        """
        Get a map type by name.

        Args:
            id: Map type name

        Returns:
            The map type

        Raises:
            KeyError: If the map type is not found
        """
        return self.m_mapTypes[id]

    # Utility methods for type conversion

    @staticmethod
    def _toUint(word: str) -> int:
        """Convert string to unsigned integer."""
        return int(word)

    @staticmethod
    def _toColor(word: str) -> int:
        """Convert hex string to color integer."""
        return int(word, 16)

    @staticmethod
    def _toFloat(word: str) -> float:
        """Convert string to float."""
        return float(word)

    @staticmethod
    def _toBool(word: str) -> bool:
        """Convert string to boolean."""
        if word == "true":
            return True
        if word == "false":
            return False
        return bool(Script._toUint(word))
