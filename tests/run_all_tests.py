#!/usr/bin/env python3
import subprocess
import sys
import os

# Проверка наличия исполняемого файла
if not os.path.exists("../bin/main"):
    print("ERROR: Executable file '../bin/main' not found. Compile the project before running tests.")
    sys.exit(1)

# Список тестовых файлов
TEST_FILES = [
    "simple_test.py"
]

def make_executable(file_path):
    """Делает файл исполняемым"""
    mode = os.stat(file_path).st_mode
    os.chmod(file_path, mode | 0o111)

def run_test(test_file):
    """Запускает тест и возвращает результат"""
    print(f"\n{'='*80}")
    print(f"Running test: {test_file}")
    print(f"{'='*80}\n")
    
    # Делаем файл исполняемым, если он еще не исполняемый
    make_executable(test_file)
    
    # Запускаем тест
    process = subprocess.run([f"./{test_file}"], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            text=True)
    
    # Выводим результат
    print(process.stdout)
    if process.stderr:
        print("STDERR:")
        print(process.stderr)
    
    return process.returncode == 0

def main():
    # Переходим в директорию с тестами
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    success_count = 0
    failed_tests = []
    
    for test_file in TEST_FILES:
        if os.path.exists(test_file):
            if run_test(test_file):
                success_count += 1
            else:
                failed_tests.append(test_file)
        else:
            print(f"SKIP: Test file {test_file} not found")
    
    # Выводим итоговый результат
    print(f"\n{'='*80}")
    print(f"FINAL RESULT: {success_count}/{len(TEST_FILES)} tests passed successfully")
    
    if failed_tests:
        print("\nFAILED TESTS:")
        for test in failed_tests:
            print(f"  - {test}")
        sys.exit(1)
    else:
        print("\nAll tests passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main() 