# M5Dial Quick Start Guide

This guide will help you quickly set up your M5Dial to control Home Assistant using the provided configuration file.

## What You'll Get

A multi-mode controller that can:
- **Mode 1 (Light)**: Control brightness of any light entity
- **Mode 2 (Volume)**: Control volume of any media player
- **Mode 3 (Climate)**: Control temperature of any thermostat/climate entity

### Controls
- **Rotate the dial**: Adjust the current value
- **Press center button**: Switch between modes
- **Touch the screen**:
  - Touch center: Switch modes
  - Touch outer ring: Jump to a specific value

### Visual Feedback
- Circular progress bar shows current value
- Color-coded mode indicator (Yellow=Light, Green=Volume, Orange=Climate)
- RGB LED flashes on rotation
- Mode dots at bottom show which mode you're in
- WiFi status indicator in top-right corner

## Installation Steps

### 1. Prerequisites

- Home Assistant with ESPHome add-on installed
- M5Dial device
- USB-C cable
- Chrome/Edge browser

### 2. Prepare Your Configuration

1. **Download the configuration file**: Get `m5dial-config.yaml`

2. **Edit entity IDs**: Open the file and update the `substitutions` section with your actual Home Assistant entity IDs:

```yaml
substitutions:
  device_name: m5dial-controller
  friendly_name: M5Dial Controller

  # Replace these with your actual entity IDs
  light_entity: "light.living_room"              # Change this
  media_player_entity: "media_player.living_room_speaker"  # Change this
  climate_entity: "climate.living_room"          # Change this
```

**To find your entity IDs:**
- Go to Home Assistant → Developer Tools → States
- Find your devices and copy their entity IDs (e.g., `light.bedroom_lamp`)

3. **Set up secrets**: Create or edit your ESPHome `secrets.yaml` file:

```yaml
# WiFi credentials (must be 2.4 GHz)
wifi_ssid: "YourNetworkName"
wifi_password: "YourPassword"

# Generate encryption key: openssl rand -base64 32
api_encryption_key: "YOUR_GENERATED_KEY_HERE"

# Choose a password for OTA updates
ota_password: "your-ota-password"
```

### 3. Flash the M5Dial

**Option A: Using ESPHome Dashboard (Recommended)**

1. Open ESPHome dashboard in Home Assistant
2. Click **+ New Device**
3. Click **Skip** on the wizard
4. Give it a name (e.g., "m5dial-controller")
5. Click **Edit** on the new device
6. Delete all content and paste the `m5dial-config.yaml` content
7. Click **Save**
8. Click **Install** → **Plug into this computer**
9. Connect M5Dial via USB-C
10. Select the USB port in the browser dialog
11. Wait for installation to complete

**Option B: Using ESPHome Command Line**

```bash
esphome run m5dial-config.yaml
```

### 4. First Boot

1. After flashing, the M5Dial will:
   - Show a rainbow LED animation
   - Connect to your WiFi
   - Appear in Home Assistant as a new ESPHome device

2. Go to Home Assistant → Settings → Devices & Services
3. You should see "M5Dial Controller" discovered
4. Click **Configure** and follow the prompts

## WiFi Configuration Directly from M5Dial

The M5Dial has built-in WiFi configuration capabilities! You can change WiFi networks without reflashing.

### Method 1: Long Press Button

1. **Press and hold** the center button for **3 seconds**
2. The LED will pulse blue
3. Display shows "WiFi Setup" screen with instructions
4. M5Dial creates a WiFi hotspot: **"M5Dial Setup"** (password: `m5dial123`)
5. Connect your phone/computer to this network
6. A captive portal should open automatically (or go to `192.168.4.1`)
7. Select your WiFi network and enter the password
8. M5Dial will reconnect and save the new credentials
9. Press button or touch screen to exit setup mode

### Method 2: Touch the WiFi Indicator

1. **Touch the bottom area** of the display (where the WiFi indicator is)
2. WiFi setup mode activates
3. Follow steps 4-9 from Method 1 above

### Method 3: From Home Assistant

1. Go to your M5Dial device in Home Assistant
2. Find the button entity: **"Enter WiFi Setup Mode"**
3. Press the button
4. M5Dial enters WiFi setup mode
5. Follow steps 4-9 from Method 1 above

### Method 4: Improv Serial (USB)

If WiFi is completely broken or you can't access the fallback AP:

