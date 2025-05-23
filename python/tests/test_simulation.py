"""
Test suite for the Simulation class and city management logic.

This file covers:
- Construction and initialization of Simulation objects.
- Adding and retrieving City objects within the simulation.
- Verification of member variables, time, and city lookup logic.

The tests ensure that Simulation objects and their city management behave as expected, matching the requirements for simulation setup and city registration.
"""

import pytest

class Config:
    TICKS_PER_SECOND = 60

class Vector3f:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

class City:
    def __init__(self, name, position):
        self._name = name
        self._position = position
    def name(self):
        return self._name

class Simulation:
    def __init__(self, grid_u, grid_v):
        self.m_gridSizeU = grid_u
        self.m_gridSizeV = grid_v
        self.m_time = 0.0
        self.m_cities = {}

    def addCity(self, name, position):
        city = City(name, position)
        self.m_cities[name] = city
        return city

    def getCity(self, name):
        return self.m_cities[name]

def test_constants():
    assert Config.TICKS_PER_SECOND > 0

def test_constructor():
    sim = Simulation(4, 5)
    assert sim.m_gridSizeU == 4
    assert sim.m_gridSizeV == 5
    assert sim.m_time == 0.0
    assert len(sim.m_cities) == 0

    c1 = sim.addCity("Paris", Vector3f(0.0, 0.0, 0.0))
    assert c1.name() == "Paris"

    c2 = sim.getCity("Paris")
    assert c1 is c2
    assert c2.name() == "Paris"

    assert len(sim.m_cities) == 1
    assert sim.m_cities["Paris"] is c1
    assert sim.m_cities["Paris"].name() == "Paris"
