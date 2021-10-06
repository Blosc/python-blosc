add_library(blosc_extension MODULE blosc_extension.c)

if(USE_SYSTEM_BLOSC)
    set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
    find_package(Blosc REQUIRED)
    target_include_directories(blosc_extension PRIVATE ${Blosc_INCLUDE_DIRS})
    target_link_libraries(blosc_extension ${Blosc_LIBRARIES})
else()
    set(BUILD_STATIC ON CACHE BOOL "Build a static version of the blosc library.")
    set(BUILD_SHARED ON CACHE BOOL "Build a shared library version of the blosc library.")
    set(BUILD_TESTS OFF CACHE BOOL "Build test programs form the blosc compression library")
    set(BUILD_BENCHMARKS OFF CACHE BOOL "Build benchmark programs form the blosc compression library")
    set(BLOSC_IS_SUBPROJECT OFF CACHE BOOL "Blosc is subproject")
    set(CMAKE_POSITION_INDEPENDENT_CODE ON)
    add_subdirectory(c-blosc)
    include_directories("${CMAKE_CURRENT_SOURCE_DIR}/c-blosc/blosc")
    target_link_libraries(blosc_extension blosc_static)
endif()



python_extension_module(blosc_extension)

add_custom_command(
    TARGET blosc_extension POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:blosc_extension> ${CMAKE_SOURCE_DIR}/blosc
)

install(TARGETS blosc_extension LIBRARY DESTINATION blosc)
