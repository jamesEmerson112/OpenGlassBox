"""
Configuration constants for OpenGlassBox simulation engine.

This module defines global configuration constants that match the C++ Config.hpp.
These constants control various aspects of the simulation behavior and rendering.
"""

# Screen/window configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Grid configuration
# Note: DESIRED_GRID_SIZE appears to be a compile-time macro in C++
# For Python, we'll use a reasonable default
GRID_SIZE = 12

# Simulation timing configuration
TICKS_PER_SECOND = 10.0

# Additional Python-specific configuration
DEFAULT_WINDOW_TITLE = "OpenGlassBox Simulation"
DEFAULT_FPS = 60

# Color constants (commonly used colors)
class Colors:
    """Common color constants in hex format."""
    WHITE = 0xFFFFFF
    BLACK = 0x000000
    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    YELLOW = 0xFFFF00
    CYAN = 0x00FFFF
    MAGENTA = 0xFF00FF
    GRAY = 0x808080
    DARK_GRAY = 0x404040
    LIGHT_GRAY = 0xC0C0C0

# Resource limits
class ResourceLimits:
    """Configuration for resource system limits."""
    MAX_CAPACITY = 999999  # Matches Resource::MAX_CAPACITY from C++
    DEFAULT_CAPACITY = 100

# Simulation limits
class SimulationLimits:
    """Configuration for simulation performance limits."""
    MAX_ITERATIONS_PER_UPDATE = 10  # Matches C++ Simulation
    MAX_CITIES = 100
    MAX_AGENTS_PER_CITY = 1000
    MAX_UNITS_PER_CITY = 1000

# Path/navigation configuration
class PathConfig:
    """Configuration for pathfinding and navigation."""
    DEFAULT_NODE_RADIUS = 5.0
    DEFAULT_WAY_WIDTH = 2.0
    MAX_PATH_FINDING_ITERATIONS = 1000

# Map configuration
class MapConfig:
    """Configuration for map and terrain systems."""
    DEFAULT_MAP_SIZE_U = 12
    DEFAULT_MAP_SIZE_V = 12
    DEFAULT_CELL_SIZE = 10.0
