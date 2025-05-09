#!/usr/bin/env python3
import subprocess
import random
import base64
import time
import sys
import os

EXECUTABLE = "../bin/main"

def run_encode(input_data):
    process = subprocess.run([EXECUTABLE, "-e"], 
                            input=input_data, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            check=False)
    return process.stdout, process.returncode

def run_decode(input_data):
    process = subprocess.run([EXECUTABLE, "-d"], 
                            input=input_data, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            check=False)
    return process.stdout, process.returncode

def generate_random_bytes(length):
    return os.urandom(length)

def test_encode_decode():
    print("\n=== Testing encoding and decoding ===")
    success = 0
    count = 10
    
    for i in range(count):
        length = random.randint(1, 1000)
        random_bytes = generate_random_bytes(length)
        
        encoded, encode_return_code = run_encode(random_bytes)
        
        if encode_return_code != 0:
            print(f"Error: Test {i+1}: Encoder returned non-zero code {encode_return_code}")
            continue

        decoded, decode_return_code = run_decode(encoded)
        
        if decode_return_code != 0:
            print(f"Error: Test {i+1}: Decoder returned non-zero code {decode_return_code}")
            continue
            
        if decoded == random_bytes:
            print(f"Success: Test {i+1}: Round-trip successful for {length} bytes")
            success += 1
        else:
            print(f"Error: Test {i+1}: Data mismatch after round-trip")
            
    print(f"\nTotal: {success}/{count} tests passed\n")
    return success == count

def test_empty_input():
    print("\n=== Empty input test ===")
    
    encoded, encode_return_code = run_encode(b"")
    
    if encode_return_code != 0:
        print("Error: Encoder returned non-zero code for empty input")
        return False
        
    if encoded != b"":
        print(f"Error: Encoded data for empty input should be empty, received: {encoded}")
        return False
    
    decoded, decode_return_code = run_decode(b"")
    
    if decode_return_code != 0:
        print("Error: Decoder returned non-zero code for empty input")
        return False
    
    if decoded != b"":
        print(f"Error: Decoded data for empty input should be empty, received: {decoded}")
        return False
    
    print("Success: Empty input test passed")
    return True

def test_special_bytes():
    print("\n=== Special bytes test ===")
    success = 0
    total_tests = 3
    
    zeros = bytes([0] * 20)
    encoded, encode_return_code = run_encode(zeros)
    
    if encode_return_code == 0:
        decoded, decode_return_code = run_decode(encoded)
        
        if decode_return_code == 0 and decoded == zeros:
            print("Success: Zero bytes encoding/decoding successful")
            success += 1
        else:
            print("Error: Data mismatch when encoding/decoding zero bytes")
    
    binary_data = bytes(range(256))
    encoded, encode_return_code = run_encode(binary_data)
    
    if encode_return_code == 0:
        decoded, decode_return_code = run_decode(encoded)
        
        if decode_return_code == 0 and decoded == binary_data:
            print("Success: Binary data encoding/decoding successful")
            success += 1
        else:
            print("Error: Data mismatch when encoding/decoding binary data")
    
    control_chars = bytes([i for i in range(33)]) + b"\x7F"
    encoded, encode_return_code = run_encode(control_chars)
    
    if encode_return_code == 0:
        decoded, decode_return_code = run_decode(encoded)
        
        if decode_return_code == 0 and decoded == control_chars:
            print("Success: Control characters encoding/decoding successful")
            success += 1
        else:
            print("Error: Data mismatch when encoding/decoding control characters")
    
    print(f"\nTotal: {success}/{total_tests} tests passed\n")
    return success == total_tests

