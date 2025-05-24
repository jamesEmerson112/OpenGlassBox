# Python Demo Makefile
# Mirrors the structure of the C++ demo Makefile but for Python

.PHONY: all clean run

# Default target
all:
	@echo "Python demo is ready to run"

# Run the demo
run:
	python -m openglassbox.demo.src.demo

# Run the enhanced demo
run-enhanced:
	python -m openglassbox.demo.src.demo_enhanced

# Clean build artifacts
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +
	find . -name "*.so" -delete
	find . -name "*.c" -not -path "./src/*" -delete
