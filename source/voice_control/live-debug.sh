#!/bin/bash
# M5Dial Live Debugging Tool

echo "=========================================="
echo "M5Dial Live Debug - Check what's happening"
echo "=========================================="
echo ""

echo "This will show LIVE output from your M5Dial."
echo "Perform these actions on your M5Dial:"
echo ""
echo "1. Turn the dial (you should see 'Rotary' messages)"
echo "2. Press the button (you should see 'Front Button' messages)"
echo "3. Try to adjust brightness (look for 'light.turn_on' calls)"
echo ""
echo "Press Ctrl+C to stop"
echo ""
echo "Starting in 3 seconds..."
sleep 3

echo "=========================================="
echo "LIVE LOG OUTPUT:"
echo "=========================================="

# Show live logs with filtering
esphome logs m5dial-config.yaml 2>&1 | grep --line-buffered -E "(Rotary|Button|light\.|brightness|control_mode|selected_device|Service|ERROR|WARNING)"
