# M5Dial Troubleshooting Quick Reference

**Quick solutions to common issues with the enhanced M5Dial configuration**

---

## 🚨 Compilation Errors

### ❌ Error: "Must be string, got <class 'esphome.helpers.EInt'>"

```
sensor.rotary_encoder: [source /config/esphome/guel.yaml:261]
  brightness_step_pct: 10
  Must be string, got <class 'esphome.helpers.EInt'>
```

**Cause**: `brightness_step_pct` values must be strings, not integers

**Fix**:
```yaml
# WRONG:
brightness_step_pct: 10

# CORRECT:
brightness_step_pct: '10'
```

**Prevention**: Run `./validate.sh` before flashing (catches this automatically!)

---

### ❌ Error: "could not determine a constructor for the tag '!secret'"

```
YAML syntax error: could not determine a constructor for the tag '!secret'
```

**Cause**: Missing secrets file or validation script can't parse ESPHome tags

**Fix for Validation**: The validation script now handles `!secret` tags (v1.1+)

**Fix for ESPHome**:
1. Create `secrets.yaml` in ESPHome folder:
```yaml
wifi_ssid: "YourNetwork"
wifi_password: "YourPassword"
api_encryption_key: "your-32-char-key-here"
ota_password: "your-ota-password"
```

2. Run: `esphome secrets m5dial-config.yaml` to verify

---

### ❌ Error: "Unknown substitution 'light_1_name'"

```
Error while processing template: Unknown substitution 'light_1_name'
```

**Cause**: Display name not defined in substitutions

**Fix**:
```yaml
substitutions:
  light_1: "light.desk_lamp"    # Entity ID
  light_1_name: "Desk"          # ← ADD THIS!
```

**Rule**: Every entity needs a matching display name:
- `light_1` → `light_1_name`
- `light_2` → `light_2_name`
- `climate_entity` → `climate_name`
- `switch_1` → `switch_1_name`

---

## 🔘 Button & Navigation Issues

### ❌ Button Press Does Nothing

**Symptoms**:
- Hear beep sound
- Screen doesn't change
- Can't enter control mode

**Diagnosis**:
```bash
# Check logs
esphome logs m5dial-config.yaml
```

Look for errors like: `display object has no member 'show_page'`

**Fix**: Ensure page switching is present (line ~479):
```yaml
on_press:
  - lambda: |-
      if (id(selected_device) <= 4) {
        id(control_mode) = 1;
        id(dial_display).show_page(id(control_page));  # ← MUST HAVE THIS!
      }
```

**Prevention**: Validation script checks this (Step 4)

---

### ❌ Can't Return to Home Page

**Symptoms**:
- Stuck in control mode
- Pressing button does nothing
- Touchscreen "< Home" doesn't work

**Fix**: Check return-to-home logic (line ~489):
```yaml
else {
  id(control_mode) = 0;
  id(dial_display).show_page(id(home_page));  # ← MUST HAVE THIS!
}
```

Also verify touchscreen home button (line ~516):
```yaml
on_press:
  - lambda: |-
      id(control_mode) = 0;
      id(dial_display).show_page(id(home_page));  # ← MUST HAVE THIS!
```

---

## 💡 Brightness Control Issues

### ❌ Dial Turns But Brightness Doesn't Change

**Symptoms**:
- Rotation works on home page
- In brightness mode, dial doesn't affect light
- No errors in logs

**Diagnosis Checklist**:
1. ✅ Is the light turned ON in Home Assistant?
2. ✅ Does the light support brightness?
3. ✅ Is the entity ID correct?
4. ✅ Check ESPHome logs for service call errors

**Check Logs**:
```bash
esphome logs m5dial-config.yaml | grep "light.turn_on"
```

Look for successful calls:
```
[D][homeassistant.service:029]: Service light.turn_on called
  entity_id: light.desk_lamp
  brightness_step_pct: 10
```

**Common Causes**:

**1. Light is OFF**
- Turn light ON in Home Assistant first
- Then adjust brightness with M5Dial

**2. Wrong Entity ID**
```yaml
# Check in Home Assistant → Developer Tools → States
substitutions:
  light_1: "light.desk_lamp"  # ← Must match exactly!
```

**3. Light Doesn't Support Brightness**
- Check light capabilities in Home Assistant
- Some switches appear as lights but don't dim
- Use a different device or remove from config

---

### ❌ Brightness Shows as 0% But Light is On

