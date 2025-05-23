import pytest

# Import all test modules to ensure they are discovered and run
import test_resource
import test_agent
import test_city
import test_command
import test_coord_inside_radius
import test_map
import test_path
import test_resources
import test_simulation
import test_unit
import test_value
import test_script_parser

if __name__ == "__main__":
    pytest.main([__file__, "test_resource.py", "test_agent.py", "test_city.py", "test_command.py",
                 "test_coord_inside_radius.py", "test_map.py", "test_path.py", "test_resources.py",
                 "test_simulation.py", "test_unit.py", "test_value.py", "test_script_parser.py"])
