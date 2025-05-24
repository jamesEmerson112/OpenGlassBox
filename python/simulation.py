"""
Simulation module for OpenGlassBox simulation engine.

This module provides the main entry point for the simulation system:
- The Simulation class manages a collection of City objects
- Handles updating of all simulation components
- Provides event listeners for simulation lifecycle events
- Inherits from Script to access parsed script resources

The Simulation class is responsible for maintaining the global state of the
simulation and coordinating updates across all cities.
"""

from typing import Dict, Optional, Dict, Union, Any
from abc import ABC, abstractmethod

from .city import City
from .vector import Vector3f
from .script_parser import Script

# Constants for simulation timing
MAX_ITERATIONS_PER_UPDATE = 20
TICKS_PER_SECOND = 200.0


class Simulation(Script):
    """
    Entry point class managing a collection of Cities and running simulation on them.

    The Simulation class extends Script to access parsed simulation resources and
    manages the creation, retrieval, and updating of city objects within the simulation.
    In the current phase of development, cities are not connected between them.
    """

    class Listener(ABC):
        """
        Abstract base class for simulation event listeners.

        Implement this interface to receive notifications about simulation events
        such as cities being added or removed.
        """

        def on_city_added(self, city: City) -> None:
            """
            Called when a city is added to the simulation.

            Args:
                city: The city that was added
            """
            pass

        def on_city_removed(self, city: City) -> None:
            """
            Called when a city is removed from the simulation.

            Args:
                city: The city that was removed
            """
            pass

    class DefaultListener(Listener):
        """Default implementation of the Listener interface that does nothing."""
        pass

    def __init__(self, grid_size_u: int = 32, grid_size_v: int = 32):
        """
        Create a simulation game.

        Args:
            grid_size_u: The grid dimension along the U-axis for creating maps
            grid_size_v: The grid dimension along the V-axis for creating maps
        """
        super().__init__()
        self.m_gridSizeU = grid_size_u
        self.m_gridSizeV = grid_size_v
        self.m_time = 0.0
        self.m_cities: Dict[str, City] = {}
        self.m_listener: Simulation.Listener = Simulation.DefaultListener()

    def set_listener(self, listener: 'Simulation.Listener') -> None:
        """
        Set the listener for simulation events.

        Args:
            listener: The listener object to receive event notifications
        """
        self.m_listener = listener

    def update(self, delta_time: float) -> None:
        """
        Update the game simulation.

        Args:
            delta_time: The delta of time in seconds from the previous update
        """
        self.m_time += delta_time

        # Rules are executed at TICKS_PER_SECOND intervals
        max_iterations = MAX_ITERATIONS_PER_UPDATE
        while (self.m_time >= 1.0 / TICKS_PER_SECOND) and (max_iterations > 0):
            self.m_time -= 1.0 / TICKS_PER_SECOND
            max_iterations -= 1

            for city in self.m_cities.values():
                city.update()

    def add_city(self, name: str, position: Vector3f) -> City:
        """
        Create a new City and replace the previous city if it already exists.

        Args:
            name: The name of the city to add
            position: The position of the city in world coordinates

        Returns:
            The newly created City object
        """
        city = City(name, position, self.m_gridSizeU, self.m_gridSizeV)
        self.m_cities[name] = city
        self.m_listener.on_city_added(city)
        return city

    def get_city(self, name: str) -> City:
        """
        Get the City referred to by its name.

        Args:
            name: The name of the city to retrieve

        Returns:
            The City object with the given name

        Raises:
            KeyError: If the given name does not match any held cities
        """
        return self.m_cities[name]

    def cities(self) -> Dict[str, City]:
        """
        Get the collection of cities.

        Returns:
            Dictionary mapping city names to City objects
        """
        return self.m_cities
