OS := Windows
WIN_ENV := MINGW
EXT_BINARY := .exe
EXT_DYNAMIC_LIB := .dll
EXT_STATIC_LIB := .lib
CC := gcc
CXX := g++

# Windows-specific local overrides
# Add include path for SDL2 and link the SDL2 library from the downloaded folder
CXXFLAGS += -I$(P)/SDL2-2.32.6/x86_64-w64-mingw32/include
LDFLAGS += -L$(P)/SDL2-2.32.6/x86_64-w64-mingw32/lib -lmingw32 -lSDL2
