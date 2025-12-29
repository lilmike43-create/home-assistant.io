#!/bin/bash
# M5Dial Light Control Debugging Script

echo "==================================================================="
echo "M5Dial Light Control Debugging"
echo "==================================================================="
echo ""

echo "Step 1: Checking entity IDs in configuration..."
echo "-------------------------------------------------------------------"
grep -A 6 "# Home Assistant Entities" /home/user/home-assistant.io/source/voice_control/m5dial-config.yaml | grep "light_"
echo ""

echo "Step 2: Checking brightness control service calls..."
echo "-------------------------------------------------------------------"
grep -B 2 -A 4 "brightness_step_pct" /home/user/home-assistant.io/source/voice_control/m5dial-config.yaml | head -40
echo ""

echo "Step 3: Checking control_mode logic..."
echo "-------------------------------------------------------------------"
grep -A 3 "Mode 1: Brightness control" /home/user/home-assistant.io/source/voice_control/m5dial-config.yaml
echo ""

echo "==================================================================="
echo "NEXT STEPS - Run these commands:"
echo "==================================================================="
echo ""
echo "1. Check if M5Dial is connected:"
echo "   esphome logs m5dial-config.yaml | grep -i 'connected'"
echo ""
echo "2. Monitor brightness commands in real-time:"
echo "   esphome logs m5dial-config.yaml | grep -i 'brightness'"
echo ""
echo "3. Watch for service call errors:"
echo "   esphome logs m5dial-config.yaml | grep -i 'error'"
echo ""
echo "4. Test a specific light in Home Assistant Developer Tools:"
echo "   Service: light.turn_on"
echo "   Entity: (your light entity from Step 1)"
echo "   Data: { \"brightness_step_pct\": 10 }"
echo ""
echo "5. Verify light is actually ON before adjusting brightness"
echo ""
