# M5Dial Enhanced Multi-Device Controller

**Transform your M5Dial into a powerful Home Assistant controller with 6-device support, RGB color picker, and a beautiful curved text UI.**

<img src="https://img.shields.io/badge/ESPHome-000000?style=for-the-badge&logo=esphome&logoColor=white" alt="ESPHome"/> <img src="https://img.shields.io/badge/Home_Assistant-41BDF5?style=for-the-badge&logo=home-assistant&logoColor=white" alt="Home Assistant"/> <img src="https://img.shields.io/badge/ESP32--S3-000000?style=for-the-badge&logo=espressif&logoColor=white" alt="ESP32-S3"/>

---

## ✨ Features

### Multi-Device Control
- 🔆 **4 RGB Lights** - Full brightness + color control
- 🌡️ **1 Climate/Thermostat** - Temperature adjustment
- 🔌 **1 Switch** - Quick toggle (coffee maker, fan, etc.)

### Beautiful Interface
- 🎨 **Curved Text** - Follows circular screen contour
- 📊 **Visual Feedback** - Devices glow orange when ON
- 🎯 **Large Display** - Easy-to-read percentages and values
- 🌈 **Live Preview** - See colors before applying

### Smart Features
- ✅ **Pre-Deployment Validation** - Catch errors before flashing
- 🔄 **OTA Updates** - Update wirelessly
- 💾 **Persistent Settings** - Remembers selected device
- 🎮 **Intuitive Controls** - Dial + button + touchscreen

---

## 📚 Documentation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[Enhanced Guide](M5DIAL-ENHANCED-GUIDE.md)** | Complete setup & usage guide | First-time setup, learning features |
| **[Quick Reference](M5DIAL-QUICK-REFERENCE.md)** | One-page cheat sheet | Daily use, quick lookups |
| **[Troubleshooting](M5DIAL-TROUBLESHOOTING.md)** | Problem solving guide | When things don't work |
| **[Validation README](VALIDATION-README.md)** | Testing & validation docs | Before flashing changes |

---

## 🚀 Quick Start

### 1. Download & Configure

```bash
# Navigate to voice_control directory
cd source/voice_control

# Edit configuration
vim m5dial-config.yaml
```

**Update lines 25-38** with your entities:
```yaml
# Home Assistant Entities
light_1: "light.desk_lamp"        # ← Change to YOUR entities
light_2: "light.bedroom"
light_3: "light.kitchen"
light_4: "light.living_room"
climate_entity: "climate.living_room"
switch_1: "switch.coffee_maker"

# Display Names (SHORT! 4-5 chars max)
light_1_name: "Desk"               # ← Change to match your names
light_2_name: "Bed"
light_3_name: "Kit"
light_4_name: "Live"
climate_name: "Clim"
switch_1_name: "Coff"
```

### 2. Validate

```bash
./validate.sh
```

Should show:
```
✓ All 7 checks passed! Configuration is ready for deployment.
✓ READY TO FLASH
```

### 3. Flash

**Via ESPHome Dashboard:**
1. Open ESPHome in Home Assistant
2. Create/edit device
3. Paste validated config
4. Install → Plug into computer
5. Connect M5Dial via USB
6. Wait for completion

**Via Command Line:**
```bash
esphome run m5dial-config.yaml
```

### 4. Test

1. ✅ Turn dial → See device selection (1-6)
2. ✅ Press button → Enter control mode
3. ✅ Turn dial → Adjust brightness
4. ✅ Tap "COLOR" → RGB color picker
5. ✅ Tap "APPLY" → Color changes
6. ✅ Press button → Return home

---

## 📖 Usage Examples

### Example 1: Dim Bedroom Light

```
1. Turn dial → Select device 2 (Bed)
2. Press button → Enter brightness mode
3. Turn left → Brightness decreases
4. See arc shrink and percentage drop
5. Press button → Return home
```

### Example 2: Change Kitchen Light to Blue

