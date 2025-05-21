###################################################
# Location of the project directory and Makefiles
#
P := ..
M := $(P)/.makefile

###################################################
# Project definition
#
include $(P)/Makefile.common
TARGET_NAME := $(PROJECT_NAME)-demo
TARGET_DESCRIPTION := A demo using $(PROJECT_NAME)
include $(M)/project/Makefile

###################################################
# Compile the standalone application
#
SRC_FILES := $(call rwildcard,src,*.cpp)
INCLUDES := $(P)/include $(P)/demo/src $(P)
INCLUDES += $(P)/SDL2-2.32.6/x86_64-w64-mingw32/include $(P)/SDL2-2.32.6/x86_64-w64-mingw32/include/SDL2 $(P)/SDL2-2.32.6/SDL2_image-2.0.5/include
LINKER_FLAGS += -L$(P)/SDL2-2.32.6/SDL2_image-2.0.5/lib/x64 -lSDL2_image -L$(P)/SDL2-2.32.6/x86_64-w64-mingw32/lib -lmingw32 -lSDL2 -Wl,-e,mainCRTStartup -mconsole
VPATH := $(P)/demo
DEFINES := -DVIRTUAL= -DDESIRED_GRID_SIZE=30u
INTERNAL_LIBS := $(call internal-lib,$(PROJECT_NAME))
PKG_LIBS := sdl2 SDL2_image

###################################################
# Create MacOS X bundle application.
#
ifeq ($(OS),Darwin)
    BUILD_MACOS_APP_BUNDLE = 1
    APPLE_IDENTIFIER := lecrapouille
    MACOS_BUNDLE_ICON := data/$(PROJECT_NAME).icns
    LINKER_FLAGS := -framework CoreFoundation
endif

###################################################
# Generic Makefile rules
#
include $(M)/rules/Makefile

$(INTERNAL_LIBS):
