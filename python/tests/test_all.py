import pytest

# Import all test modules to ensure they are discovered and run
from . import test_resource
from . import test_agent
from . import test_city
from . import test_command
from . import test_coord_inside_radius
from . import test_map
from . import test_path
from . import test_resources
from . import test_simulation
from . import test_unit
from . import test_value
from . import test_script_parser
from . import test_vector

if __name__ == "__main__":
    pytest.main([__file__, "test_resource.py", "test_agent.py", "test_city.py", "test_command.py",
                 "test_coord_inside_radius.py", "test_map.py", "test_path.py", "test_resources.py",
                 "test_simulation.py", "test_unit.py", "test_value.py", "test_script_parser.py",
                 "test_vector.py"])
