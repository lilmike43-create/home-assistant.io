#!/bin/bash
# M5Dial Pre-Deployment Validation Script
# Run this before flashing your M5Dial to catch configuration errors

cd "$(dirname "$0")"

echo "Running M5Dial configuration validation..."
echo ""

python3 validate-m5dial.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "To flash your M5Dial, run:"
    echo "  esphome run m5dial-config.yaml"
else
    echo "Fix the issues above before flashing."
fi

exit $exit_code
