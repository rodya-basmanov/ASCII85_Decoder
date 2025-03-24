#include <gtest/gtest.h>
#include "../include/ASCII85.h"
#include <sstream>

TEST(ASCII85EncoderTest, EmptyInput) {
    std::vector<unsigned char> input;
    std::string encoded = encodeAscii85(input);
    EXPECT_EQ(encoded, "");
}

TEST(ASCII85EncoderTest, SimpleString) {
    std::string inputStr = "Hello, World!";
    std::vector<unsigned char> input(inputStr.begin(), inputStr.end());
    std::string encoded = encodeAscii85(input);
    EXPECT_EQ(encoded, "87cURD_*#4DfTZ)+T");
}

TEST(ASCII85EncoderTest, ZeroBytes) {
    std::vector<unsigned char> input = {0, 0, 0, 0};
    std::string encoded = encodeAscii85(input);
    EXPECT_EQ(encoded, "z");
}

TEST(ASCII85EncoderTest, PartialGroup) {
    std::vector<unsigned char> input = {'a', 'b', 'c'};
    std::string encoded = encodeAscii85(input);
    EXPECT_EQ(encoded, "FD,B"); // partial group (3 bytes) encodes to 4 characters
}

TEST(ASCII85DecoderTest, EmptyInput) {
    std::string input = "";
    std::vector<unsigned char> decoded = decodeAscii85(input);
    EXPECT_TRUE(decoded.empty());
}

TEST(ASCII85DecoderTest, SimpleString) {
    std::string input = "87cURD_*#4DfTZ)+T";
    std::vector<unsigned char> decoded = decodeAscii85(input);
    std::string decodedStr(decoded.begin(), decoded.end());
    EXPECT_EQ(decodedStr, "Hello, World!");
}

TEST(ASCII85DecoderTest, ZeroBytes) {
    std::string input = "z";
    std::vector<unsigned char> decoded = decodeAscii85(input);
    EXPECT_EQ(decoded.size(), 4);
    for (auto byte : decoded) {
        EXPECT_EQ(byte, 0);
    }
}

TEST(ASCII85DecoderTest, PartialGroup) {
    std::string input = "FD,B";
    std::vector<unsigned char> decoded = decodeAscii85(input);
    EXPECT_EQ(decoded.size(), 3);
    EXPECT_EQ(decoded[0], 'a');
    EXPECT_EQ(decoded[1], 'b');
    EXPECT_EQ(decoded[2], 'c');
}

TEST(ASCII85DecoderTest, WhitespaceHandling) {
    std::string input = "87cURD\n_*#4D\tfTZ)+T";
    std::vector<unsigned char> decoded = decodeAscii85(input);
    std::string decodedStr(decoded.begin(), decoded.end());
    EXPECT_EQ(decodedStr, "Hello, World!");
}

TEST(ASCII85DecoderTest, InvalidInput) {
    std::string input = "Invalid|ASCII85";
    std::vector<unsigned char> decoded = decodeAscii85(input);
    EXPECT_TRUE(decoded.empty());
}

TEST(ASCII85StreamTest, RoundTrip) {
    // Test round-trip via streams
    std::string original = "This is a test string for ASCII85 encoding and decoding.";
    
    // Encode
    std::istringstream iss(original);
    std::ostringstream encoded;
    encodeAscii85Stream(iss, encoded);
    
    // Decode
    std::istringstream iss2(encoded.str());
    std::ostringstream decoded;
    bool result = decodeAscii85Stream(iss2, decoded);
    
    EXPECT_TRUE(result);
    EXPECT_EQ(decoded.str(), original);
}

TEST(ASCII85StreamTest, MultipleZeroGroups) {
    // Test encoding/decoding with multiple zero groups
    std::vector<unsigned char> input(20, 0); // 20 zero bytes (5 groups of 4)
    
    // Encode
    std::string encodedStr = encodeAscii85(input);
    
    // Should be 5 'z' characters
    EXPECT_EQ(encodedStr, "zzzzz");
    
    // Decode
    std::vector<unsigned char> decoded = decodeAscii85(encodedStr);
    
    // Should be 20 zero bytes
    EXPECT_EQ(decoded.size(), 20);
    for (auto byte : decoded) {
        EXPECT_EQ(byte, 0);
    }
} 