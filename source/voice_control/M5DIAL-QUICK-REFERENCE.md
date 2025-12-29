# M5Dial Quick Reference Card

**Print this for quick reference while using your M5Dial!**

---

## 🎮 Controls At-A-Glance

| Action | What It Does |
|--------|-------------|
| **Turn Dial** (Home) | Cycle through devices 1→2→3→4→5→6 |
| **Turn Dial** (Brightness) | Adjust brightness ±10% |
| **Turn Dial** (Color) | Adjust current RGB channel ±10 |
| **Press Button** (Home) | Enter control mode for selected device |
| **Press Button** (Control) | Return to home page |
| **Press Button** (Device 6) | Toggle switch ON/OFF |
| **Tap "< Home"** | Return to device selection |
| **Tap "COLOR"** | Enter color picker |
| **Tap "APPLY"** | Apply color & return |
| **Tap Bottom** (Color mode) | Switch RGB channel (R→G→B) |

---

## 📱 Screen Indicators

| Symbol | Meaning |
|--------|---------|
| **○** White outline | Device is OFF |
| **●** Orange filled | Device is ON |
| **◉** Cyan filled | Currently selected |
| **Curved arc** | Current value (brightness/temp/color) |
| **Large number** | Percentage or value |

---

## 🔧 Devices

| # | Type | Controls |
|---|------|----------|
| **1** | Light | Brightness + RGB Color |
| **2** | Light | Brightness + RGB Color |
| **3** | Light | Brightness + RGB Color |
| **4** | Light | Brightness + RGB Color |
| **5** | Climate | Temperature |
| **6** | Switch | ON/OFF Toggle |

---

## 🎨 Color Picker Flow

```
Brightness Mode
       ↓ Tap "COLOR"
  Color Picker
  ├─ Turn dial to adjust current channel
  ├─ Tap bottom to switch R→G→B
  └─ Tap "APPLY" to save
       ↓
  Back to Brightness Mode
```

---

## ⚡ Quick Workflow

### Adjust Light Brightness
1. Turn dial → Select light (1-4)
2. Press button → Enter brightness mode
3. Turn dial → Adjust ±10%
4. Press button → Return home

### Change Light Color
1. Enter brightness mode (see above)
2. Tap "COLOR" (top-left)
3. Turn dial → Adjust Red value
4. Tap bottom → Switch to Green
5. Turn dial → Adjust Green value
6. Tap bottom → Switch to Blue
7. Turn dial → Adjust Blue value
8. Tap "APPLY" (top-right)
9. Done! Color applied

### Toggle Switch
1. Turn dial → Select device 6
2. Press button → Switch toggles
3. Already back on home page!

---

## 🐛 Common Issues

| Problem | Quick Fix |
|---------|-----------|
| **Button does nothing** | Check logs, verify page switching code |
| **Brightness won't change** | Light must be ON, check entity ID |
| **Color won't apply** | Light must support RGB, brightness >20% |
| **Display names wrong** | Update entity name AND display name, reflash |
| **Won't compile** | Run `./validate.sh` before flashing |

---

## 🔍 Before Flashing Checklist

- [ ] Edit entity IDs in substitutions
- [ ] Edit display names to match
- [ ] Run `./validate.sh`
- [ ] All 7 checks pass ✓
- [ ] Save configuration
- [ ] Flash via USB or OTA

---

## 📝 Key Files

```
source/voice_control/
├── m5dial-config.yaml          ← Main config
├── validate.sh                 ← Run before flashing!
├── M5DIAL-ENHANCED-GUIDE.md    ← Full documentation
└── M5DIAL-TROUBLESHOOTING.md   ← Problem solving
```

---

## 💡 Configuration Tips

### Entity IDs (lines 25-30)
```yaml
light_1: "light.desk_lamp"      # YOUR entity ID here
light_2: "light.bedroom"
light_3: "light.kitchen"
```

### Display Names (lines 33-38)
```yaml
light_1_name: "Desk"      # 4-5 chars max!
light_2_name: "Bed"
light_3_name: "Kit"
```

**Rule**: Both must be updated together!

---

## 🎯 Validation Command

```bash
cd source/voice_control
./validate.sh
```

**Expected output:**
```
✓ All 7 checks passed!
✓ READY TO FLASH
```

---

## 📊 Getting Logs

```bash
# View live logs
esphome logs m5dial-config.yaml

# Save to file
esphome logs m5dial-config.yaml > logs.txt
```

---

## 🔗 Quick Links

- **ESPHome Docs**: https://esphome.io
- **M5Dial Specs**: https://docs.m5stack.com/en/core/M5Dial
- **Home Assistant**: https://www.home-assistant.io

---

## 🎨 Color Codes (Customizable)

```yaml
background_color: '000000'  # Black
primary_color: 'FF8C00'     # Orange
secondary_color: 'FFFFFF'   # White
accent_color: '00D9FF'      # Cyan
```

---

## ⚙️ Brightness Step Size

**Default**: 10% per rotation

**Change to 5%**:
```yaml
# Lines 261, 270, 279, 288, 331, 340, 349, 358
brightness_step_pct: '5'    # Was '10'
brightness_step_pct: '-5'   # Was '-10'
```

---

## 🚀 OTA Update

1. Edit config
2. Run `./validate.sh`
3. ESPHome → **Wirelessly**
4. Done in ~30 seconds!

---

## 💾 Backup Config

```bash
# Save working config
cp m5dial-config.yaml m5dial-config-backup.yaml

# Commit to git
git add m5dial-config.yaml
git commit -m "Working M5Dial config"
```

---

**Keep this card handy while configuring your M5Dial! 📋**
