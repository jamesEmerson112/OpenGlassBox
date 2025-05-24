#!/usr/bin/env python3
"""
Main entry point for the OpenGlassBox Python demo.
This file mirrors the functionality of demo/src/main.cpp in the C++ implementation.
"""

import sys
import os
import argparse

# Add parent directory to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from .demo import main as demo_main
from .demo_enhanced import main as demo_enhanced_main


def main():
    """Main entry point for the OpenGlassBox demo."""
    parser = argparse.ArgumentParser(description='OpenGlassBox Python Demo')
    parser.add_argument('--enhanced', action='store_true',
                        help='Run the enhanced demo with more visualization features')
    parser.add_argument('--simulation', type=str, default='TestCity.txt',
                        help='Path to the simulation file to load')
    args = parser.parse_args()

    # Set up the simulation path
    simulation_path = os.path.join(
        os.path.dirname(__file__),
        '../data/Simulations',
        args.simulation
    )

    if args.enhanced:
        demo_enhanced_main(simulation_path)
    else:
        demo_main(simulation_path)


if __name__ == "__main__":
    main()
