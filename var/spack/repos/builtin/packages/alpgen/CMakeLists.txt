cmake_minimum_required(VERSION 2.6 FATAL_ERROR)
#----------------------------------------------------------------------------
project(alpgen Fortran)
#----------------------------------------------------------------------------

#---Compilation and Link options----------------------------------------------
if(CMAKE_SYSTEM_NAME MATCHES Darwin)
  set(CMAKE_SHARED_LIBRARY_CREATE_Fortran_FLAGS "${CMAKE_SHARED_LIBRARY_CREATE_Fortran_FLAGS} -flat_namespace -single_module -undefined dynamic_lookup")
endif()

set(CMAKE_Fortran_FLAGS_DEBUG          "-fPIC -g -fno-automatic -std=legacy")
set(CMAKE_Fortran_FLAGS_MINSIZEREL     "-fPIC -Os -DNDEBUG -fno-automatic -std=legacy")
set(CMAKE_Fortran_FLAGS_RELEASE        "-fPIC -O2 -DNDEBUG -fno-automatic -std=legacy")
set(CMAKE_Fortran_FLAGS_RELWITHDEBINFO "-fPIC -O2 -g -fno-automatic -std=legacy")



#---Select sources for the various libraries---------------------------------

file(GLOB alpgen_sources ${PROJECT_SOURCE_DIR}/alplib/Acp.f 
${PROJECT_SOURCE_DIR}/alplib/Acp.f ${PROJECT_SOURCE_DIR}/alplib/Aint.f ${PROJECT_SOURCE_DIR}/alplib/alpgen.f ${PROJECT_SOURCE_DIR}/alplib/alppdf.f 
${PROJECT_SOURCE_DIR}/alplib/alputi.f ${PROJECT_SOURCE_DIR}/alplib/Asu3.f)

file(GLOB alpgen_alpsho_sources ${PROJECT_SOURCE_DIR}/alplib/alpsho.f)

file(GLOB sources_libs RECURSIVE ${PROJECT_SOURCE_DIR}/*lib)
file(GLOB sources_work RECURSIVE ${PROJECT_SOURCE_DIR}/*work)
file(GLOB sources_rest RECURSIVE ${PROJECT_SOURCE_DIR}/DOCS ${PROJECT_SOURCE_DIR}/validation ${PROJECT_SOURCE_DIR}/examples )
file(GLOB source_readme compare prc.list README)

#---Add libraries------------------------------------------------------------


add_library(alpgen SHARED ${alpgen_sources})
add_library(alpgen_static STATIC ${alpgen_sources})
set_target_properties(alpgen PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/alplib)
set_target_properties(alpgen_static PROPERTIES OUTPUT_NAME alpgen ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/alplib)

add_library(alpsho SHARED ${alpgen_alpsho_sources})
add_library(alpsho_static STATIC ${alpgen_alpsho_sources})
set_target_properties(alpsho PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/alplib)
set_target_properties(alpsho_static PROPERTIES OUTPUT_NAME alpsho ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/alplib)

file(GLOB alpgen_herlib_sources ${PROJECT_SOURCE_DIR}/herlib/atoher.f)
file(GLOB alpgen_pylib_sources ${PROJECT_SOURCE_DIR}/pylib/atopyt.f)

add_library(atoher SHARED ${alpgen_herlib_sources})
add_library(atoher_static STATIC ${alpgen_herlib_sources})
set_target_properties(atoher PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/herlib)
set_target_properties(atoher_static PROPERTIES OUTPUT_NAME atoher ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/herlib)

add_library(atopyt SHARED ${alpgen_pylib_sources})
add_library(atopyt_static STATIC ${alpgen_pylib_sources})
set_target_properties(atopyt PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/pylib)
set_target_properties(atopyt_static PROPERTIES OUTPUT_NAME atopyt ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/herlib)

#---Install build products---------------------------------------------------
install(TARGETS alpgen alpsho atoher atopyt DESTINATION lib)
install(TARGETS alpgen_static alpsho_static atoher_static atopyt_static DESTINATION lib)

#---create subdirectory archive with symlinks----------------------------------
install(DIRECTORY ${sources_libs} ${sources_work} ${sources_rest}  DESTINATION ${CMAKE_INSTALL_PREFIX}/share/sources)
install(CODE "execute_process(COMMAND cmake -E create_symlink sources ${CMAKE_INSTALL_PREFIX}/share/alpgen-author)") 

install(CODE "file(MAKE_DIRECTORY ${CMAKE_INSTALL_PREFIX}/lib/archive)")
install(CODE "execute_process(COMMAND cmake -E create_symlink ../libalpgen.a ${CMAKE_INSTALL_PREFIX}/lib/archive/libalpgen.a)")
install(CODE "execute_process(COMMAND cmake -E create_symlink ../libalpsho.a ${CMAKE_INSTALL_PREFIX}/lib/archive/libalpsho.a)")
install(CODE "execute_process(COMMAND cmake -E create_symlink ../libatoher.a ${CMAKE_INSTALL_PREFIX}/lib/archive/libatoher.a)")
install(CODE "execute_process(COMMAND cmake -E create_symlink ../libatopyt.a ${CMAKE_INSTALL_PREFIX}/lib/archive/libatopyt.a)")