**Symptoms**:
- Light is ON in Home Assistant
- M5Dial shows 0% or no percentage
- Circular arc is empty

**Cause**: Brightness sensor not receiving data

**Fix**: Check sensor configuration (lines 375-398):
```yaml
sensor:
  - platform: homeassistant
    id: light_1_brightness
    entity_id: ${light_1}    # ← Must match your light
    attribute: brightness
    filters:
      - lambda: 'if (isnan(x)) { return 0; } else { return x; }'
```

**Verify in Home Assistant**:
1. Go to Developer Tools → States
2. Find your light entity
3. Check attributes → should have `brightness: 0-255`
4. If no brightness attribute, light doesn't support dimming

---

## 🎨 Color Picker Issues

### ❌ Color Doesn't Apply

**Symptoms**:
- Adjust RGB values in color picker
- Tap "APPLY"
- Light color doesn't change

**Diagnosis**:
```bash
esphome logs m5dial-config.yaml | grep "rgb_color"
```

Should see:
```
[D][homeassistant.service:029]: Service light.turn_on called
  entity_id: light.desk_lamp
  rgb_color: [255,128,64]
```

**Common Causes**:

**1. Light Doesn't Support RGB**
- Check light capabilities in Home Assistant
- Light must support `rgb_color` attribute
- White-only lights won't change color
- Solution: Use RGB/RGBW lights only

**2. Brightness Too Low**
- Some lights don't show color when very dim
- Turn brightness to >20% first
- Then adjust color

**3. Wrong Logic Order (Bug)**
Check apply button logic (line ~542):
```yaml
on_press:
  # CORRECT: Check mode BEFORE changing it
  - if:
      condition:
        lambda: 'return id(control_mode) == 2 && ...'  # ← Mode 2!
      then:
        - homeassistant.action: ...

  # WRONG: This would be AFTER mode changed to 1
  - lambda: 'id(control_mode) = 1;'
```

**Prevention**: Validation script checks this (Step 6)

---

### ❌ Can't Switch RGB Channels

**Symptoms**:
- In color picker mode
- Tap bottom of screen
- Channel doesn't change (stays on RED)

**Fix**: Check touchscreen region (lines 609-625):
```yaml
binary_sensor:
  - platform: touchscreen
    name: "Next RGB Channel"
    x_min: 70      # ← Bottom center region
    x_max: 170
    y_min: 200
    y_max: 240
    on_press:
      - lambda: |-
          if (id(control_mode) == 2) {
            id(color_channel) = (id(color_channel) + 1) % 3;
          }
```

**Test**: Touch different areas of screen to find sensitive region

---

## 📱 Display Issues

### ❌ Text Not Following Circular Contour

**Symptoms**:
- Text appears straight across top/bottom
- Not curved like in examples

**Cause**: Old configuration version

**Check**: Look for curved text code (line ~715):
```yaml
// Curved title text along top arc
const char* title = "SELECT DEVICE";
float title_spacing = 5.5;  # ← Must have this!
for (int i = 0; i < title_len; i++) {
  float angle = (title_start_angle + i * title_spacing) * 0.01745329;
  // ... positioning code
}
```

**Fix**: Update to latest config with curved text support

---

### ❌ Display Names Don't Match Entities

**Symptoms**:
- Changed `light_1: "light.kitchen"`
- Display still shows "Desk" instead of "Kit"

**Cause**: Forgot to update display name

**Fix**: Update BOTH values:
```yaml
light_1: "light.kitchen"     # ← Changed entity
light_1_name: "Kit"           # ← MUST ALSO CHANGE THIS!
```

**Important**: Display names are compiled into firmware
1. Change substitutions
2. Save file
3. Recompile with ESPHome
4. Upload to M5Dial

**Prevention**: Validation script warns about this (Step 2)

---

### ❌ Device States Don't Update

**Symptoms**:
- Light is ON in Home Assistant
- M5Dial shows it as OFF (white circle)
- State doesn't update in real-time

**Cause**: State sensor not working

**Fix**: Check text sensor configuration (lines 410-437):
```yaml
text_sensor:
  - platform: homeassistant
    id: light_1_state
    entity_id: ${light_1}    # ← Must match your light
    internal: true
```

**Verify**:
```bash
esphome logs m5dial-config.yaml | grep "light_1_state"
```

