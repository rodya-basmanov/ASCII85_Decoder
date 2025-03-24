## Author Basmanov Rodion 24.B81-mm
## Contacts st135699@student.spbu.ru

# ASCII85 Encoder/Decoder

A program for encoding and decoding data using the ASCII85 algorithm. This command-line utility works similarly to the standard Unix `base64` utility.

## Project Structure

```
.
├── bin/        # Executable files
├── include/    # Header files
├── obj/        # Object files
├── src/        # Source files
├── test/       # Functional test scripts
└── tests/      # Unit tests
```

## Compilation

To compile the program, simply run:

```
make
```

This will create the executable in the `bin` directory.

## Usage

```
./bin/main      # reads bytes from STDIN and outputs ASCII85 to STDOUT
./bin/main -e   # same as above
./bin/main -d   # reads ASCII85 from STDIN and outputs bytes to STDOUT
```

Examples:

```
# Encoding
echo -n "Hello, World!" | ./bin/main

# Decoding
echo -n "87cURD]i,\"Cht" | ./bin/main -d

# Encoding a file
cat input.bin | ./bin/main > encoded.txt

# Decoding a file
cat encoded.txt | ./bin/main -d > decoded.bin
```

## Testing

### Installing GoogleTest

Before running the tests, you need to install GoogleTest:

```
make install_gtest
```

Or manually:

```
sudo apt-get install libgtest-dev
cd /usr/src/gtest
sudo cmake .
sudo make
sudo cp lib/*.a /usr/lib
```

### Running Tests

To build and run the unit tests:

```
make run_tests
```

Alternatively, you can run the script:

```
cd tests
./run_tests.sh
```

### Tests Coverage

The test suite covers:
- Empty input handling
- Basic string encoding/decoding
- Special cases (zero bytes)
- Partial groups
- Whitespace handling 
- Invalid input handling
- Stream-based operations
- Round-trip encoding and decoding

## CI/CD

The project uses GitHub Actions for Continuous Integration. On each push or pull request to main branches, the following actions are performed:
- Building the project
- Running all tests

## About ASCII85 Format

ASCII85 is a data encoding format that converts binary data to ASCII text. It uses 5 ASCII characters to represent 4 bytes of binary data, making it more efficient than Base64 (which uses 4 characters to represent 3 bytes).

Features:
- Uses ASCII characters from '!' (33) to 'u' (117)
- Special character 'z' represents a group of four zero bytes
- Whitespace characters are ignored when decoding

## Implementation

This implementation supports:
- Stream processing (allows working with data of arbitrary length)
- Correct handling of incomplete groups at the end of the stream
- Processing the special 'z' character
- Returns non-zero exit code on decoding errors 