CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
INCLUDES = -Iinclude
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin
TESTS_DIR = tests

# Create directory if it doesn't exist
$(shell mkdir -p $(OBJ_DIR) $(BIN_DIR))

# Source files
SRCS = $(SRC_DIR)/ASCII85.cpp
OBJS = $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRCS))
MAIN_SRC = $(SRC_DIR)/main.cpp
MAIN_OBJ = $(OBJ_DIR)/main.o
TARGET = $(BIN_DIR)/main

# Test files
TEST_SRCS = $(TESTS_DIR)/ASCII85_test.cpp
TEST_OBJS = $(patsubst $(TESTS_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(TEST_SRCS))
TEST_TARGET = $(BIN_DIR)/ascii85_tests

# GoogleTest
GTEST_LIBS = -lgtest -lgtest_main -pthread

# Default target
all: $(TARGET)

# Main program
$(TARGET): $(OBJS) $(MAIN_OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(MAIN_OBJ): $(MAIN_SRC)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<

# Library objects
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<

# Test objects
$(OBJ_DIR)/%.o: $(TESTS_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<

# Build tests
tests: $(TEST_TARGET)

$(TEST_TARGET): $(OBJS) $(TEST_OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(GTEST_LIBS)

# Run tests
run_tests: tests
	$(TEST_TARGET)

# Install GoogleTest (Ubuntu/Debian)
install_gtest:
	sudo apt-get update
	sudo apt-get install -y libgtest-dev
	cd /usr/src/gtest && sudo cmake . && sudo make && sudo cp lib/*.a /usr/lib

# Clean
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

# Phony targets
.PHONY: all clean tests run_tests install_gtest 