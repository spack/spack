cmake_minimum_required (VERSION 3.13)
project(spack_installer NONE)

set(PYTHON_VERSION "3.9.0" CACHE STRING "Version of Python to build.")
set(PY_DOWNLOAD_LINK "https://www.paraview.org/files/dependencies")
set(PY_FILENAME "Python-${PYTHON_VERSION}-win64.tar.xz")
set(PYTHON_DIR "Python-${PYTHON_VERSION}")

if (SPACK_VERSION)
  set(SPACK_DL "https://github.com/spack/spack/releases/download/v${SPACK_VERSION}")
  set(SPACK_FILENAME "spack-${SPACK_VERSION}.tar.gz")
  set(SPACK_DIR "spack-${SPACK_VERSION}")

  # SPACK DOWLOAD AND EXTRACTION-----------------------------------
  file(DOWNLOAD "${SPACK_DL}/${SPACK_FILENAME}"
    "${CMAKE_CURRENT_BINARY_DIR}/${SPACK_FILENAME}"
    STATUS download_status
  )
  list(GET download_status 0 res)
  if(res)
    list(GET download_status 1 err)
    message(FATAL_ERROR "Failed to download ${SPACK_FILENAME} ${err}")
  endif()
  message(STATUS "Successfully downloaded ${SPACK_FILENAME}")

  execute_process(COMMAND ${CMAKE_COMMAND} -E tar xfz
    "${CMAKE_CURRENT_BINARY_DIR}/${SPACK_FILENAME}"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    RESULT_VARIABLE res)
  if(NOT res EQUAL 0)
    message(FATAL_ERROR "Extraction of ${SPACK_FILENAME} failed.")
  endif()
  message(STATUS "Extracted ${SPACK_DIR}")
  SET(SPACK_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/${SPACK_DIR}")
elseif(SPACK_SOURCE)
  get_filename_component(SPACK_DIR ${SPACK_SOURCE} NAME)
else()
  message(FATAL_ERROR "Must specify SPACK_VERSION or SPACK_SOURCE")
endif()


# GIT DOWNLOAD----------------------------------------------------
set(GIT_FILENAME "Git-2.31.1-64-bit.exe")
file(DOWNLOAD "https://github.com/git-for-windows/git/releases/download/v2.31.1.windows.1/Git-2.31.1-64-bit.exe"
    "${CMAKE_CURRENT_BINARY_DIR}/${GIT_FILENAME}"
    STATUS download_status
    EXPECTED_HASH "SHA256=c43611eb73ad1f17f5c8cc82ae51c3041a2e7279e0197ccf5f739e9129ce426e"
)
list(GET download_status 0 res)
if(res)
  list(GET download_status 1 err)
  message(FATAL_ERROR "Failed to download ${GIT_FILENAME} ${err}")
endif()
message(STATUS "Successfully downloaded ${GIT_FILENAME}")


# PYTHON DOWLOAD AND EXTRACTION-----------------------------------
file(DOWNLOAD "${PY_DOWNLOAD_LINK}/${PY_FILENAME}"
  "${CMAKE_CURRENT_BINARY_DIR}/${PY_FILENAME}"
  STATUS download_status
  EXPECTED_HASH "SHA256=f6aeebc6d1ff77418678ed5612b64ce61be6bc9ef3ab9c291ac557abb1783420"
)
list(GET download_status 0 res)
if(res)
  list(GET download_status 1 err)
  message(FATAL_ERROR "Failed to download ${PY_FILENAME} ${err}")
endif()
message(STATUS "Successfully downloaded ${PY_FILENAME}")

execute_process(COMMAND ${CMAKE_COMMAND} -E tar xfz
  "${CMAKE_CURRENT_BINARY_DIR}/${PY_FILENAME}"
  WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
  RESULT_VARIABLE res)
if(NOT res EQUAL 0)
  message(FATAL_ERROR "Extraction of ${PY_FILENAME} failed.")
endif()
message(STATUS "Extracted ${PY_FILENAME}.")

# license must be a .txt or .rtf file
configure_file("${SPACK_LICENSE}" "${CMAKE_CURRENT_BINARY_DIR}/LICENSE.rtf" COPYONLY)


#INSTALLATION COMMANDS---------------------------------------------------
install(DIRECTORY "${SPACK_SOURCE}/"
  DESTINATION "${SPACK_DIR}")
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/Python-${PYTHON_VERSION}-win64/"
  DESTINATION "${PYTHON_DIR}")
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/scripts/" DESTINATION "scripts")
#install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/spack_cmd.bat/" DESTINATION ".")

# CPACK Installer Instructions
set(CPACK_PACKAGE_NAME "Spack")
set(CPACK_PACKAGE_VENDOR "Lawrence Livermore National Laboratories")
set(CPACK_PACKAGE_VERSION "0.16.0")
set(CPACK_PACKAGE_DESCRIPTION "A flexible package manager designed to support multiple versions, configurations, platforms, and compilers.")
set(CPACK_PACKAGE_HOMEPAGE_URL "https://spack.io")
set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}")
set(CPACK_PACKAGE_ICON "${SPACK_LOGO}")
set(CPACK_RESOURCE_FILE_README "${CMAKE_CURRENT_SOURCE_DIR}/README.md")
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_BINARY_DIR}/LICENSE.rtf")
#set(CPACK_RESOURCE_FILE_WELCOME "${CMAKE_CURRENT_SOURCE_DIR}/NOTICE")
# WIX options (the default)
set(CPACK_GENERATOR "WIX")
set(CPACK_WIX_PRODUCT_ICON "${SPACK_LOGO}")
set(CPACK_WIX_UI_BANNER "${CMAKE_CURRENT_SOURCE_DIR}/banner493x58.bmp")
set(CPACK_WIX_PATCH_FILE "${CMAKE_CURRENT_SOURCE_DIR}/patch.xml")
set(CPACK_WIX_UPGRADE_GUID "D2C703E4-721D-44EC-8016-BCB96BB64E0B")
set(CPACK_WIX_SKIP_PROGRAM_FOLDER TRUE)

# Set full path to icon, shortcut in spack.wxs
set(SPACK_SHORTCUT "${CMAKE_CURRENT_SOURCE_DIR}/spack_cmd.bat")
configure_file("spack.wxs.in" "${CMAKE_CURRENT_BINARY_DIR}/spack.wxs")
configure_file("bundle.wxs.in" "${CMAKE_CURRENT_BINARY_DIR}/bundle.wxs")
set(CPACK_WIX_EXTRA_SOURCES "${CMAKE_CURRENT_BINARY_DIR}/spack.wxs")

include(CPack)
