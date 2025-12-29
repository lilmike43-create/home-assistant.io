# M5Dial Enhanced Multi-Device Controller Guide

**Complete guide for the enhanced M5Dial configuration with 6-device control, RGB color picker, and curved text UI**

---

## 🎯 What You Get

A powerful multi-device controller featuring:

- **6 Controllable Devices**:
  - 4 RGB Lights (with brightness + color control)
  - 1 Climate/Thermostat
  - 1 Switch (coffee maker, fan, etc.)

- **Beautiful Curved UI**:
  - Text follows the natural contour of the circular screen
  - Visual state indicators (devices glow orange when ON)
  - Large, easy-to-read percentages and values

- **Dual Control Modes**:
  - **Brightness Mode**: Adjust light brightness with circular progress arc
  - **Color Picker Mode**: Full RGB color control with live preview

- **Intuitive Navigation**:
  - Turn dial to select devices or adjust values
  - Press button to enter control mode
  - Touch screen for quick access to color picker

---

## 📱 Screen Layout

### Home Page (Device Selection)
```
        ╔═══════════════════════════════╗
        ║   S E L E C T   D E V I C E   ║  ← Curved text
        ║                               ║
        ║      (Desk)         (Coff)    ║  ← Device circles
        ║        1   ╭───╮   6          ║
        ║            │ 1 │              ║  ← Selected device
        ║            ╰───╯              ║
        ║      (Bed)         (Clim)    ║
        ║        2             5        ║
        ║                               ║
        ║      (Kit)         (Live)    ║
        ║        3             4        ║
        ║                               ║
        ║ Turn-select  Press-control    ║  ← Curved text
        ╚═══════════════════════════════╝

Legend:
  ○ = Device OFF (white outline)
  ● = Device ON (orange filled)
  ◉ = Selected device (cyan filled)
```

### Brightness Control Page
```
        ╔═══════════════════════════════╗
        ║  B R I G H T N E S S          ║  ← Curved text
COLOR   ║         Desk                  ║  APPLY
↑ tap   ║                               ║  ↑ tap
        ║      ╭─────────╮              ║
        ║   75%│   75%   │              ║  ← Progress arc
        ║      ╰─────────╯              ║
        ║                               ║
        ║    Turn to adjust             ║  ← Curved text
        ╚═══════════════════════════════╝
```

### Color Picker Page
```
        ╔═══════════════════════════════╗
        ║  C O L O R   P I C K E R      ║  ← Curved text
        ║         RED                   ║  APPLY
        ║                               ║  ↑ tap
        ║      ╭─────────╮              ║
        ║      │ Preview │              ║  ← Live color
        ║      ╰─────────╯              ║
        ║   R 255  G 128  B 64          ║  ← RGB values
        ║  Tap bottom-switch            ║  ← Curved text
        ╚═══════════════════════════════╝
                    ↑ tap to cycle R→G→B
```

---

## 🎮 Controls

### Rotary Dial
- **On Home Page**: Turn to cycle through devices 1→2→3→4→5→6→1
- **In Brightness Mode**: Turn to adjust brightness ±10%
- **In Color Picker**: Turn to adjust current RGB channel ±10

### Center Button
- **On Home Page**: Press to enter control mode for selected device
- **In Control Mode**: Press to return to home page
- **Device 6 (Switch)**: Press to toggle ON/OFF (stays on home page)

### Touchscreen
- **"< Home" (top center)**: Tap to return to device selection
- **"COLOR" (top-left, brightness mode)**: Tap to enter color picker
- **"APPLY" (top-right, color picker)**: Tap to apply color and return
- **Bottom area (color picker)**: Tap to cycle RGB channels (Red→Green→Blue)

---

## 🔧 Installation

### 1. Prerequisites

- ✅ Home Assistant with ESPHome add-on
- ✅ M5Stack M5Dial device
- ✅ USB-C cable
- ✅ Chrome or Edge browser
- ✅ Python 3.6+ (for validation script)

### 2. Configure Your Entities

Open `m5dial-config.yaml` and find the substitutions section (lines 11-39):

```yaml
################################################################################
# ⚠️ CRITICAL: Entities & Display Names Work Together!
################################################################################
# When customizing, you MUST update BOTH sections:
#
# Step 1: Change entity ID below          ↓
# Step 2: Change display name below       ↓
# Step 3: Recompile & upload firmware     ↓
#
# EXAMPLE - To change Device 1 from Desk Lamp to Kitchen:
#   light_1: "light.kitchen"              ← Change this
#   light_1_name: "Kit"                   ← AND change this (4-5 chars max)
################################################################################

# Home Assistant Entities - Change these to YOUR entity IDs
light_1: "light.desk_lamp"              # ← Your entity ID
light_2: "light.bedroom"
light_3: "light.kitchen"
light_4: "light.living_room"
climate_entity: "climate.living_room"
switch_1: "switch.coffee_maker"

# Display Names - Change these to match YOUR entities above (SHORT names!)
light_1_name: "Desk"      # ← Display name (max 4-5 characters)
light_2_name: "Bed"
light_3_name: "Kit"
light_4_name: "Live"
climate_name: "Clim"
switch_1_name: "Coff"
```

