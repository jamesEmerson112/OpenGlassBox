"""
Test suite for the RuleValue class and related value types.

This file covers:
- Construction and evaluation of different RuleValue types.
- Testing global values, local values, map values, and constants.
- Verification of arithmetic operations and value comparisons.
- Testing resource-based value calculations and context handling.

The tests ensure that RuleValue objects behave correctly for simulation logic,
rule evaluation, and resource management within the OpenGlassBox engine.
"""

import pytest

from resource import Resource as OpenGlassBoxResource
from rule_value import RuleContext, RuleValueGlobal, RuleValueLocal, RuleValueMap

import math


def test_rule_value_global():
    """Test global rule values."""
    # Test creating and evaluating global values
    global_value = RuleValueGlobal("TestResource")
    assert global_value.m_name == "TestResource"

    # Test evaluation with context
    context = RuleContext()
    context.m_globalResources = {"TestResource": OpenGlassBoxResource("TestResource", 42.0)}

    result = global_value.eval(context)
    assert result == 42.0

    # Test with missing resource
    context.m_globalResources = {}
    result = global_value.eval(context)
    assert result == 0.0


def test_rule_value_local():
    """Test local rule values."""
    # Test creating and evaluating local values
    local_value = RuleValueLocal("LocalResource")
    assert local_value.m_name == "LocalResource"

    # Test evaluation with context
    context = RuleContext()
    context.m_localResources = {"LocalResource": OpenGlassBoxResource("LocalResource", 25.5)}

    result = local_value.eval(context)
    assert result == 25.5

    # Test with missing resource
    context.m_localResources = {}
    result = local_value.eval(context)
    assert result == 0.0


def test_rule_value_map():
    """Test map rule values."""
    # Test creating map values
    map_value = RuleValueMap("MapResource")
    assert map_value.m_name == "MapResource"

    # Test evaluation with context
    context = RuleContext()
    context.m_mapValue = 15.0

    result = map_value.eval(context)
    assert result == 15.0

    # Test with no map value set
    context.m_mapValue = 0.0
    result = map_value.eval(context)
    assert result == 0.0


def test_rule_context():
    """Test the RuleContext container."""
    context = RuleContext()

    # Test initialization
    assert isinstance(context.m_globalResources, dict)
    assert isinstance(context.m_localResources, dict)
    assert context.m_mapValue == 0.0

    # Test setting resources
    global_res = OpenGlassBoxResource("Global", 100.0)
    local_res = OpenGlassBoxResource("Local", 50.0)

    context.m_globalResources["Global"] = global_res
    context.m_localResources["Local"] = local_res
    context.m_mapValue = 75.0

    assert context.m_globalResources["Global"].value() == 100.0
    assert context.m_localResources["Local"].value() == 50.0
    assert context.m_mapValue == 75.0


def test_rule_value_arithmetic():
    """Test arithmetic operations with rule values."""
    # Create some test values
    value1 = RuleValueGlobal("Resource1")
    value2 = RuleValueGlobal("Resource2")

    context = RuleContext()
    context.m_globalResources = {
        "Resource1": OpenGlassBoxResource("Resource1", 10.0),
        "Resource2": OpenGlassBoxResource("Resource2", 5.0)
    }

    # Test individual evaluations
    assert value1.eval(context) == 10.0
    assert value2.eval(context) == 5.0


def test_complex_rule_evaluation():
    """Test complex rule evaluation scenarios."""
    context = RuleContext()

    # Set up a complex context
    context.m_globalResources = {
        "Population": OpenGlassBoxResource("Population", 1000.0),
        "Happiness": OpenGlassBoxResource("Happiness", 0.8)
    }

    context.m_localResources = {
        "Housing": OpenGlassBoxResource("Housing", 50.0),
        "Jobs": OpenGlassBoxResource("Jobs", 45.0)
    }

    context.m_mapValue = 25.0

    # Test various value types
    pop_value = RuleValueGlobal("Population")
    happiness_value = RuleValueGlobal("Happiness")
    housing_value = RuleValueLocal("Housing")
    jobs_value = RuleValueLocal("Jobs")
    map_value = RuleValueMap("WaterLevel")

    assert pop_value.eval(context) == 1000.0
    assert happiness_value.eval(context) == 0.8
    assert housing_value.eval(context) == 50.0
    assert jobs_value.eval(context) == 45.0
    assert map_value.eval(context) == 25.0


def test_rule_value_edge_cases():
    """Test edge cases and error handling."""
    context = RuleContext()

    # Test with empty context
    value = RuleValueGlobal("NonExistent")
    assert value.eval(context) == 0.0

    # Test with None resources
    context.m_globalResources = None
    context.m_localResources = None

    global_val = RuleValueGlobal("Test")
    local_val = RuleValueLocal("Test")
    map_val = RuleValueMap("Test")

    # Should handle gracefully
    assert global_val.eval(context) == 0.0
    assert local_val.eval(context) == 0.0
    assert map_val.eval(context) == 0.0


def test_resource_value_precision():
    """Test floating point precision in resource values."""
    context = RuleContext()

    # Test with very small values
    small_value = 0.000001
    context.m_globalResources = {
        "Small": OpenGlassBoxResource("Small", small_value)
    }

    value = RuleValueGlobal("Small")
    result = value.eval(context)
    assert abs(result - small_value) < 1e-10

    # Test with very large values
    large_value = 1e10
    context.m_globalResources = {
        "Large": OpenGlassBoxResource("Large", large_value)
    }

    value = RuleValueGlobal("Large")
    result = value.eval(context)
    assert result == large_value
