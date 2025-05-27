#include "OpenGlassBox/ScriptParser.hpp"
#include <iostream>

int main() {
    Script parser;
    if (!parser.parse("demo/data/Simulations/TestCity.txt")) {
        std::cerr << "Failed to parse script." << std::endl;
        return 1;
    }

    // Print resources
    std::cout << "Resources:" << std::endl;
    for (const auto& pair : parser.m_resources) {
        std::cout << "  " << pair.first << std::endl;
    }

    // Print maps
    std::cout << "Maps:" << std::endl;
    for (const auto& pair : parser.m_mapTypes) {
        std::cout << "  " << pair.first << std::endl;
    }

    // Print paths
    std::cout << "Paths:" << std::endl;
    for (const auto& pair : parser.m_pathTypes) {
        std::cout << "  " << pair.first << std::endl;
    }

    // Print units
    std::cout << "Units:" << std::endl;
    for (const auto& pair : parser.m_unitTypes) {
        std::cout << "  " << pair.first << std::endl;
    }

    // Print map rules
    std::cout << "Map Rules:" << std::endl;
    for (const auto& pair : parser.m_ruleMaps) {
        std::cout << "  " << pair.first << std::endl;
    }

    // Print unit rules
    std::cout << "Unit Rules:" << std::endl;
    for (const auto& pair : parser.m_ruleUnits) {
        std::cout << "  " << pair.first << std::endl;
    }

    return 0;
}