```
1. Turn dial → Select device 3 (Kit)
2. Press button → Enter brightness mode
3. Tap "COLOR" (top-left) → Color picker opens
4. Turn dial → Set Red to 0
5. Tap bottom → Switch to Green channel
6. Turn dial → Set Green to 0
7. Tap bottom → Switch to Blue channel
8. Turn dial → Set Blue to 255
9. Watch preview turn blue
10. Tap "APPLY" (top-right) → Blue light!
```

### Example 3: Toggle Coffee Maker

```
1. Turn dial → Select device 6 (Coff)
2. Press button → Switch toggles ON/OFF
3. Circle fills orange when ON
```

---

## 🎨 Screen Layouts

### Home Page
```
     ╔═══════════════════════════════╗
     ║ S E L E C T   D E V I C E     ║  ← Curved
     ║                               ║
     ║   (Desk)          (Coff)      ║
     ║     ◉               ○         ║
     ║         ╭─────╮               ║
     ║         │  1  │               ║  ← Selected
     ║         ╰─────╯               ║
     ║   (Bed)           (Clim)      ║
     ║     ●               ○         ║
     ║                               ║
     ║ Turn-select  Press-control    ║  ← Curved
     ╚═══════════════════════════════╝

Legend: ○ OFF  ● ON  ◉ Selected
```

---

## 🔧 Customization

### Change Number of Devices

Edit device cycling logic (line ~240):
```yaml
id(selected_device) = (id(selected_device) % 6) + 1;
                                           ↑
                              Change to 3, 4, 5, etc.
```

### Adjust Brightness Steps

```yaml
# Change from 10% to 5% steps
brightness_step_pct: '5'    # Was '10'
brightness_step_pct: '-5'   # Was '-10'
```

### Customize Colors

```yaml
substitutions:
  primary_color: 'FF8C00'     # Orange → Change to any hex color
  accent_color: '00D9FF'      # Cyan
  background_color: '000000'  # Black
```

---

## ✅ Pre-Deployment Validation

**Why Validate?**
- Catches 95% of errors before compilation
- Saves 2-3 minutes per fix
- Prevents broken deployments

**7 Automated Checks:**
1. ✅ YAML syntax
2. ✅ Entity/display name consistency
3. ✅ Brightness format (string vs integer)
4. ✅ Page switching logic
5. ✅ Curved text implementation
6. ✅ Color apply button logic
7. ✅ ESPHome validation

**Run Before Every Flash:**
```bash
./validate.sh
```

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Won't compile** | Run `./validate.sh` → Fix errors shown |
| **Button does nothing** | Missing `show_page()` calls (validation checks this) |
| **Brightness doesn't change** | Light must be ON, check entity ID, verify supports brightness |
| **Color doesn't apply** | Light must support RGB, brightness >20% |
| **Display names don't match** | Update entity ID **AND** display name, reflash |
| **Device states wrong** | Check sensor entity IDs, verify Home Assistant connection |

**Full troubleshooting**: See [M5DIAL-TROUBLESHOOTING.md](M5DIAL-TROUBLESHOOTING.md)

---

## 📊 Configuration Reference

### File Structure
```
source/voice_control/
├── m5dial-config.yaml              ← Main config (36KB)
│   ├── Lines 11-39: Substitutions (YOUR entities here!)
│   ├── Lines 160-199: Globals (device state)
│   ├── Lines 228-373: Rotary encoder logic
│   ├── Lines 461-625: Button & touchscreen
│   └── Lines 706-1010: Display rendering
│
├── validate-m5dial.py              ← Validation script
├── validate.sh                     ← Quick validation wrapper
│
├── M5DIAL-README.md                ← This file
├── M5DIAL-ENHANCED-GUIDE.md        ← Complete guide
├── M5DIAL-QUICK-REFERENCE.md       ← One-page reference
├── M5DIAL-TROUBLESHOOTING.md       ← Problem solving
└── VALIDATION-README.md            ← Validation docs
```

### Key Sections

| Lines | Section | Edit To... |
|-------|---------|------------|
| 11-39 | Substitutions | Change entity IDs & names |
| 33-38 | Display Names | Match your entity names |
| 42-48 | Colors | Customize UI colors |
| 261-288 | Brightness Up | Adjust step size |
| 331-358 | Brightness Down | Adjust step size |