1. Connect M5Dial to your computer via USB-C
2. Open a browser and go to https://www.improv-wifi.com/
3. Click **Connect Device**
4. Select the M5Dial USB port
5. Follow the on-screen prompts to configure WiFi
6. No reflashing needed!

### WiFi Setup Mode Indicators

When in WiFi setup mode:
- **LED**: Pulsing blue
- **Display**: Shows "WiFi Setup" with instructions
- **WiFi Icon**: Flashing at bottom of screen
- **Fallback AP**: "M5Dial Setup" is broadcasting

### 5. Test It Out

1. **Test Mode Switching**: Press the center button to cycle through modes
   - You should see: LIGHT → VOLUME → CLIMATE → LIGHT...
   - LED flashes white on mode change
   - Mode dots at bottom indicate current mode

2. **Test Rotation**: Turn the dial
   - Value should increase/decrease
   - LED flashes green (clockwise) or orange (counter-clockwise)
   - Progress circle updates

3. **Test Touch**: Touch the outer ring of the display
   - Value should jump to the touched position

## Customization

### Change the Controlled Entities

Edit the `substitutions` section:

```yaml
substitutions:
  light_entity: "light.bedroom"
  media_player_entity: "media_player.kitchen_speaker"
  climate_entity: "climate.main_floor"
```

### Adjust Temperature Range

Edit the climate number component:

```yaml
number:
  - platform: template
    name: "Thermostat Temperature"
    id: thermostat_temp
    min_value: 60  # Change to 60°F
    max_value: 80  # Change to 80°F
    step: 1        # Change to 1 degree steps
```

### Change LED Brightness

In the encoder `on_clockwise` and `on_anticlockwise` sections:

```yaml
brightness: 30%  # Change this (0-100%)
```

### Disable Touch Screen

If you don't want touch controls, comment out the touchscreen section:

```yaml
# touchscreen:
#   - platform: ft63x6
#     id: my_touchscreen
#     ...
```

### Add More Modes

You can add a 4th mode (e.g., fan speed) by:

1. Adding a new number component
2. Updating the mode cycle: `id(control_mode) = (id(control_mode) + 1) % 4;`
3. Adding the mode case in the display lambda
4. Adding another mode indicator dot

## Troubleshooting

### Device won't connect to WiFi
- Ensure you're using a 2.4 GHz network (not 5 GHz)
- Check the fallback hotspot: "M5Dial Controller Fallback" (password: m5dial123)
- Connect to it and reconfigure WiFi

### Display is blank
- Check if the device powered on (LED should flash on boot)
- Try pressing the center button
- Re-flash the firmware

### Encoder doesn't respond
- Values should still change in Home Assistant
- Check the logs in ESPHome dashboard
- Verify pin numbers are correct for your M5Dial model

### Touch screen not working
- Ensure I2C pins are correct (GPIO11, GPIO12)
- Check interrupt pin (GPIO9)
- Look for errors in ESPHome logs

### Changes don't apply to Home Assistant
- Make sure the entity IDs are correct
- Check that devices are available in Home Assistant
- Look at ESPHome logs for service call errors

## Advanced Features

### Home Assistant Automations

You can create automations based on the M5Dial's sensors:

```yaml
automation:
  - alias: "M5Dial Mode Changed"
    trigger:
      - platform: state
        entity_id: sensor.dial_encoder
    action:
      - service: notify.mobile_app
        data:
          message: "M5Dial adjusted to {{ states('sensor.dial_encoder') }}"
```

### Multiple M5Dials

To set up multiple M5Dials:

1. Copy the config file
2. Change the `device_name` substitution to something unique
3. Configure different entities for each dial
4. Flash each device with its own config

Example:
- M5Dial 1: Living room controls
- M5Dial 2: Bedroom controls
- M5Dial 3: Kitchen controls

## Updates

To update the firmware wirelessly (OTA):

1. Open ESPHome dashboard
2. Find your M5Dial device
3. Click **Install** → **Wirelessly**
4. Wait for update to complete

## Support

- [ESPHome Documentation](https://esphome.io)
- [Home Assistant Community](https://community.home-assistant.io)
- [M5Stack M5Dial Docs](https://docs.m5stack.com/en/core/M5Dial)

## Tips

1. **Keep it charged**: The M5Dial needs constant USB power
2. **Strong WiFi**: Place within good WiFi range for reliable control
3. **Responsive control**: Adjust `update_interval` in display config for smoother or faster updates
4. **Battery backup**: Consider a USB power bank for portable use
5. **3D printed case**: Many community designs available for desk mounting

Enjoy your M5Dial controller!
