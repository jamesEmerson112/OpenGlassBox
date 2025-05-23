# Porting OpenGlassBox to Python – Integrated Plan

---

## 🚩 Todo List for Porting to Python

- [x] **1. Preparation & Scoping**
  - [x] Review C++ classes, relationships, and simulation flow
  - [x] Identify all core modules to port
  - [x] Set up `python/` directory and initialize a Python virtual environment
  - [x] Choose and configure a test framework (e.g., `pytest`)
  - [x] Plan to use modern Python tools (`dataclasses`, `typing`, etc.)

- [ ] **2. Iterative Porting (Repeat for Each Module)**
  - **C++ test files to port (in order):**
    - [x] TestsResource.cpp
    - [x] TestsAgent.cpp
    - [x] TestsCity.cpp
    - [x] TestsCommand.cpp
    - [x] TestsCoordInsideRadius.cpp
    - [x] TestsMap.cpp
    - [x] TestsPath.cpp
    - [x] TestsResources.cpp
    - [x] TestsScriptParser.cpp
    - [x] TestsSimulation.cpp
    - [x] TestsUnit.cpp
    - [x] TestsValue.cpp
  - **All C++ test files have been ported to Python.**
  - **Each Python test file includes a descriptive docstring summarizing its coverage and purpose.**
  - **A test runner script (`python/tests/test_all.py`) is provided to run all tests at once.**
  - **All tests are passing, and the Python port mirrors the C++ test suite in a test-driven manner.**

