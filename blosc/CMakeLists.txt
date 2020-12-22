# Todo: c-blosc provides a CMake package configuration file that we can build
# against if blosc is available on the system, etc.
# find_package(blosc)
# if(NOT blosc_FOUND)
set(BUILD_STATIC ON CACHE BOOL "Build a static version of the blosc library.")
set(BUILD_SHARED ON CACHE BOOL "Build a shared library version of the blosc library.")
set(BUILD_TESTS OFF CACHE BOOL "Build test programs form the blosc compression library")
set(BUILD_BENCHMARKS OFF CACHE BOOL "Build benchmark programs form the blosc compression library")
set(BLOSC_IS_SUBPROJECT OFF CACHE BOOL "Blosc is subproject")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_subdirectory(c-blosc)
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/c-blosc/blosc")


add_library(blosc_extension MODULE blosc_extension.c)
target_link_libraries(blosc_extension blosc_static)
python_extension_module(blosc_extension)

add_custom_command(
    TARGET blosc_extension POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:blosc_extension> ${CMAKE_SOURCE_DIR}/blosc
)

install(TARGETS blosc_extension LIBRARY DESTINATION blosc)