def test_partial_groups():
    print("\n=== Partial groups test ===")
    success = 0
    total_tests = 3
    
    for length in range(1, 4):
        test_data = b"a" * length
        encoded, encode_return_code = run_encode(test_data)
        
        if encode_return_code != 0:
            print(f"Error: Encoder returned non-zero code when encoding {length} bytes")
            continue
            
        decoded, decode_return_code = run_decode(encoded)
        
        if decode_return_code != 0:
            print(f"Error: Decoder returned non-zero code when decoding partial group")
            continue
            
        if decoded == test_data:
            print(f"Success: Partial group encoding/decoding successful ({length} bytes)")
            success += 1
        else:
            print(f"Error: Data mismatch when encoding/decoding partial group")
    
    print(f"\nTotal: {success}/{total_tests} tests passed\n")
    return success == total_tests

def test_invalid_inputs():
    print("\n=== Invalid inputs test ===")
    
    invalid_inputs = [
        b"v", 
        b"!!!!!", 
        b"z!", 
        b"!!z!!", 
        b"z\x80", 
        b"!!!\x80!!"
    ]
    
    success = 0
    total_tests = len(invalid_inputs)
    
    for i, invalid_input in enumerate(invalid_inputs):
        _, return_code = run_decode(invalid_input)
        
        if return_code != 0:
            print(f"Success: Test {i+1}: Decoder correctly rejected invalid data")
            success += 1
        else:
            print(f"Error: Test {i+1}: Decoder incorrectly processed invalid data")
    
    print(f"\nTotal: {success}/{total_tests} tests passed\n")
    return success == total_tests

def test_ascii85_vs_base64():
    print("\n=== ASCII85 vs Base64 comparison ===")
    
    test_sizes = [10, 100, 1000]
    
    for size in test_sizes:
        random_bytes = generate_random_bytes(size)
        
        ascii85_encoded, _ = run_encode(random_bytes)
        base64_encoded = base64.b64encode(random_bytes)
        
        print(f"Size: {size} bytes")
        print(f"ASCII85 length: {len(ascii85_encoded)}")
        print(f"Base64 length: {len(base64_encoded)}")
        
        ascii85_decoded, _ = run_decode(ascii85_encoded)
        base64_decoded = base64.b64decode(base64_encoded)
        
        if ascii85_decoded == random_bytes and base64_decoded == random_bytes:
            print(f"Success: Both encodings correctly processed {size} bytes")
        else:
            print(f"Error: Results mismatch for {size} bytes")
            return False
    
    print("\nAll comparison tests passed")
    return True

def test_performance():
    print("\n=== Performance test ===")
    
    size = 100000
    iterations = 3
    
    random_bytes = generate_random_bytes(size)
    
    print(f"Testing with {size} bytes, {iterations} iterations")
    
    ascii85_encode_time = 0
    for _ in range(iterations):
        start = time.time()
        ascii85_encoded, _ = run_encode(random_bytes)
        ascii85_encode_time += (time.time() - start) * 1000
    ascii85_encode_time /= iterations
    
    base64_encode_time = 0
    for _ in range(iterations):
        start = time.time()
        base64_encoded = base64.b64encode(random_bytes)
        base64_encode_time += (time.time() - start) * 1000
    base64_encode_time /= iterations
    
    print(f"ASCII85 encoding: {ascii85_encode_time:.2f} ms")
    print(f"Base64 encoding: {base64_encode_time:.2f} ms")
    
    print("\nPerformance test completed")
    return True

def main():
    if not os.path.exists("../bin/main"):
        print("Error: Executable file '../bin/main' not found. Compile the project before running tests.")
        sys.exit(1)
    
    all_passed = True
    
    if not test_encode_decode():
        all_passed = False
    
    if not test_empty_input():
        all_passed = False
    
    if not test_special_bytes():
        all_passed = False
    
    if not test_partial_groups():
        all_passed = False
    
    if not test_invalid_inputs():
        all_passed = False
    
    if not test_ascii85_vs_base64():
        all_passed = False
    
    if not test_performance():
        all_passed = False
    
    if all_passed:
        print("\n=== All tests passed successfully! ===")
        sys.exit(0)
    else:
        print("\n=== Some tests failed! ===")
        sys.exit(1)

if __name__ == "__main__":
    main() 