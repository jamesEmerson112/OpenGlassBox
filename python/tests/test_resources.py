"""
Test suite for the Resources class (resource collections).

This file covers:
- Construction and initialization of Resources collections.
- Adding, removing, and transferring resources between collections.
- Capacity management, edge cases, and resource lookup logic.
- Self-transfer and self-addition edge cases.

The tests ensure that resource collections behave as expected for all basic operations, matching the logic and constraints of the original C++ simulation engine.
"""

import pytest
from .. import resource
from ..resource import Resource
from ..resources import Resources


def test_constructor():
    """Test the constructor creates an empty resources container."""
    house = Resources()
    assert len(house.m_bin) == 0
    assert house.isEmpty() is True


def test_empty_collection():
    """Test operations on an empty collection."""
    house = Resources()
    assert house.findResource("people") is None
    assert house.hasResource("people") is False

    house.removeResource("people", 10)
    assert len(house.m_bin) == 0
    assert house.isEmpty() is True

    assert house.canAddSomeResources(house) is False
    assert house.getAmount("people") == 0
    assert house.getCapacity("people") == 0

    house.removeResources(house)
    assert house.getAmount("people") == 0
    assert house.getCapacity("people") == 0


def test_nominal():
    """Test nominal operations on resources."""
    house = Resources()

    # Add a new resource "people". Check if the new resource has been added.
    r1 = house.addResource("people", 0)
    assert len(house.m_bin) == 1
    assert r1.type() == "people"
    assert house.m_bin[0].type() == "people"
    assert house.getAmount("people") == 0
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    assert house.isEmpty() is True
    assert house.canAddSomeResources(house) is False

    # Add a new resource "car". Check if the new resource has been added.
    r2 = house.addResource("car", 2)
    assert len(house.m_bin) == 2
    assert r2.type() == "car"
    assert house.m_bin[0].type() == "people"
    assert house.m_bin[1].type() == "car"
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 2
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    assert house.getCapacity("car") == Resource.MAX_CAPACITY
    assert house.isEmpty() is False
    assert house.canAddSomeResources(house) is False

    # Check self transfer of resources does nothing
    house.removeResources(house)
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 2
    house.addResources(house)
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 2

    # Add more to the "car" resource. Check if the amount has changed.
    r3 = house.addResource("car", 8)
    assert len(house.m_bin) == 2
    assert r3.type() == "car"
    assert house.m_bin[0].type() == "people"
    assert house.m_bin[1].type() == "car"
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 10
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    assert house.getCapacity("car") == Resource.MAX_CAPACITY
    assert house.isEmpty() is False

    # Reduce amount resource "car". Check if the amount has changed.
    res = house.removeResource("car", 5)
    assert res is True
    assert len(house.m_bin) == 2
    assert house.m_bin[0].type() == "people"
    assert house.m_bin[1].type() == "car"
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 5
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    assert house.getCapacity("car") == Resource.MAX_CAPACITY
    assert house.isEmpty() is False

    # Change capacity for resource "car". Check if the amount has been changed.
    assert house.getCapacity("car") == Resource.MAX_CAPACITY
    house.setCapacity("car", 2)
    assert house.getCapacity("car") == 2
    assert house.getAmount("car") == 2

    # Change capacity for all resources in the collection.
    caps = Resources()
    caps.setCapacity("car", 20)
    caps.setCapacity("people", 10)
    caps.setCapacity("trash", 10)
    assert len(caps.m_bin) == 3
    assert caps.m_bin[0].type() == "car"
    assert caps.m_bin[1].type() == "people"
    assert caps.m_bin[2].type() == "trash"
    assert caps.getCapacity("car") == 20
    assert caps.getCapacity("people") == 10
    assert caps.getCapacity("trash") == 10

    assert len(house.m_bin) == 2  # before
    assert house.getCapacity("car") == 2
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    house.setCapacities(caps)
    assert len(house.m_bin) == 3  # after
    assert house.getCapacity("car") == 20
    assert house.getCapacity("people") == 10
    assert house.getCapacity("trash") == 10

    # Change amount for all resources in the collection.
    toAdd = Resources()
    toAdd.addResource("car", 5)
    toAdd.addResource("people", 2)
    toAdd.addResource("trash", 10)
    assert toAdd.getAmount("car") == 5
    assert toAdd.getAmount("people") == 2
    assert toAdd.getAmount("trash") == 10

    assert house.getAmount("car") == 2  # before
    assert house.getAmount("people") == 0
    house.addResources(toAdd)
    assert house.getAmount("car") == 7  # after
    assert house.getAmount("people") == 2
    assert house.getAmount("trash") == 10
    house.removeResources(toAdd)
    assert house.getAmount("car") == 2
    assert house.getAmount("people") == 0
    assert house.getAmount("trash") == 0


def test_can_add_some_resources():
    """Test canAddSomeResources functionality."""
    house = Resources()
    foo = Resources()

    # Empty collections
    ret = house.canAddSomeResources(foo)
    assert ret is False

    # One collection has resources but the other doesn't have that type
    foo.addResource("car", 5)
    ret = house.canAddSomeResources(foo)
    assert ret is False

    # Both collections have the same resource type
    house.addResource("car", 5)
    ret = house.canAddSomeResources(foo)
    assert ret is True

    # Resources at capacity
    house.setCapacity("car", 5)
    ret = house.canAddSomeResources(foo)
    assert ret is False

    # Self check
    ret = house.canAddSomeResources(house)
    assert ret is False


def test_transfer_resources_to():
    """Test transferResourcesTo functionality."""
    house = Resources()
    foo = Resources()

    # Set up initial resources
    house.addResource("car", 5)
    foo.addResource("oil", 5)
    foo.addResource("car", 5)

    # Transfer resources
    house.transferResourcesTo(foo)
    assert house.getAmount("car") == 0
    assert foo.getAmount("car") == 10
    assert foo.getAmount("oil") == 5

    # Test transfer with capacity limits
    house.addResource("car", 5)
    foo.setCapacity("car", 12)
    house.transferResourcesTo(foo)
    assert house.getAmount("car") == 3
    assert foo.getAmount("car") == 12


def test_string_representation():
    """Test string representation of resources."""
    resources = Resources()
    resources.addResource("water", 5)
    resources.addResource("electricity", 10)

    # Check __str__ output
    str_repr = str(resources)
    assert "2 Resources:" in str_repr
    assert "Resource water: 5/" in str_repr
    assert "Resource electricity: 10/" in str_repr

    # Check __repr__ output
    repr_str = repr(resources)
    assert "Resources([" in repr_str
