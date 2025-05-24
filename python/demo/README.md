# OpenGlassBox Python Demo

This directory contains the Python implementation of the OpenGlassBox demo, mirroring the structure of the C++ demo in the root `demo/` directory.

## Directory Structure

```
python/demo/
├── data/
│   ├── Fonts/             # Font assets for UI
│   └── Simulations/       # Simulation definition files
│       ├── TestCity.txt
│       └── TestCity1.txt
├── src/
│   ├── Display/           # UI and display related code
│   │   └── debug_ui.py    # Debug UI implementation
│   ├── demo.py            # Basic demo implementation
│   ├── demo_enhanced.py   # Enhanced demo with additional features
│   ├── main.py            # Main entry point (mirrors main.cpp)
│   └── run_demo.py        # Demo runner utilities
└── Makefile               # Build and run tasks
```

## Running the Demo

```bash
# Run the basic demo
make run

# Run the enhanced demo
make run-enhanced

# Or run directly with Python
python -m openglassbox.demo.src.main
python -m openglassbox.demo.src.main --enhanced
```

This demo directory structure parallels the C++ implementation while providing a Pythonic interface to the OpenGlassBox simulation engine.
