#ifndef ASCII85_H
#define ASCII85_H

#include <vector>
#include <string>
#include <iostream>

// Function to encode data to ASCII85
std::string encodeAscii85(const std::vector<unsigned char>& data);

// Function to decode ASCII85
std::vector<unsigned char> decodeAscii85(const std::string& input);

// Encode binary data from input stream to ASCII85 in output stream
void encodeAscii85Stream(std::istream& in, std::ostream& out);

// Decode ASCII85 from input stream to binary data in output stream
bool decodeAscii85Stream(std::istream& in, std::ostream& out);

#endif 