- [ ] **3. Module Implementation Checklist**
  - [ ] **Data Classes & Utilities**
    - [ ] **Resource** (Resource.hpp/cpp → resource.py)
      - [ ] Implement `Resource` class with proper type hints
      - [ ] Ensure proper initialization with name and value
      - [ ] Implement methods for modification and query (`Clone`, `Equals`, `ToString`)
      - [ ] Add Python-specific utility methods and properties
      - [ ] Complete type hints for all methods and properties
      - [ ] Add comprehensive docstrings

    - [ ] **RuleValue** (RuleValue.hpp/cpp → rule_value.py)
      - [ ] Port `RuleValue` class with type annotations
      - [ ] Implement different value types (constants, variables, operations)
      - [ ] Add evaluation methods
      - [ ] Implement ToString() and other debug utilities
      - [ ] Add proper docstrings and type information
      - [ ] Support operations (Add, Subtract, Multiply, Divide)

    - [ ] **Vector** (Vector.hpp → vector.py)
      - [ ] Create Vector2D class with type hints
      - [ ] Implement methods for vector operations (+, -, *, /)
      - [ ] Add utility methods (magnitude, normalization, etc.)
      - [ ] Implement equality and comparison operations
      - [ ] Add docstrings and examples

  - [ ] **Core Entities**
    - [ ] **Agent** (Agent.hpp/cpp → agent.py)
      - [ ] Port `Agent` class with proper type hints
      - [ ] Implement movement logic along paths
      - [ ] Add resource carrying capability
      - [ ] Implement update/simulation methods
      - [ ] Add proper initialization and reset methods
      - [ ] Ensure compatibility with Path and Resource classes
      - [ ] Add relevant agent status properties (position, resources, etc.)

    - [ ] **City** (City.hpp/cpp → city.py)
      - [ ] Port `City` class with all methods and properties
      - [ ] Implement map, path, and unit management
      - [ ] Add agent tracking and management
      - [ ] Implement entity creation methods
      - [ ] Handle simulation step processing
      - [ ] Ensure coordination of all simulation components
      - [ ] Add docstrings and examples

    - [ ] **Unit** (Unit.hpp/cpp → unit.py)
      - [ ] Port `Unit` class with proper type hints
      - [ ] Implement resource production/consumption logic
      - [ ] Add agent creation capabilities
      - [ ] Implement update/simulation methods
      - [ ] Handle activation/deactivation logic
      - [ ] Add proper initialization
      - [ ] Connect with city and path components

    - [ ] **Map** (Map.hpp/cpp → map.py)
      - [ ] Implement base `Map` class
      - [ ] Add grid functionality and coordinate system
      - [ ] Implement map cell access and modification methods
      - [ ] Create visualization utilities
      - [ ] Support resource spread mechanisms
      - [ ] Add map query operations
      - [ ] Include bounds checking and safety mechanisms

    - [ ] **Path** (Path.hpp/cpp → path.py)
      - [ ] Port `Path` class with Node and Way components
      - [ ] Implement path finding algorithms
      - [ ] Add methods for path traversal and manipulation
      - [ ] Ensure Node-Way connectivity is properly maintained
      - [ ] Implement path queries and searches
      - [ ] Add path utility methods (length, obstacles, etc.)

    - [ ] **Node** (part of Path implementation → node.py)
      - [ ] Create Node class for path nodes
      - [ ] Implement connection management
      - [ ] Add position and property data
      - [ ] Include search-related metadata
      - [ ] Add utility methods for node operations

  - [ ] **Simulation Logic**
    - [ ] **Simulation** (Simulation.hpp/cpp → simulation.py)
      - [ ] Port `Simulation` class as main control system
      - [ ] Implement simulation loop and update methods
      - [ ] Add proper time management
      - [ ] Create initialization and reset capabilities
      - [ ] Implement rule processing and triggering
      - [ ] Add event handling system
      - [ ] Support saving/loading simulation state

    - [ ] **Rule** (Rule.hpp/cpp → rule.py)
      - [ ] Port `Rule` class with condition and action components
      - [ ] Implement rule evaluation logic
      - [ ] Add command execution capabilities
      - [ ] Ensure proper rule triggering
      - [ ] Add rule management utilities
      - [ ] Include rule ordering and priority system

    - [ ] **RuleCommand** (RuleCommand.hpp/cpp → rule_command.py)
      - [ ] Port command types and execution logic
      - [ ] Implement all command actions from C++ version
      - [ ] Add parameter handling
      - [ ] Create command factory methods
      - [ ] Include execution context management
      - [ ] Support command sequencing

    - [ ] **ScriptParser** (ScriptParser.hpp/cpp → script_parser.py)
      - [ ] Port script parsing functionality
      - [ ] Implement token parsing and interpretation
      - [ ] Add error handling and reporting
      - [ ] Support comment handling
      - [ ] Create utilities for script validation
      - [ ] Add script debugging aids

    - [ ] **Resources** (Resources.hpp/cpp → resources.py)
      - [ ] Port `Resources` container class
      - [ ] Implement collection management methods
      - [ ] Add query and search capabilities
      - [ ] Include resource manipulation operations
      - [ ] Add serialization/deserialization support
      - [ ] Implement resource transfer mechanisms

    - [ ] **Dijkstra** (Dijkstra.hpp/cpp → dijkstra.py)
      - [ ] Port pathfinding algorithm
      - [ ] Implement priority queue and path tracking
      - [ ] Add cost calculations
      - [ ] Create path reconstruction
      - [ ] Include optimizations for large graphs
      - [ ] Support custom path cost functions

    - [ ] **MapCoordinatesInsideRadius** (MapCoordinatesInsideRadius.hpp/cpp → map_coordinates_inside_radius.py)
      - [ ] Port coordinate calculation within radius
      - [ ] Implement efficient radius searches
      - [ ] Add various radius shapes (circle, square)
      - [ ] Support weighted searches
      - [ ] Include boundary handling

    - [ ] **MapRandomCoordinates** (MapRandomCoordinates.hpp/cpp → map_random_coordinates.py)
      - [ ] Port random coordinate generation
      - [ ] Implement various distribution patterns
      - [ ] Add seed management for reproducibility
      - [ ] Include bounds checking and validation
      - [ ] Support constrained randomization

  - [ ] **Demo/UI**
    - [ ] **Choose Python UI Framework** (for demo.py)
      - [ ] Research suitable Python UI frameworks (pygame, pyglet, kivy, etc.)
      - [ ] Evaluate compatibility with simulation requirements
      - [ ] Assess performance for real-time simulation rendering
      - [ ] Consider cross-platform compatibility
      - [ ] Determine learning curve and documentation quality

    - [ ] **Port Demo Logic** (demo/src/* → demo.py)
      - [ ] Create base application structure
      - [ ] Implement rendering loop
      - [ ] Add user input handling
      - [ ] Port camera and view controls
      - [ ] Implement entity visualization
      - [ ] Create UI controls and panels
      - [ ] Add simulation control interface
      - [ ] Implement debug visualization options

- [ ] **4. Testing & Validation**
  - [ ] Ensure all tests pass for each ported module
  - [ ] Use code coverage tools (e.g., `pytest --cov`)
  - [ ] Compare Python and C++ test results for validation

- [ ] **5. Documentation & Examples**
  - [ ] Add docstrings to all Python modules and tests
  - [ ] Create example scripts in `python/` to demonstrate simulations

- [ ] **6. Continuous Improvement**
  - [ ] Refactor for Pythonic style and idioms
  - [ ] Add new tests for edge cases and new features
  - [ ] Optimize after correctness is established

---

**Migration will follow a "tests first" approach:**
For each module, port the C++ test file to Python first, then implement only enough of the Python module to make the test pass. This ensures correctness and incremental progress.

This document provides a comprehensive, actionable plan for porting the OpenGlassBox simulation engine from C++ to Python, integrating best practices from both traditional and test-driven development (TDD) approaches.

---

## 1. Preparation & Scoping

- **Understand the Codebase:** Review C++ classes, relationships, and simulation flow.
- **Identify Core Modules:** List all major components (Agent, City, Unit, Map, Resource, Rule, Simulation, etc.).
- **Set Up Python Environment:** Create a `python/` directory, initialize a virtual environment, and decide on a test framework (e.g., `pytest`).
- **Leverage Python Ecosystem:** Plan to use `dataclasses`, `typing`, `pytest`, and other modern Python tools.

---

## 2. Project Structure Overview

### Main Source Files (`src/` and `include/OpenGlassBox/`)
- Agent.cpp / Agent.hpp
- City.cpp / City.hpp
- Dijkstra.cpp / Dijkstra.hpp
- Map.cpp / Map.hpp
- MapCoordinatesInsideRadius.cpp / MapCoordinatesInsideRadius.hpp
- MapRandomCoordinates.cpp / MapRandomCoordinates.hpp
- Path.cpp / Path.hpp
- Resource.cpp / Resource.hpp
- Resources.cpp / Resources.hpp
- Rule.cpp / Rule.hpp
- RuleCommand.cpp / RuleCommand.hpp
- RuleValue.cpp / RuleValue.hpp
- ScriptParser.cpp / ScriptParser.hpp
- Simulation.cpp / Simulation.hpp
- Unit.cpp / Unit.hpp
- Vector.hpp (header only)

### Tests (`tests/`)
- main.cpp, main.hpp (test runner)
- TestsAgent.cpp
- TestsCity.cpp
- TestsCommand.cpp
- TestsCoordInsideRadius.cpp
- TestsMap.cpp
- TestsPath.cpp
- TestsResource.cpp
- TestsResources.cpp
- TestsScriptParser.cpp
- TestsSimulation.cpp
- TestsUnit.cpp
- TestsValue.cpp

---

## 3. Test-First, Iterative Porting Workflow

For each component (e.g., Agent), follow this detailed process:

### a. Port the Test

- **Translate the C++ test file** (e.g., `TestsAgent.cpp`) to Python (`test_agent.py`).
  - Map C++ test macros (e.g., `TEST`, `ASSERT_EQ`, `ASSERT_STREQ`) to Python's `unittest` or `pytest` assertions.
  - If the Python class does not exist yet, create stubs or mocks so the test can be written and run first.
- **Tips:**
  - Use `@unittest.skip` or `pytest.mark.skip` for incomplete tests.
  - Write docstrings for each test to clarify intent.

### b. Port the Implementation

- **Translate the C++ class** (e.g., `Agent`) to Python (`agent.py`).
  - Use Python idioms: classes, `@dataclass` for simple data holders, `list`/`dict` for containers.
  - Implement only enough to make the test pass.
- **Tips:**
  - Use type hints for clarity.
  - Document class and methods with docstrings.

### c. Run and Refine

- **Run the test** with `pytest` or `python -m unittest`.
  - Fix any issues in the implementation or test until the test passes.
  - Refactor for clarity and Pythonic style as you go.
- **Tips:**
  - Use code coverage tools (`pytest --cov`) to ensure all logic is tested.
  - Commit frequently to track progress and enable easy rollbacks.

### d. Repeat

- **Move to the next component** and repeat steps a–c.
  - Port the next test and its corresponding implementation.
  - Maintain a steady, incremental pace for reliability and maintainability.

---

## 4. Divide and Conquer: Migration Checklist

**For each item below, port the test file first, then the implementation.**
Use the C++ test output as a reference for expected results and edge cases.

### Data Classes & Utilities
- [ ] Resource.hpp/cpp → resource.py, test_resource.py
- [ ] RuleValue.hpp/cpp → rule_value.py, test_rule_value.py
- [ ] Vector.hpp → vector.py, test_vector.py

### Core Entities
- [ ] Agent.hpp/cpp → agent.py, test_agent.py
- [ ] City.hpp/cpp → city.py, test_city.py
- [ ] Unit.hpp/cpp → unit.py, test_unit.py
- [ ] Map.hpp/cpp → map.py, test_map.py
- [ ] Path.hpp/cpp → path.py, test_path.py
- [ ] Node (part of Map/Path) → node.py, test_node.py

### Simulation Logic
- [ ] Simulation.hpp/cpp → simulation.py, test_simulation.py
- [ ] Rule.hpp/cpp → rule.py, test_rule.py
- [ ] RuleCommand.hpp/cpp → rule_command.py, test_rule_command.py
- [ ] ScriptParser.hpp/cpp → script_parser.py, test_script_parser.py
- [ ] Resources.hpp/cpp → resources.py, test_resources.py
- [ ] Dijkstra.hpp/cpp → dijkstra.py, test_dijkstra.py
- [ ] MapCoordinatesInsideRadius.hpp/cpp → map_coordinates_inside_radius.py, test_map_coordinates_inside_radius.py
- [ ] MapRandomCoordinates.hpp/cpp → map_random_coordinates.py, test_map_random_coordinates.py

### Demo/UI (after core logic)
- [ ] Port demo logic to demo.py, test_demo.py (choose Python UI library)

---

## How to Run Python Tests

- With pytest:
  ```
  pytest python/tests/test_agent.py
  ```
- With unittest:
  ```
  python -m unittest python/tests/test_agent.py
  ```

---

## 5. Expanded Migration Table

| C++ Source/Test File                | Python Module/Test File                | Description/Notes                |
|-------------------------------------|----------------------------------------|----------------------------------|
| Agent.hpp / Agent.cpp               | agent.py                               | Core agent logic                 |
| TestsAgent.cpp                      | test_agent.py                          | Agent unit tests                 |
| City.hpp / City.cpp                 | city.py                                | City logic                       |
| TestsCity.cpp                       | test_city.py                           | City unit tests                  |
| Unit.hpp / Unit.cpp                 | unit.py                                | Unit logic                       |
| TestsUnit.cpp                       | test_unit.py                           | Unit unit tests                  |
| Map.hpp / Map.cpp                   | map.py                                 | Map logic                        |
| TestsMap.cpp                        | test_map.py                            | Map unit tests                   |
| Path.hpp / Path.cpp                 | path.py                                | Path logic                       |
| TestsPath.cpp                       | test_path.py                           | Path unit tests                  |
| Node (in Map/Path)                  | node.py                                | Node logic                       |
| Resource.hpp / Resource.cpp         | resource.py                            | Resource logic                   |
| TestsResource.cpp                   | test_resource.py                       | Resource unit tests              |
| Resources.hpp / Resources.cpp       | resources.py                           | Resource container logic         |
| TestsResources.cpp                  | test_resources.py                      | Resources unit tests             |
| Rule.hpp / Rule.cpp                 | rule.py                                | Rule logic                       |
| TestsValue.cpp                      | test_rule_value.py                     | Rule value tests                 |
| RuleValue.hpp / RuleValue.cpp       | rule_value.py                          | Rule value logic                 |
| RuleCommand.hpp / RuleCommand.cpp   | rule_command.py                        | Rule command logic               |
| TestsCommand.cpp                    | test_rule_command.py                   | Rule command tests               |
| ScriptParser.hpp / ScriptParser.cpp | script_parser.py                       | Script parsing logic             |
| TestsScriptParser.cpp               | test_script_parser.py                  | Script parser tests              |
| Simulation.hpp / Simulation.cpp     | simulation.py                          | Simulation engine                |
| TestsSimulation.cpp                 | test_simulation.py                     | Simulation tests                 |
| Dijkstra.hpp / Dijkstra.cpp         | dijkstra.py                            | Pathfinding logic                |
| MapCoordinatesInsideRadius.hpp/cpp  | map_coordinates_inside_radius.py        | Map radius logic                 |
| TestsCoordInsideRadius.cpp          | test_map_coordinates_inside_radius.py   | Map radius tests                 |
| MapRandomCoordinates.hpp/cpp        | map_random_coordinates.py               | Map random coord logic           |
| main.cpp / main.hpp (tests)         | test_main.py                            | Test runner (if needed)          |
| demo/src/*                          | demo.py                                 | Demo/UI logic                    |

---

## 6. Testing & Validation

- For each ported module, ensure all tests pass before moving on.
- Use code coverage tools (e.g., `pytest --cov`) to track test completeness.
- Compare Python test results with C++ test results for validation.
- Use TDD principles: write tests before or alongside implementation.

---

## 7. UI/Demo Port

- After the core logic is ported and tested, choose a Python UI library (e.g., `pygame`, `pyimgui`, `tkinter`).
- Port the demo logic, adapting event handling and rendering to the chosen library.

---

## 8. Documentation & Examples

- Document each Python module and test with docstrings.
- Create example scripts in the `python/` directory to demonstrate running simulations.
- Update this document with progress and lessons learned.

---

## 9. Continuous Improvement

- Refactor for Pythonic style (type hints, comprehensions, idiomatic error handling).
- Add new tests for uncovered edge cases or new features.
- Optimize only after correctness is established.

---

## Example Directory Structure

```
python/
  __init__.py
  agent.py
  city.py
  ...
  tests/
    __init__.py
    test_agent.py
    test_city.py
    ...
```

---

**Summary:**
- Use a test-first, incremental approach for reliability and maintainability.
- Leverage Python’s ecosystem and idioms for a clean, modern codebase.
- Validate correctness at every step by porting and running tests in parallel with the code.
