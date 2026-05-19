#!/bin/bash

# Directory containing test files
TEST_DIR="slitherlink-boards-public"

# Script to test
SCRIPT="slitherlink.py"

passed=0
failed=0

for input_file in "$TEST_DIR"/test*.txt; do
    # Extract test number (e.g. test01)
    test_name=$(basename "$input_file" .txt)

    expected_output="$TEST_DIR/$test_name.out"

    echo "Running $test_name..."

    # Run test and capture output
    actual_output=$(python3 "$SCRIPT" < "$input_file")

    # Read expected output
    expected=$(cat "$expected_output")

    # Compare outputs
    if diff <(echo "$actual_output") <(echo "$expected") > /dev/null; then
        echo "✅ $test_name PASSED"
        ((passed++))
    else
        echo "❌ $test_name FAILED"
        echo "Expected:"
        echo "$expected"
        echo
        echo "Got:"
        echo "$actual_output"
        ((failed++))
    fi

    echo "-----------------------------"
done

echo "Finished."
echo "Passed: $passed"
echo "Failed: $failed"