---

## 🎓 Tips & Best Practices

### 1. **Always Validate First**
```bash
./validate.sh  # Catches most errors!
```

### 2. **Keep Display Names Short**
- Maximum 4-5 characters
- Examples: "Desk", "Bed", "Kit", "Live"
- Longer names may overflow on circular screen

### 3. **Test Incrementally**
- Start with 1-2 devices
- Test thoroughly
- Add more devices gradually

### 4. **Monitor Logs**
```bash
esphome logs m5dial-config.yaml
```

### 5. **Backup Working Configs**
```bash
cp m5dial-config.yaml m5dial-backup-$(date +%Y%m%d).yaml
```

### 6. **Use OTA for Updates**
- Faster than USB
- No cable needed
- Update in ~30 seconds

---

## 🔄 Update Process

### Wireless Update (Recommended)
```bash
# 1. Edit configuration
vim m5dial-config.yaml

# 2. Validate
./validate.sh

# 3. Upload wirelessly
# ESPHome Dashboard → Install → Wirelessly
```

### USB Update
```bash
# 1. Edit configuration
vim m5dial-config.yaml

# 2. Validate
./validate.sh

# 3. Flash via USB
esphome run m5dial-config.yaml
```

---

## 📈 Version History

### v2.0 - Enhanced Multi-Device (Current)
- ✨ 6 device support (4 lights, climate, switch)
- ✨ RGB color picker with live preview
- ✨ Curved text UI
- ✨ Visual state indicators
- ✨ Pre-deployment validation
- ✨ Comprehensive documentation

### v1.0 - Original
- Basic 3-mode system
- Single entity per mode
- Simple UI

---

## 🆘 Getting Help

### Before Asking

**Collect this info:**
1. ESPHome logs: `esphome logs m5dial-config.yaml > logs.txt`
2. Validation output: `./validate.sh > validation.txt`
3. Your substitutions section (lines 11-39)
4. Clear description of the problem

### Resources
- 📖 [Enhanced Guide](M5DIAL-ENHANCED-GUIDE.md)
- 🐛 [Troubleshooting Guide](M5DIAL-TROUBLESHOOTING.md)
- 📝 [Quick Reference](M5DIAL-QUICK-REFERENCE.md)
- 🔍 [ESPHome Discord](https://discord.gg/KhAMKrd)
- 💬 [Home Assistant Community](https://community.home-assistant.io)

---

## 🎯 Quick Command Reference

```bash
# Validate before flashing
./validate.sh

# Flash via USB
esphome run m5dial-config.yaml

# Flash wirelessly
esphome upload m5dial-config.yaml --device 192.168.1.XXX

# View live logs
esphome logs m5dial-config.yaml

# Check WiFi configuration
esphome config m5dial-config.yaml
```

---

## 🌟 Features Comparison

| Feature | v1.0 | v2.0 Enhanced |
|---------|------|---------------|
| Devices | 3 | 6 |
| Light Control | Brightness only | Brightness + RGB color |
| UI Design | Basic | Curved text, visual indicators |
| Color Picker | ❌ | ✅ Full RGB with preview |
| Validation | ❌ | ✅ 7 automated checks |
| Documentation | Basic | Complete (4 guides) |
| State Indicators | ❌ | ✅ Visual ON/OFF states |

---

## 💡 Pro Tips

1. **Print the Quick Reference** - Keep it nearby while using M5Dial
2. **Use Git for Configs** - Track changes, easy rollback
3. **Test in Stages** - Add features one at a time
4. **Read the Logs** - They tell you exactly what's wrong
5. **Validate Always** - 30 seconds can save 30 minutes

---

## 📜 License

This configuration is provided as-is for personal and educational use. Modify and adapt as needed for your Home Assistant setup.

---

## 🙏 Credits

Built on ESPHome for the M5Stack M5Dial hardware, designed to work seamlessly with Home Assistant.

---

**Ready to get started? Read the [Enhanced Guide](M5DIAL-ENHANCED-GUIDE.md)! 🚀**