Should see state updates:
```
[D][text_sensor:064]: 'light_1_state': Received new state on
[D][text_sensor:064]: 'light_1_state': Received new state off
```

---

## 🔌 Device Connection Issues

### ❌ Device Not Found in Home Assistant

**Symptoms**:
- M5Dial powers on
- Display works
- Doesn't appear in Home Assistant

**Check**:
1. WiFi connected? (check M5Dial logs)
2. API encryption key matches?
3. ESPHome integration installed?

**Fix**:
```bash
# Check M5Dial logs
esphome logs m5dial-config.yaml
```

Look for:
```
[I][wifi:504]: WiFi Connected!
[C][api:139]: API Server:
  Address: 192.168.1.XXX:6053
```

If no WiFi connection:
- Check SSID/password in secrets.yaml
- Ensure 2.4GHz network (not 5GHz!)
- Try fallback hotspot: "M5Dial Controller Fallback"

---

### ❌ OTA Updates Fail

**Symptoms**:
- Try to upload wirelessly
- Upload times out or fails
- Have to use USB cable

**Causes**:
1. **Weak WiFi signal**: Move M5Dial closer to router
2. **Firewall blocking**: Check port 6053 is open
3. **Power cycling during upload**: Keep powered on
4. **Different network**: Ensure computer and M5Dial on same network

**Fix**:
```bash
# Try upload with more verbose output
esphome upload m5dial-config.yaml --device 192.168.1.XXX
```

If fails, use USB:
```bash
esphome run m5dial-config.yaml
```

---

## 🔧 Validation Script Issues

### ❌ Validation Script Fails

**Error**: `./validate.sh: command not found`

**Fix**:
```bash
chmod +x validate.sh validate-m5dial.py
./validate.sh
```

---

**Error**: `ModuleNotFoundError: No module named 'yaml'`

**Fix**:
```bash
pip install pyyaml
./validate.sh
```

---

**Error**: Validation says "READY TO FLASH" but ESPHome compilation fails

**Reason**: Validation script catches common errors but not all ESPHome-specific issues

**Fix**: Check ESPHome logs for specific error, then:
1. Search error message online
2. Check ESPHome documentation
3. Verify hardware pins match your M5Dial model

---

## 📊 Quick Diagnosis Flowchart

```
Issue with M5Dial?
│
├─ Won't compile?
│  ├─ Run ./validate.sh
│  ├─ Check error message
│  └─ Fix highlighted issues
│
├─ Compiles but button doesn't work?
│  ├─ Check logs for errors
│  ├─ Verify show_page() calls present
│  └─ Test with different button press
│
├─ Brightness doesn't change?
│  ├─ Is light ON?
│  ├─ Does light support brightness?
│  ├─ Check entity ID correct?
│  └─ View ESPHome logs
│
├─ Color doesn't apply?
│  ├─ Does light support RGB?
│  ├─ Is brightness >20%?
│  ├─ Check apply button logic
│  └─ View ESPHome logs
│
└─ Display names wrong?
   ├─ Update BOTH entity & display name
   ├─ Recompile firmware
   └─ Upload to M5Dial
```

---

## 🆘 Getting Help

**Before asking for help, collect this info:**

1. **ESPHome Logs**:
```bash
esphome logs m5dial-config.yaml > m5dial-logs.txt
```

2. **Validation Output**:
```bash
./validate.sh > validation-output.txt
```

3. **Your Configuration**:
- Substitutions section (lines 11-39)
- Any custom modifications

4. **Symptoms**:
- What you're trying to do
- What actually happens
- When it started failing

**Resources**:
- [ESPHome Discord](https://discord.gg/KhAMKrd)
- [Home Assistant Community](https://community.home-assistant.io)
- [ESPHome GitHub Issues](https://github.com/esphome/issues/issues)

---

## ✅ Prevention Checklist

**Before Every Flash:**
- [ ] Run `./validate.sh`
- [ ] All 7 checks pass
- [ ] Entity IDs verified in Home Assistant
- [ ] Display names updated to match entities
- [ ] Changes saved

**After Flashing:**
- [ ] Check M5Dial boots and shows home page
- [ ] Test device selection (turn dial)
- [ ] Test button press (enter control mode)
- [ ] Test brightness control (if using lights)
- [ ] Test color picker (if using RGB lights)
- [ ] Verify states update (devices show ON/OFF correctly)

---

**Most issues are caught by the validation script! Always run `./validate.sh` first! 🎯**
