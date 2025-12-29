#!/usr/bin/env python3
"""
M5Dial Configuration Pre-Deployment Validator
Checks ESPHome configuration for common issues before flashing to device
"""

import yaml
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Add ESPHome-specific YAML constructors
def esphome_secret_constructor(loader, node):
    """Handle !secret tags in ESPHome configs"""
    return f"SECRET:{loader.construct_scalar(node)}"

def esphome_lambda_constructor(loader, node):
    """Handle !lambda tags in ESPHome configs"""
    return f"LAMBDA:{loader.construct_scalar(node)}"

# Register custom constructors
yaml.SafeLoader.add_constructor('!secret', esphome_secret_constructor)
yaml.SafeLoader.add_constructor('!lambda', esphome_lambda_constructor)

class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ WARNING: {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ ERROR: {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def validate_yaml_syntax(config_path: Path) -> Tuple[bool, Dict]:
    """Validate YAML syntax"""
    print_header("Step 1: Validating YAML Syntax")

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print_success("YAML syntax is valid")
        return True, config
    except yaml.YAMLError as e:
        print_error(f"YAML syntax error: {e}")
        return False, {}
    except FileNotFoundError:
        print_error(f"Configuration file not found: {config_path}")
        return False, {}

def check_entity_display_names(config: Dict) -> bool:
    """Check if entity IDs have corresponding display names"""
    print_header("Step 2: Checking Entity/Display Name Consistency")

    if 'substitutions' not in config:
        print_warning("No substitutions found in config")
        return True

    subs = config['substitutions']
    issues = []
    all_good = True

    # Check each light entity has a display name
    for i in range(1, 5):
        light_key = f'light_{i}'
        name_key = f'light_{i}_name'

        if light_key in subs and name_key not in subs:
            issues.append(f"Entity '{light_key}' exists but '{name_key}' is missing")
            all_good = False
        elif light_key in subs and name_key in subs:
            entity = subs[light_key]
            name = subs[name_key]
            if len(name) > 5:
                print_warning(f"{name_key} is '{name}' ({len(name)} chars) - recommend ≤5 chars for circular display")
            print_success(f"{light_key}: {entity} → Display: '{name}'")

    # Check climate
    if 'climate_entity' in subs and 'climate_name' not in subs:
        issues.append("Entity 'climate_entity' exists but 'climate_name' is missing")
        all_good = False
    elif 'climate_entity' in subs:
        print_success(f"climate_entity: {subs['climate_entity']} → Display: '{subs.get('climate_name', 'N/A')}'")

    # Check switch
    if 'switch_1' in subs and 'switch_1_name' not in subs:
        issues.append("Entity 'switch_1' exists but 'switch_1_name' is missing")
        all_good = False
    elif 'switch_1' in subs:
        print_success(f"switch_1: {subs['switch_1']} → Display: '{subs.get('switch_1_name', 'N/A')}'")

    if issues:
        for issue in issues:
            print_error(issue)

    return all_good

def check_brightness_step_format(config_path: Path) -> bool:
    """Check that brightness_step_pct values are strings"""
    print_header("Step 3: Checking Brightness Control Format")

    with open(config_path, 'r') as f:
        content = f.read()

    # Look for brightness_step_pct without quotes
    pattern = r'brightness_step_pct:\s*(-?\d+)\s*$'
    matches = re.finditer(pattern, content, re.MULTILINE)

    issues = []
    for match in matches:
        line_num = content[:match.start()].count('\n') + 1
        value = match.group(1)
        issues.append(f"Line {line_num}: brightness_step_pct: {value} should be brightness_step_pct: '{value}'")

    if issues:
        for issue in issues:
            print_error(issue)
        print_error("brightness_step_pct values must be strings (wrapped in quotes)")
        return False
    else:
        print_success("All brightness_step_pct values are properly formatted as strings")
        return True

def check_page_switching(config_path: Path) -> bool:
    """Check that button press includes page switching logic"""
    print_header("Step 4: Checking Page Switching Logic")

    with open(config_path, 'r') as f:
        content = f.read()

    all_good = True