**Finding Your Entity IDs:**
1. Go to Home Assistant → Developer Tools → States
2. Search for your devices
3. Copy the entity IDs (e.g., `light.bedroom_lamp`)
4. Update BOTH the entity ID AND display name

### 3. Validate Configuration (Recommended!)

**Before flashing**, run the validation script to catch errors:

```bash
cd source/voice_control
./validate.sh
```

You should see:
```
✓ All 7 checks passed! Configuration is ready for deployment.
✓ READY TO FLASH
```

If validation fails, fix the errors before flashing!

### 4. Flash the M5Dial

**Using ESPHome Dashboard:**
1. Open ESPHome in Home Assistant
2. Create new device or edit existing
3. Paste the validated `m5dial-config.yaml` content
4. Click **Save** → **Install** → **Plug into this computer**
5. Connect M5Dial via USB-C
6. Select the USB port when prompted
7. Wait for installation to complete (~2-3 minutes)

**Using Command Line:**
```bash
esphome run m5dial-config.yaml
```

### 5. First Boot

After flashing:
1. M5Dial connects to WiFi
2. Home page appears with device selection
3. Device appears in Home Assistant as "M5Dial Controller"
4. Turn dial to see device selection working
5. Press button to test control mode

---

## 💡 How to Use

### Controlling Lights (Devices 1-4)

**Adjust Brightness:**
1. Turn dial to select light (1-4)
2. Press button to enter brightness mode
3. Turn dial clockwise to brighten (+10%)
4. Turn dial counter-clockwise to dim (-10%)
5. Watch the circular progress arc update
6. Press button to return home

**Change Color:**
1. Enter brightness mode (see above)
2. Tap "COLOR" in top-left corner
3. Color picker opens showing live preview
4. Turn dial to adjust current channel (Red shown first)
5. Tap bottom of screen to switch channel (Red→Green→Blue)
6. Watch the preview circle update in real-time
7. Tap "APPLY" to set the color
8. Returns to brightness mode

### Controlling Climate (Device 5)

1. Turn dial to select device 5 (Clim)
2. Press button to enter climate mode
3. Turn dial to adjust temperature
4. Display shows current temperature
5. Press button to return home

### Controlling Switch (Device 6)

1. Turn dial to select device 6 (Coff)
2. Press button to toggle ON/OFF
3. Device circle fills orange when ON
4. Stays on home page (no separate control screen)

---

## 🎨 Visual Indicators

### Device States (Home Page)
- **White outline ○**: Device is OFF
- **Orange filled ●**: Device is ON
- **Cyan filled ◉**: Currently selected device

### Control Pages
- **Circular arc**: Shows current value (brightness, temperature, color channel)
- **Large number**: Percentage or value in center
- **Curved text**: Follows natural screen contour for better readability
- **Color preview**: Live color preview in color picker mode

---

## 🔧 Customization

### Change Device Count

Want only 3 lights instead of 4? Edit the encoder logic:

```yaml
# In rotary_encoder on_clockwise section (line ~240)
id(selected_device) = (id(selected_device) % 6) + 1;
                                           ↑
                                     Change to 3, 4, 5, etc.
```

Also update the home page display to remove unused devices.

### Adjust Brightness Step Size

Change from 10% to 5% steps:

```yaml
# Lines 261, 270, 279, 288
brightness_step_pct: '10'   ← Change to '5'
brightness_step_pct: '-10'  ← Change to '-5'
```

### Customize Colors

```yaml
substitutions:
  background_color: '000000'  # Black
  primary_color: 'FF8C00'     # Orange
  secondary_color: 'FFFFFF'   # White
  accent_color: '00D9FF'      # Cyan ← Change these!
```

### Disable Color Picker

If you only need brightness control, comment out:
```yaml
# Lines 518-531: Color Mode Button
# Lines 533-607: Apply Color Button
# Lines 930-999: Color picker display
```

---

## 🐛 Troubleshooting

### Compilation Fails

**Error: "Must be string, got <class 'esphome.helpers.EInt'>"**
- **Fix**: Run `./validate.sh` to check brightness_step_pct values
- They must be strings: `'10'` not `10`

**Error: "Unknown entity ID"**
- **Fix**: Verify entity IDs in Home Assistant Developer Tools → States
- Make sure entities exist and are spelled correctly

### Button Does Nothing

**Symptoms**: Pressing button plays sound but screen doesn't change
- **Fix**: Check logs for page switching errors
- Validation script checks for this (Step 4)

### Brightness Doesn't Change

**Symptoms**: Turn dial but light brightness doesn't change
- **Check**: Is the light ON in Home Assistant?
- **Check**: Does the entity support brightness?
- **Check**: Look at ESPHome logs for service call errors

### Color Doesn't Apply

