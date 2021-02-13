find_path(Blosc_INCLUDE_DIR blosc.h)

find_library(Blosc_LIBRARY NAMES blosc)

if (Blosc_INCLUDE_DIR AND Blosc_LIBRARY)
    set(Blosc_FOUND TRUE)
    set(Blosc_INCLUDE_DIRS ${Blosc_INCLUDE_DIR})
    set(Blosc_LIBRARIES ${Blosc_LIBRARY})
    message(STATUS "Found Blosc library: ${Blosc_LIBRARIES}")
else ()
    message(STATUS "No Blosc library found.  Using internal sources.")
endif ()