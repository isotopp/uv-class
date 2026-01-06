cmake_minimum_required(VERSION 3.20)
project(helloext LANGUAGES C)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

Python_add_library(_hello MODULE src/helloext/_hello.c)

set_target_properties(_hello PROPERTIES
  OUTPUT_NAME "_hello"
)

if (WIN32)
  set_target_properties(_hello PROPERTIES SUFFIX ".pyd")
endif()

install(TARGETS _hello LIBRARY DESTINATION helloext)