**Symptoms**: Set color but light doesn't change color
- **Check**: Does your light support RGB color?
- **Check**: Is brightness above 0? (some lights won't show color if dim)
- **Check**: ESPHome logs for "rgb_color" service call errors

### Display Names Don't Update

**Symptoms**: Changed entity names but display still shows old names
- **Fix**: You must update BOTH entity ID AND display name
- **Fix**: After changing, recompile and upload firmware
- Display names are compiled into firmware, not live

### Devices Show Wrong State

**Symptoms**: Light is ON but shows as OFF on home page
- **Fix**: Check sensor entity IDs (light_1_state, etc.)
- **Fix**: Verify Home Assistant can read device states
- **Fix**: Check ESPHome logs for sensor update errors

---

## 📊 Advanced Features

### Pre-Deployment Validation

Always run validation before flashing:

```bash
./validate.sh
```

**What it checks:**
1. ✅ YAML syntax errors
2. ✅ Entity/display name consistency
3. ✅ Brightness control format
4. ✅ Page switching logic
5. ✅ Curved text implementation
6. ✅ Color apply button logic
7. ✅ ESPHome configuration validation

### Git Pre-Commit Hook

Automatically validate before commits:

```bash
# Create .git/hooks/pre-commit
#!/bin/bash
cd source/voice_control && ./validate.sh || exit 1
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Over-The-Air Updates

After initial USB flash, update wirelessly:

1. Edit `m5dial-config.yaml`
2. Run `./validate.sh` to check for errors
3. In ESPHome dashboard: **Install** → **Wirelessly**
4. M5Dial updates without USB cable
5. Takes ~30 seconds

---

## 📚 Configuration Reference

### Key Files

```
source/voice_control/
├── m5dial-config.yaml           ← Main configuration (36KB)
├── validate-m5dial.py           ← Validation script
├── validate.sh                  ← Wrapper script
├── VALIDATION-README.md         ← Validation documentation
└── M5DIAL-ENHANCED-GUIDE.md     ← This file
```

### Important Sections

| Section | Lines | Purpose |
|---------|-------|---------|
| Substitutions | 11-39 | Entity IDs and display names |
| Globals | 160-199 | Device selection and RGB state |
| Rotary Encoder | 228-373 | Dial rotation handlers |
| Button | 461-501 | Center button press logic |
| Touchscreen | 503-625 | Touch controls |
| Display Pages | 706-1010 | UI rendering |

### Entity Sensors

The configuration creates these sensors in Home Assistant:

**For each light (1-4):**
- `sensor.light_X_brightness` - Current brightness (0-255)
- `sensor.light_X_state` - ON/OFF state

**Other sensors:**
- `sensor.climate_state` - Climate entity state
- `sensor.climate_temperature` - Current climate temperature
- `sensor.switch_1_state` - Switch ON/OFF state

---

## 🎓 Tips & Best Practices

### 1. Start Small
- Configure just 1-2 devices initially
- Test thoroughly before adding more
- Easier to debug with fewer devices

### 2. Choose Short Names
- Display names should be 4-5 characters max
- Examples: "Desk", "Bed", "Kit", "Live"
- Longer names may overflow on circular screen

### 3. Use Validation
- Always run `./validate.sh` before flashing
- Catches 95% of common errors
- Saves compilation time

### 4. Test Each Feature
- ✓ Device selection (turn dial)
- ✓ Brightness control (turn in control mode)
- ✓ Color picker (tap COLOR button)
- ✓ Return home (press button or tap Home)
- ✓ Switch toggle (device 6)

### 5. Monitor Logs
- Watch ESPHome logs during first use
- Look for service call errors
- Verify entity IDs are correct

### 6. Keep Firmware Updated
- Use OTA updates for bug fixes
- Test new features on one device first
- Keep backups of working configurations

---

## 🔗 Related Resources

- [Validation README](VALIDATION-README.md) - Complete validation documentation
- [ESPHome Documentation](https://esphome.io) - Official ESPHome docs
- [M5Stack M5Dial](https://docs.m5stack.com/en/core/M5Dial) - Hardware documentation
- [Home Assistant ESPHome Integration](https://www.home-assistant.io/integrations/esphome/)

---

## 📝 Changelog

### Version 2.0 (Enhanced Multi-Device)

**New Features:**
- ✨ 6 device support (4 lights, climate, switch)
- ✨ RGB color picker with live preview
- ✨ Curved text following circular screen contour
- ✨ Visual state indicators (orange = ON)
- ✨ Per-device brightness control
- ✨ Touch-based color mode access

**Improvements:**
- 🎨 Beautiful circular UI design
- 🎨 Larger, more readable text
- 🎨 Intuitive navigation flow
- 🎨 Real-time visual feedback

**Developer Experience:**
- 🔧 Pre-deployment validation system
- 🔧 Comprehensive error checking
- 🔧 Clear configuration warnings
- 🔧 Automated testing before flash

### Version 1.0 (Original)
- Basic 3-mode system (light/media/climate)
- Single entity per mode
- Basic UI

---

## 🎉 You're Ready!

Your M5Dial is now a powerful multi-device controller with:
- ✅ 6 controllable devices
- ✅ Full RGB color control
- ✅ Beautiful curved text UI
- ✅ Visual state indicators
- ✅ Automated validation

Enjoy your enhanced M5Dial controller! 🚀
