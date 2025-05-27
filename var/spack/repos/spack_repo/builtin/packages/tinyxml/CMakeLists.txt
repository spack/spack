cmake_minimum_required(VERSION 2.6)

project(TinyXml)

OPTION(TIXML_USE_STL "Use STL with TIXML" ON)
OPTION(BUILD_SHARED_LIBS "build as shared library" ON)

if(TIXML_USE_STL)
	add_definitions(-DTIXML_USE_STL)
endif(TIXML_USE_STL)

if(BUILD_SHARED_LIBS)
  add_library(tinyxml SHARED tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp)
  install(TARGETS tinyxml LIBRARY DESTINATION lib)
else()
  add_library(tinyxml_static STATIC tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp)
  set_target_properties(tinyxml_static PROPERTIES OUTPUT_NAME tinyxml)
  install(TARGETS tinyxml_static ARCHIVE DESTINATION lib)
endif(BUILD_SHARED_LIBS)

install(FILES tinyxml.h tinystr.h DESTINATION include)
