#include "../include/ASCII85.h"
#include <iostream>
#include <cstring>

void printUsage(const char* programName) {
    std::cerr << "Usage: " << programName << " [-e | -d]" << std::endl;
    std::cerr << "  -e  Encode (default mode)" << std::endl;
    std::cerr << "  -d  Decode" << std::endl;
}

int main(int argc, char* argv[]) {
    bool encode = true;  // Default mode is encode

    // Parse command line arguments
    if (argc > 2) {
        printUsage(argv[0]);
        return 1;
    } else if (argc == 2) {
        if (std::strcmp(argv[1], "-e") == 0) {
            encode = true;
        } else if (std::strcmp(argv[1], "-d") == 0) {
            encode = false;
        } else {
            printUsage(argv[0]);
            return 1;
        }
    }

    // Make sure we read binary data correctly
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    
    if (encode) {
        std::cin.unsetf(std::ios::skipws);
        encodeAscii85Stream(std::cin, std::cout);
    } else {
        if (!decodeAscii85Stream(std::cin, std::cout)) {
            std::cerr << "Error: invalid ASCII85 data for decoding" << std::endl;
            return 1;
        }
    }

    return 0;
} 