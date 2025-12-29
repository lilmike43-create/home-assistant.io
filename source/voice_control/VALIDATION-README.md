# M5Dial Pre-Deployment Validation

Automated testing to catch configuration errors **before** flashing your M5Dial device.

## 🚀 Quick Start

```bash
cd source/voice_control
./validate.sh
```

That's it! The script will check your configuration and tell you if it's safe to flash.

## ✅ What Gets Validated

The validation script performs **7 comprehensive checks**:

### 1. **YAML Syntax Validation**
- Ensures the configuration file is valid YAML
- Catches formatting errors before ESPHome sees them

### 2. **Entity/Display Name Consistency**
- Verifies every entity ID has a matching display name
- Example: `light_1` requires `light_1_name`
- Warns if display names are too long (>5 characters) for the circular screen

### 3. **Brightness Control Format**
- Checks that `brightness_step_pct` values are strings (not integers)
- Catches the common error: `brightness_step_pct: 10` → should be `'10'`

### 4. **Page Switching Logic**
- Ensures button presses actually switch display pages
- Verifies `show_page(id(control_page))` and `show_page(id(home_page))` are present
- Prevents the "button does nothing" bug

### 5. **Curved Text Implementation**
- Checks if curved text is implemented for circular screen
- Ensures text follows the natural contour of the M5Dial

### 6. **Color Apply Button Logic**
- Validates color picker apply button checks correct mode (mode 2)
- Prevents the "color doesn't apply" bug

### 7. **ESPHome Validation** (if installed)
- Runs official ESPHome configuration validation
- Catches all ESPHome-specific errors

## 📊 Example Output

```
M5Dial Configuration Pre-Deployment Validator
============================================================

ℹ Validating: m5dial-config.yaml

============================================================
Step 1: Validating YAML Syntax
============================================================

✓ YAML syntax is valid

============================================================
Step 2: Checking Entity/Display Name Consistency
============================================================

✓ light_1: light.Smart_LED_Bulb → Display: 'Desk'
✓ light_2: light.Office → Display: 'Bed'
✓ light_3: light.kitchen → Display: 'Kit'
✓ light_4: light.living_room → Display: 'Live'
✓ climate_entity: climate.living_room → Display: 'Clim'
✓ switch_1: switch.coffee_maker → Display: 'Coff'

============================================================
Step 3: Checking Brightness Control Format
============================================================

✓ All brightness_step_pct values are properly formatted as strings

============================================================
Step 4: Checking Page Switching Logic
============================================================

✓ Page switching logic found
✓ Control page switching present
✓ Home page switching present

============================================================
Step 5: Checking Curved Text Implementation
============================================================

✓ Curved text implementation found

============================================================
Step 6: Checking Color Apply Button Logic
============================================================

✓ Color apply button checks mode 2 (color picker mode)

============================================================
Step 7: Running ESPHome Validation
============================================================

✓ ESPHome configuration is valid

============================================================
Validation Summary
============================================================

✓ All 7 checks passed! Configuration is ready for deployment.

✓ READY TO FLASH

To flash your M5Dial, run:
  esphome run m5dial-config.yaml
```

## ⚠️ When Validation Fails

If validation fails, you'll see colored output showing exactly what's wrong:

- **🔴 Red (ERROR)**: Critical issue that must be fixed
- **🟡 Yellow (WARNING)**: Potential issue or best practice violation
- **🔵 Blue (INFO)**: Informational message

Example error output:
```
✗ ERROR: Line 261: brightness_step_pct: 10 should be brightness_step_pct: '10'
✗ ERROR: brightness_step_pct values must be strings (wrapped in quotes)
```

## 🛠️ Installation Requirements

**Minimum (works without ESPHome installed):**
```bash
# Python 3.6+ with PyYAML
pip install pyyaml
```

**Recommended (full validation):**
```bash
# Install ESPHome for complete validation
pip install esphome pyyaml
```

## 📝 Usage in Development Workflow

### Before Every Flash
```bash
# 1. Edit your configuration
vim m5dial-config.yaml

# 2. Validate
./validate.sh

# 3. If validation passes, flash
esphome run m5dial-config.yaml
```

### Integrate with Git Pre-Commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
cd source/voice_control
./validate.sh
if [ $? -ne 0 ]; then
    echo "Validation failed! Commit aborted."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

Now validation runs automatically before every commit!

## 🔧 Customizing Validation

Edit `validate-m5dial.py` to add your own checks:

```python
def check_custom_rule(config_path: Path) -> bool:
    """Add your custom validation logic"""
    print_header("Step 8: My Custom Check")

    # Your validation logic here

    return True  # or False if check fails
```

Then add it to the `results` list in `main()`.

## 🐛 Common Issues Caught by Validation

1. **Brightness control not working**
   - Catches: `brightness_step_pct: 10` (should be `'10'`)

2. **Button clicks do nothing**
   - Catches: Missing `show_page()` calls

3. **Color picker doesn't apply**
   - Catches: Wrong mode check in apply button

4. **Display names don't match entities**
   - Catches: Mismatched entity/display name pairs

5. **YAML syntax errors**
   - Catches: Indentation, missing colons, etc.

## 📚 Exit Codes

- `0`: All validations passed, safe to flash
- `1`: One or more validations failed, review issues

Use in scripts:
```bash
./validate.sh && esphome run m5dial-config.yaml || echo "Fix errors first!"
```

## 🎯 Benefits

- **Catch errors early**: Find issues before spending time compiling
- **Faster development**: No more compile-flash-test-repeat cycles
- **Confidence**: Know your config is correct before flashing
- **Learning tool**: Understand common mistakes and best practices

## 💡 Tips

1. **Run validation often**: It's fast! Run it after every change
2. **Read the warnings**: They highlight best practices
3. **Check before commits**: Use the pre-commit hook
4. **Update validation**: Add checks for your own common mistakes

---

**Questions?** The validation script is just Python - read the code to understand what it checks, or add your own validation rules!
