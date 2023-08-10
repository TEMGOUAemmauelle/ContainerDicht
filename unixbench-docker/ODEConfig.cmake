# ODE CMake Configuration file
#
# CMake variables are set by call:
#   FIND_PACKAGE(ODE REQUIRED) #ode only
#   FIND_PACKAGE(ODE REQUIRED drawstuff) #If you want to use Drawstuff
#
# These variables are provided:
# ODE_LIBS
# ODE_VERSION
# ODE_VERSION_MAJOR
# ODE_VERSION_MINOR
#
# If you use Drawstuff, this macro is provided:
#   DRAWSTUFF_TEXTURES_PATH:"/path/to/textures" (string define)


set(ODE_VERSION 0.12)
set(ODE_VERSION_MAJOR 0)
set(ODE_VERSION_MINOR 12)

include(FindPkgConfig)
pkg_check_modules(ODE REQUIRED ode)
if(ODE_FOUND)
	message(STATUS "  ODE_INCLUDE_DIRS= ${ODE_INCLUDE_DIRS}") 
	message(STATUS "  ODE_LIBRARIES= ${ODE_LIBRARIES}") 
	message(STATUS "  ODE_LIBRARY_DIRS= ${ODE_LIBRARY_DIRS}")
	message(STATUS "  ODE_CFLAGS= ${ODE_CFLAGS}")
endif()

if(${ODE_FIND_COMPONENTS} MATCHES drawstuff)
	pkg_check_modules(DS REQUIRED drawstuff)
	if(DS_FOUND)
		message(STATUS "  DS_INCLUDE_DIRS= ${DS_INCLUDE_DIRS}") 
		message(STATUS "  DS_LIBRARIES= ${DS_LIBRARIES}") 
		message(STATUS "  DS_LIBRARY_DIRS= ${DS_LIBRARY_DIRS}")
		message(STATUS "  DS_CFLAGS= ${DS_CFLAGS}")
		include(FindGLUT)
		include(FindOpenGL)
	endif()
endif()

link_directories(${ODE_LIBRARY_DIRS} ${DS_LIBRARY_DIRS})
include_directories(${ODE_INCLUDE_DIRS} ${DS_INCLUDE_DIRS})
add_definitions(${ODE_CFLAGS} ${DS_CFLAGS})
set(ODE_LIBS ${ODE_LIBRARIES} ${DS_LIBRARIES} ${GLUT_LIBRARIES} ${OPENGL_LIBRARIES})
