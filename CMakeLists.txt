cmake_minimum_required(VERSION 3.16)
project(CACT_PR001 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(Java 11 REQUIRED COMPONENTS Runtime)
find_package(Threads REQUIRED)
set(GENERATED "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(GRAMMAR "${CMAKE_CURRENT_SOURCE_DIR}/grammar/CACT.g4")
set(ANTLR_JAR "${CMAKE_CURRENT_SOURCE_DIR}/deps/antlr-4.13.1-complete.jar")
set(GENERATED_SOURCES "${GENERATED}/CACTLexer.cpp" "${GENERATED}/CACTParser.cpp"
    "${GENERATED}/CACTBaseVisitor.cpp" "${GENERATED}/CACTVisitor.cpp")
add_custom_command(
    OUTPUT ${GENERATED_SOURCES} "${GENERATED}/CACTLexer.h" "${GENERATED}/CACTParser.h"
    COMMAND ${CMAKE_COMMAND} -E make_directory "${GENERATED}"
    COMMAND ${Java_JAVA_EXECUTABLE} -jar "${ANTLR_JAR}" -Dlanguage=Cpp
        -visitor -no-listener -o "${GENERATED}" CACT.g4
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/grammar"
    DEPENDS "${GRAMMAR}" "${ANTLR_JAR}" VERBATIM)
file(GLOB_RECURSE ANTLR_SOURCES CONFIGURE_DEPENDS "deps/antlr4-runtime/*.cpp")
add_library(antlr STATIC ${ANTLR_SOURCES})
target_include_directories(antlr PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/deps/antlr4-runtime")
target_link_libraries(antlr PUBLIC Threads::Threads)
add_executable(compiler src/main.cpp ${GENERATED_SOURCES})
target_include_directories(compiler PRIVATE "${GENERATED}")
target_link_libraries(compiler PRIVATE antlr)
target_compile_options(compiler PRIVATE -Wall -Wextra)
enable_testing()
find_package(Python3 COMPONENTS Interpreter)
if(Python3_FOUND)
    add_test(NAME pr001_checks COMMAND ${Python3_EXECUTABLE}
        "${CMAKE_CURRENT_SOURCE_DIR}/test/test_pr001.py" $<TARGET_FILE:compiler>)
endif()
