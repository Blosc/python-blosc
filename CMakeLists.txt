cmake_minimum_required(VERSION 3.11.0)
project(python-blosc)
find_package(PythonExtensions REQUIRED)

# Todo: c-blosc provides a CMake package configuration file that we can build
# against if blosc is available on the system, etc.
# find_package(blosc)
# if(NOT blosc_FOUND)
set(BUILD_STATIC ON CACHE BOOL "Build a static version of the blosc library.")
set(BUILD_SHARED OFF CACHE BOOL "Build a shared library version of the blosc library.")
set(BUILD_TESTS OFF CACHE BOOL "Build test programs form the blosc compression library")
set(BUILD_BENCHMARKS OFF CACHE BOOL "Build benchmark programs form the blosc compression library")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_subdirectory(c-blosc)

add_library(blosc_extension MODULE blosc/blosc_extension.c)
target_link_libraries(blosc_extension blosc_static)
python_extension_module(blosc_extension)
install(TARGETS blosc_extension LIBRARY DESTINATION blosc)
