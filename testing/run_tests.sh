#!/bin/bash

# SAGE API Test Runner
# Run all example tests against the API

API_URL="${API_URL:-http://localhost:8000}"
EXAMPLES_DIR="$(dirname "$0")/examples"

echo "=========================================="
echo "SAGE API Test Runner"
echo "API URL: $API_URL"
echo "=========================================="
echo ""

for input_file in "$EXAMPLES_DIR"/*_input.json; do
    test_name=$(basename "$input_file" _input.json)
    output_file="${EXAMPLES_DIR}/${test_name}_output.json"

    echo "Running: $test_name"
    echo "-------------------------------------------"

    result=$(cat "$input_file" | curl -s -X POST "$API_URL/test-concept" \
        -H "Content-Type: application/json" \
        -d @-)

    # Save output
    echo "$result" | python3 -m json.tool > "$output_file" 2>/dev/null

    # Extract key metrics
    passed=$(echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print('PASS ✓' if d['result']['passed'] else 'FAIL ✗')" 2>/dev/null)
    score=$(echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"{d['result']['composite_score']:.3f}\")" 2>/dev/null)
    threshold=$(echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"{d['result']['threshold']:.2f}\")" 2>/dev/null)
    personas=$(echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"{d['personas_matched']}/{d['personas_total']}\")" 2>/dev/null)

    echo "  Result: $passed"
    echo "  Score: $score (threshold: $threshold)"
    echo "  Personas: $personas matched"
    echo "  Output saved to: $output_file"
    echo ""
done

echo "=========================================="
echo "All tests completed!"
echo "=========================================="