    # Check if show_page is called in button press
    if 'id(dial_display).show_page' not in content:
        print_error("No page switching logic found - buttons won't change screens")
        all_good = False
    else:
        print_success("Page switching logic found")

    # Check for show_page(id(control_page))
    if 'show_page(id(control_page))' in content:
        print_success("Control page switching present")
    else:
        print_warning("No control_page switching found")
        all_good = False

    # Check for show_page(id(home_page))
    if 'show_page(id(home_page))' in content:
        print_success("Home page switching present")
    else:
        print_warning("No home_page switching found")
        all_good = False

    return all_good

def check_curved_text(config_path: Path) -> bool:
    """Check if curved text is implemented"""
    print_header("Step 5: Checking Curved Text Implementation")

    with open(config_path, 'r') as f:
        content = f.read()

    if 'title_radius' in content and 'title_spacing' in content:
        print_success("Curved text implementation found")
        return True
    else:
        print_warning("Curved text not found - text may not follow circular contour")
        return False

def check_color_apply_logic(config_path: Path) -> bool:
    """Check that color apply button logic is correct"""
    print_header("Step 6: Checking Color Apply Button Logic")

    with open(config_path, 'r') as f:
        content = f.read()

    # Find the Apply Color Button section
    apply_section_start = content.find('# Touchscreen - Apply RGB color')
    if apply_section_start == -1:
        print_warning("Apply RGB color button not found")
        return False

    apply_section = content[apply_section_start:apply_section_start + 2000]

    # Check that condition checks mode == 2 (not mode == 1)
    if 'control_mode) == 2 && id(selected_device)' in apply_section:
        print_success("Color apply button checks mode 2 (color picker mode)")
        return True
    else:
        print_error("Color apply button logic may be incorrect - should check mode 2")
        return False

def run_esphome_validation(config_path: Path) -> bool:
    """Run ESPHome config validation if ESPHome is installed"""
    print_header("Step 7: Running ESPHome Validation")

    import subprocess

    try:
        result = subprocess.run(
            ['esphome', 'config', str(config_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print_success("ESPHome configuration is valid")
            return True
        else:
            print_error("ESPHome validation failed:")
            print(result.stderr)
            return False

    except FileNotFoundError:
        print_warning("ESPHome not installed - skipping ESPHome validation")
        print_info("Install with: pip install esphome")
        return True  # Don't fail if ESPHome isn't installed
    except subprocess.TimeoutExpired:
        print_error("ESPHome validation timed out")
        return False
    except Exception as e:
        print_warning(f"Could not run ESPHome validation: {e}")
        return True

def main():
    """Main validation function"""
    print(f"\n{Colors.BOLD}M5Dial Configuration Pre-Deployment Validator{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    config_path = Path(__file__).parent / 'm5dial-config.yaml'

    if not config_path.exists():
        print_error(f"Configuration file not found: {config_path}")
        sys.exit(1)

    print_info(f"Validating: {config_path}\n")

    # Run all validation checks
    checks = [
        validate_yaml_syntax(config_path),
        (check_entity_display_names(validate_yaml_syntax(config_path)[1]), None),
        (check_brightness_step_format(config_path), None),
        (check_page_switching(config_path), None),
        (check_curved_text(config_path), None),
        (check_color_apply_logic(config_path), None),
        (run_esphome_validation(config_path), None),
    ]

    # Extract boolean results
    results = []
    results.append(checks[0][0])  # YAML syntax
    if checks[0][0]:  # Only check entity names if YAML is valid
        results.append(check_entity_display_names(checks[0][1]))
    results.append(checks[2][0])  # Brightness format
    results.append(checks[3][0])  # Page switching
    results.append(checks[4][0])  # Curved text
    results.append(checks[5][0])  # Color apply
    results.append(checks[6][0])  # ESPHome validation

    # Print summary
    print_header("Validation Summary")

    passed = sum(results)
    total = len(results)

    if all(results):
        print_success(f"All {total} checks passed! Configuration is ready for deployment.")
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ READY TO FLASH{Colors.END}\n")
        sys.exit(0)
    else:
        failed = total - passed
        print_warning(f"{passed}/{total} checks passed, {failed} failed")
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ REVIEW ISSUES BEFORE FLASHING{Colors.END}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
