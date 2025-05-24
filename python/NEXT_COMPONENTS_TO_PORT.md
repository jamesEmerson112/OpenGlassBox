# Next Components to Port

Based on the analysis of the current codebase, here are the next components that should be ported from C++ to Python:

## Pending Components

HIGHEST PRIORITY CHALLENGE:
"one second. I feel like we may have run into this errors whereas when triggering tests to triggering all of the tests inside tests/, we run into import problem where <resource> has to be turned into `.<resource>`, but if we demo programs from demo/, `.<resource` cannot be read so it has to be converted back to <resource>. investigate that problem for me"

SECOND HIGHEST PRIORITY CHALLENGE:
python/demo is not working as demo/ from .cpp version. please investigate

1. **Rule and RuleCommand**
   - Rule.cpp → rule.py (partial implementation exists)
   - RuleCommand.cpp → rule_command.py (partial implementation exists)
   - Testing and verification needed

2. **Simulation**
   - Simulation.cpp → simulation.py (partial implementation exists)
   - Complete implementation of simulation update logic
   - Testing and verification needed

3. **ScriptParser**
   - ScriptParser.cpp → script_parser.py (partial implementation exists)
   - Complete the parsing functionality
   - Add support for all script commands
   - Testing and verification needed

4. **Integration Components**
   - Complete demo_enhanced.py for the enhanced simulation demo
   - Complete debug_ui.py for visualization and debugging
   - Integration testing between components

## Recent Fixes

1. Fixed import issues in test files:
   - test_vector.py
   - test_resource.py
   - test_city.py
   - test_coord_inside_radius.py
   - test_path.py
   - test_dijkstra.py

2. Modified test structure to use relative imports correctly

3. **Project Structure Reorganization**
   - Implemented proper package structure with src/ directory
   - Created centralized imports in src/__init__.py to expose all classes
   - Updated demo code to use the src package structure
   - Fixed import conflicts between test modules and demo applications
   - Ensures consistent importing regardless of execution context

## Future Work

1. Performance optimization
   - Benchmarking the Python implementation against C++
   - Identifying bottlenecks and optimizing critical paths
   - Possible use of Cython for performance-critical sections

2. Additional features
   - Enhanced visualization capabilities
   - More complex simulation scenarios
   - Additional rule types and commands

3. Documentation
   - Complete API documentation
   - Usage examples
   - Tutorials for creating custom simulations
