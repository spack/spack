cmake_minimum_required(VERSION 2.6)

project(TinyXml)
OPTION(TIXML_PIC "Use positiion independent code" OFF)
OPTION(TIXML_USE_STL "Use STL with TIXML" ON)
if(TIXML_USE_STL)
	add_definitions(-DTIXML_USE_STL)
endif(TIXML_USE_STL)
add_library(
	tinyxml
	tinyxml.cpp
	tinystr.cpp
	tinyxmlerror.cpp
	tinyxmlparser.cpp
)
if(TIXML_PIC)
	set_target_properties(tinyxml PROPERTIES POSITION_INDEPENDENT_CODE ON)
endif(TIXML_PIC)
INSTALL( FILES tinyxml.h tinystr.h DESTINATION include )
INSTALL( TARGETS tinyxml ARCHIVE DESTINATION lib )
