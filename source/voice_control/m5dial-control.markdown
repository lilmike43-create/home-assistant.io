---
title: "M5Dial for Home Assistant control"
product_name: M5Dial
device_name_entry: M5Stack M5Dial
config_link: /voice_control/m5dial-control/#removing-the-configuration
related:
  - docs: /integrations/esphome/
    title: ESPHome integration
  - docs: /voice_control/troubleshooting/
    title: General troubleshooting section for Assist
  - url: https://esphome.io
    title: ESPHome documentation
  - url: https://docs.m5stack.com/en/core/M5Dial
    title: M5Dial hardware documentation
---

This tutorial will guide you to turn an M5Dial into a versatile Home Assistant controller. Use the rotary encoder and circular touchscreen display to control lights, adjust volume, change climate settings, and more—all with an intuitive interface that provides real-time feedback.

## About the M5Dial

The M5Dial is an ESP32-S3 based smart rotary knob with a 1.28-inch round touch screen (240x240 GC9A01 driver), a RFID 2 unit (WS1850S), and a rotary encoder. It combines physical rotation control with a vibrant color display, making it perfect for:

- Controlling lights (brightness and color)
- Adjusting volume for media players
- Setting climate control temperatures
- Navigating through multiple devices or rooms
- Creating custom control interfaces

## Prerequisites

- Home Assistant 2024.1 or later, installed with the Home Assistant Operating System. If you do not have Home Assistant installed yet, refer to the [installation page](/installation/) for instructions.
- The password to your 2.4&nbsp;GHz Wi-Fi network
- Chrome or Edge browser on a desktop (not Android/iOS)
- [M5Stack M5Dial](https://shop.m5stack.com/products/m5dial-smart-rotary-knob-w-1-28-round-touch-screen) device
- USB-C cable to connect the M5Dial

## Installing ESPHome firmware on the M5Dial

Before you can use this device with Home Assistant, you need to install ESPHome firmware on it.

### Option 1: Using the ESPHome Add-on (Recommended)

1. Install the ESPHome add-on in Home Assistant:
   - Go to {% my supervisor title="**Settings** > **Add-ons**" %}.
   - Select **Add-on Store** and search for **ESPHome**.
   - Select **ESPHome** and then select **Install**.

2. Once installed, select **Start** and enable **Show in sidebar**.

3. Open the ESPHome dashboard from your sidebar.

4. Select **+ New Device** and follow the wizard:
   - Give your device a name (e.g., "Living Room Dial").
   - Select **ESP32-S3** as the device type.
   - Enter your Wi-Fi credentials.

5. After the initial configuration is created, select **Edit** on your new device.

6. Replace the configuration with the M5Dial configuration (see [Basic Configuration](#basic-configuration) below).

7. Select **Save** and then **Install**.

8. For the first installation, select **Plug into this computer**.
   - Connect your M5Dial via USB-C.
   - Follow the browser prompts to flash the firmware.

9. After the first flash, future updates can be done wirelessly (OTA).

### Option 2: Using ESP Web Tools

For advanced users who want to use pre-compiled firmware:

1. Make sure this page is opened in a Chromium-based browser on a desktop.
2. Connect your M5Dial to your computer using a USB-C cable.
3. Use the ESPHome web flasher or compile your own firmware using the configuration below.

## Basic Configuration

Here's a basic ESPHome configuration for the M5Dial that sets up the display, rotary encoder, and touch screen:

```yaml
esphome:
  name: m5dial-controller
  friendly_name: M5Dial Controller
  platformio_options:
    board_build.flash_mode: dio

esp32:
  board: esp32-s3-devkitc-1
  flash_size: 8MB
  framework:
    type: esp-idf

# Enable logging
logger:

# Enable Home Assistant API
api:
  encryption:
    key: !secret api_encryption_key

ota:
  - platform: esphome
    password: !secret ota_password

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "M5Dial Fallback Hotspot"
    password: "m5dial123"

captive_portal:

# I2C Bus for touchscreen and RTC
i2c:
  - id: internal_i2c
    sda: GPIO11
    scl: GPIO12
    scan: false

# SPI Bus for display
spi:
  id: spi_bus
  mosi_pin: GPIO5
  clk_pin: GPIO6

# Touchscreen
touchscreen:
  - platform: ft5x06
    id: touchscreen_dial
    i2c_id: internal_i2c
    address: 0x38

# RTC (Real-Time Clock)
time:
  - platform: pcf8563
    id: rtctime
    i2c_id: internal_i2c
    address: 0x51
    update_interval: never

  - platform: homeassistant
    id: esptime
    on_time_sync:
      then:
        - pcf8563.write_time:

# Buzzer for sound feedback
output:
  - platform: ledc
    pin: GPIO3
    id: buzzer

  # Backlight PWM control
  - platform: ledc
    pin: GPIO9
    id: backlight_pwm

# Backlight control
light:
  - platform: monochromatic
    name: "Backlight"
    output: backlight_pwm
    id: backlight
    default_transition_length: 0s
    restore_mode: ALWAYS_ON
    internal: true

# Sound
rtttl:
  output: buzzer

# Display configuration (GC9A01A 240x240 round display)
# IMPORTANT: Use ili9xxx platform with GC9A01A model and invert_colors: true
display:
  - platform: ili9xxx
    id: dial_display
    model: GC9A01A
    cs_pin: GPIO7
    dc_pin: GPIO4
    reset_pin: GPIO8
    invert_colors: true
    update_interval: 0.05s
    rotation: 0
    lambda: |-
      // Clear screen with black background
      it.filled_circle(120, 120, 120, Color(0, 0, 0));

      // Draw title
      it.print(120, 20, id(font_title), Color(0, 168, 232), TextAlign::TOP_CENTER, "M5Dial");
      it.print(120, 50, id(font_medium), Color(255, 255, 255), TextAlign::TOP_CENTER, "Controller");

      // Draw time
      it.strftime(120, 100, id(font_medium), Color(255, 255, 255), TextAlign::CENTER, "%H %M", id(esptime).now());

      // Draw status message
      it.print(120, 180, id(font_small), Color(255, 255, 255), TextAlign::TOP_CENTER, "Ready");

# Colors
color:
  - id: color_primary
    hex: '00A8E8'
  - id: color_background
    hex: '000000'

# Fonts
font:
  - file: "gfonts://Roboto"
    id: font_title
    size: 24
    glyphs: " !\"#$%&'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~°0123456789"
  - file: "gfonts://Roboto"
    id: font_medium
    size: 18
    glyphs: " !\"#$%&'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~°0123456789"
  - file: "gfonts://Roboto"
    id: font_small
    size: 14
    glyphs: " !\"#$%&'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~°0123456789"

# Rotary Encoder
sensor:
  - platform: rotary_encoder
    name: "Dial Encoder"
    id: dial_encoder
    pin_a: GPIO40
    pin_b: GPIO41
    on_clockwise:
      then:
        - rtttl.play: 'beep:d=64,o=5,b=255:c7'
        - lambda: |-
            ESP_LOGD("encoder", "Clockwise turn");
    on_anticlockwise:
      then:
        - rtttl.play: 'beep:d=64,o=5,b=255:c7'
        - lambda: |-
            ESP_LOGD("encoder", "Counter-clockwise turn");

# Center button (encoder button)
binary_sensor:
  - platform: gpio
    name: "Dial Button"
    id: dial_button
    pin:
      number: GPIO42
      inverted: true
    internal: true
    on_press:
      then:
        - logger.log: "Dial button pressed"

  # WiFi connection status
  - platform: template
    name: "WiFi Connected"
    id: wifi_connected
    lambda: |-
      return wifi::global_wifi_component->is_connected();

# RGB LED (for feedback)
light:
  - platform: esp32_rmt_led_strip
    id: dial_light
    name: "Dial LED"
    rgb_order: GRB
    pin: GPIO21
    num_leds: 1
    rmt_channel: 0
    chipset: WS2812
    default_transition_length: 0s
```

This configuration provides the foundation for your M5Dial. The device will appear in Home Assistant as an ESPHome device with the encoder sensor, button, and LED light entities.

## Using the Rotary Encoder to Control Home Assistant

The rotary encoder can be used to control various Home Assistant entities. Here are practical examples:

### Example 1: Controlling Light Brightness

This example shows how to use the dial to control the brightness of a light in your living room:

```yaml
# Add to your M5Dial configuration
globals:
  - id: current_mode
    type: int
    restore_value: no
    initial_value: '0'  # 0 = light control mode

number:
  - platform: template
    name: "Light Brightness Control"
    id: light_brightness
    min_value: 0
    max_value: 100
    step: 1
    optimistic: true
    on_value:
      then:
        - homeassistant.service:
            service: light.turn_on
            data:
              entity_id: light.living_room
              brightness_pct: !lambda 'return x;'

sensor:
  - platform: rotary_encoder
    name: "Dial Encoder"
    id: dial_encoder
    pin_a:
      number: GPIO40
      mode:
        input: true
        pullup: true
    pin_b:
      number: GPIO41
      mode:
        input: true
        pullup: true
    resolution: 2
    on_clockwise:
      then:
        - number.increment:
            id: light_brightness
            cycle: false
        - component.update: dial_display
    on_anticlockwise:
      then:
        - number.decrement:
            id: light_brightness
            cycle: false
        - component.update: dial_display

display:
  - platform: gc9a01
    id: dial_display
    cs_pin: GPIO7
    dc_pin: GPIO4
    update_interval: 100ms
    lambda: |-
      it.fill(COLOR_BLACK);

      // Draw title
      it.print(120, 30, id(font_title), COLOR_WHITE, TextAlign::CENTER, "Living Room");
      it.print(120, 55, id(font_medium), COLOR_CYAN, TextAlign::CENTER, "Light");

      // Draw brightness value
      int brightness = (int)id(light_brightness).state;
      it.printf(120, 120, id(font_large), COLOR_WHITE, TextAlign::CENTER, "%d%%", brightness);

      // Draw circular progress bar
      int radius = 80;
      int center_x = 120;
      int center_y = 120;
      float progress = brightness / 100.0;

      for (int angle = 0; angle < 360 * progress; angle += 2) {
        float rad = angle * 3.14159 / 180.0;
        int x = center_x + (int)(radius * cos(rad));
        int y = center_y + (int)(radius * sin(rad));
        it.filled_circle(x, y, 3, COLOR_YELLOW);
      }
```

### Example 2: Media Player Volume Control

Control the volume of your media player with visual feedback:

```yaml
number:
  - platform: template
    name: "Media Volume Control"
    id: media_volume
    min_value: 0
    max_value: 100
    step: 2
    optimistic: true
    on_value:
      then:
        - homeassistant.service:
            service: media_player.volume_set
            data:
              entity_id: media_player.living_room_speaker
              volume_level: !lambda 'return x / 100.0;'

sensor:
  - platform: rotary_encoder
    # ... (same pin configuration as above)
    on_clockwise:
      then:
        - number.increment:
            id: media_volume
            cycle: false
        - light.turn_on:
            id: dial_light
            red: 0%
            green: 100%
            blue: 0%
            brightness: 50%
        - component.update: dial_display
    on_anticlockwise:
      then:
        - number.decrement:
            id: media_volume
            cycle: false
        - light.turn_on:
            id: dial_light
            red: 100%
            green: 50%
            blue: 0%
            brightness: 50%
        - component.update: dial_display

binary_sensor:
  - platform: gpio
    name: "Dial Button"
    id: dial_button
    # ... (same pin configuration as above)
    on_press:
      then:
        - homeassistant.service:
            service: media_player.media_play_pause
            data:
              entity_id: media_player.living_room_speaker

display:
  - platform: gc9a01
    id: dial_display
    # ... (same configuration as above)
    lambda: |-
      it.fill(COLOR_BLACK);

      it.print(120, 30, id(font_title), COLOR_WHITE, TextAlign::CENTER, "Media Player");
      it.print(120, 55, id(font_medium), COLOR_CYAN, TextAlign::CENTER, "Volume");

      int volume = (int)id(media_volume).state;
      it.printf(120, 120, id(font_large), COLOR_WHITE, TextAlign::CENTER, "%d", volume);

      // Draw volume bars
      int bar_count = 10;
      int active_bars = (volume * bar_count) / 100;
      for (int i = 0; i < bar_count; i++) {
        int x = 120;
        int y = 160 + (i * 8);
        int bar_width = 60;
        if (i < active_bars) {
          it.filled_rectangle(x - bar_width/2, y, bar_width, 5, COLOR_GREEN);
        } else {
          it.rectangle(x - bar_width/2, y, bar_width, 5, COLOR_DARKGREY);
        }
      }
```

### Example 3: Climate Control (Thermostat)

Use the M5Dial to adjust your thermostat temperature:

```yaml
number:
  - platform: template
    name: "Thermostat Temperature"
    id: thermostat_temp
    min_value: 15
    max_value: 30
    step: 0.5
    optimistic: true
    initial_value: 20
    unit_of_measurement: "°C"
    on_value:
      then:
        - homeassistant.service:
            service: climate.set_temperature
            data:
              entity_id: climate.living_room
              temperature: !lambda 'return x;'

sensor:
  - platform: rotary_encoder
    # ... (same pin configuration)
    on_clockwise:
      then:
        - number.increment:
            id: thermostat_temp
            cycle: false
    on_anticlockwise:
      then:
        - number.decrement:
            id: thermostat_temp
            cycle: false

  - platform: homeassistant
    name: "Current Temperature"
    id: current_temp
    entity_id: climate.living_room
    attribute: current_temperature
    unit_of_measurement: "°C"

display:
  - platform: gc9a01
    id: dial_display
    # ... (same configuration)
    lambda: |-
      it.fill(COLOR_BLACK);

      it.print(120, 20, id(font_medium), COLOR_WHITE, TextAlign::CENTER, "Thermostat");

      // Draw target temperature (large)
      float target = id(thermostat_temp).state;
      it.printf(120, 90, id(font_large), COLOR_ORANGE, TextAlign::CENTER, "%.1f°", target);

      // Draw current temperature (smaller)
      if (id(current_temp).has_state()) {
        float current = id(current_temp).state;
        it.printf(120, 140, id(font_medium), COLOR_CYAN, TextAlign::CENTER, "Current: %.1f°", current);
      }

      // Draw heating/cooling indicator
      if (id(current_temp).has_state()) {
        float current = id(current_temp).state;
        if (target > current + 0.5) {
          it.print(120, 180, id(font_small), COLOR_RED, TextAlign::CENTER, "HEATING");
        } else if (target < current - 0.5) {
          it.print(120, 180, id(font_small), COLOR_BLUE, TextAlign::CENTER, "COOLING");
        } else {
          it.print(120, 180, id(font_small), COLOR_GREEN, TextAlign::CENTER, "IDLE");
        }
      }
```

### Example 4: Multi-Mode Controller

Create a versatile controller that can switch between different control modes:

```yaml
globals:
  - id: control_mode
    type: int
    restore_value: yes
    initial_value: '0'  # 0=lights, 1=volume, 2=climate

number:
  - platform: template
    name: "Light Brightness"
    id: light_value
    min_value: 0
    max_value: 100
    step: 1
    optimistic: true

  - platform: template
    name: "Volume Level"
    id: volume_value
    min_value: 0
    max_value: 100
    step: 2
    optimistic: true

  - platform: template
    name: "Temperature"
    id: temp_value
    min_value: 15
    max_value: 30
    step: 0.5
    optimistic: true

binary_sensor:
  - platform: gpio
    name: "Dial Button"
    id: dial_button
    pin:
      number: GPIO42
      mode:
        input: true
        pullup: true
      inverted: true
    on_press:
      then:
        # Cycle through modes on button press
        - lambda: |-
            id(control_mode) = (id(control_mode) + 1) % 3;
            ESP_LOGD("mode", "Switched to mode %d", id(control_mode));
        - component.update: dial_display
        # Flash LED to indicate mode change
        - light.turn_on:
            id: dial_light
            brightness: 100%
            red: 100%
            green: 100%
            blue: 100%
        - delay: 200ms
        - light.turn_off: dial_light

sensor:
  - platform: rotary_encoder
    name: "Dial Encoder"
    id: dial_encoder
    # ... (same pin configuration)
    on_clockwise:
      then:
        - lambda: |-
            if (id(control_mode) == 0) {
              id(light_value).make_call().number_increment(false).perform();
            } else if (id(control_mode) == 1) {
              id(volume_value).make_call().number_increment(false).perform();
            } else if (id(control_mode) == 2) {
              id(temp_value).make_call().number_increment(false).perform();
            }
    on_anticlockwise:
      then:
        - lambda: |-
            if (id(control_mode) == 0) {
              id(light_value).make_call().number_decrement(false).perform();
            } else if (id(control_mode) == 1) {
              id(volume_value).make_call().number_decrement(false).perform();
            } else if (id(control_mode) == 2) {
              id(temp_value).make_call().number_decrement(false).perform();
            }

display:
  - platform: gc9a01
    id: dial_display
    # ... (same configuration)
    lambda: |-
      it.fill(COLOR_BLACK);

      // Display different UI based on mode
      if (id(control_mode) == 0) {
        // Light mode
        it.print(120, 20, id(font_title), COLOR_YELLOW, TextAlign::CENTER, "LIGHT");
        int brightness = (int)id(light_value).state;
        it.printf(120, 120, id(font_large), COLOR_WHITE, TextAlign::CENTER, "%d%%", brightness);

      } else if (id(control_mode) == 1) {
        // Volume mode
        it.print(120, 20, id(font_title), COLOR_GREEN, TextAlign::CENTER, "VOLUME");
        int volume = (int)id(volume_value).state;
        it.printf(120, 120, id(font_large), COLOR_WHITE, TextAlign::CENTER, "%d", volume);

      } else if (id(control_mode) == 2) {
        // Climate mode
        it.print(120, 20, id(font_title), COLOR_ORANGE, TextAlign::CENTER, "CLIMATE");
        float temp = id(temp_value).state;
        it.printf(120, 120, id(font_large), COLOR_WHITE, TextAlign::CENTER, "%.1f°C", temp);
      }

      // Mode indicator dots at bottom
      for (int i = 0; i < 3; i++) {
        int x = 90 + (i * 30);
        if (i == id(control_mode)) {
          it.filled_circle(x, 210, 5, COLOR_WHITE);
        } else {
          it.circle(x, 210, 5, COLOR_DARKGREY);
        }
      }
```

## Advanced UI Customization

### Custom Graphics and Icons

You can create more sophisticated UIs with custom graphics:

```yaml
# Add font for icons
font:
  - file: "gfonts://Roboto"
    id: font_title
    size: 24
  - file: "gfonts://Roboto"
    id: font_large
    size: 48
  - file: "gfonts://Roboto"
    id: font_medium
    size: 18
  - file: "gfonts://Roboto"
    id: font_small
    size: 14
  # Material Design Icons for visual elements
  - file: "fonts/materialdesignicons-webfont.ttf"
    id: icon_font
    size: 48
    glyphs:
      - "\U000F0335"  # lightbulb
      - "\U000F057E"  # volume-high
      - "\U000F0238"  # home-thermometer

display:
  - platform: gc9a01
    id: dial_display
    # ... (configuration)
    lambda: |-
      it.fill(COLOR_BLACK);

      // Draw icon based on mode
      if (id(control_mode) == 0) {
        it.print(120, 60, id(icon_font), COLOR_YELLOW, TextAlign::CENTER, "\U000F0335");
      } else if (id(control_mode) == 1) {
        it.print(120, 60, id(icon_font), COLOR_GREEN, TextAlign::CENTER, "\U000F057E");
      } else if (id(control_mode) == 2) {
        it.print(120, 60, id(icon_font), COLOR_ORANGE, TextAlign::CENTER, "\U000F0238");
      }

      // ... rest of display code
```

### Animated Transitions

Add smooth animations when values change:

```yaml
# Add animation globals
globals:
  - id: display_value
    type: float
    restore_value: no
    initial_value: '0'
  - id: target_value
    type: float
    restore_value: no
    initial_value: '0'

interval:
  - interval: 50ms
    then:
      - lambda: |-
          // Smooth animation towards target
          float diff = id(target_value) - id(display_value);
          if (abs(diff) > 0.5) {
            id(display_value) += diff * 0.2;  // 20% easing
            id(dial_display).update();
          } else {
            id(display_value) = id(target_value);
          }
```

### Touch Screen Integration

The M5Dial also has a touchscreen. Here's how to add touch controls:

```yaml
# Add touchscreen support
touchscreen:
  - platform: ft63x6
    id: my_touchscreen
    interrupt_pin: GPIO9
    on_touch:
      - lambda: |-
          ESP_LOGI("touch", "Touch at x=%d, y=%d", touch.x, touch.y);

          // Detect touch zones
          int center_x = 120;
          int center_y = 120;
          int dx = touch.x - center_x;
          int dy = touch.y - center_y;
          int distance = sqrt(dx*dx + dy*dy);

          // Center circle touch = toggle
          if (distance < 40) {
            // Toggle action
            ESP_LOGI("touch", "Center touched");
          }

          // Outer ring touch = adjust value based on angle
          else if (distance > 80 && distance < 110) {
            float angle = atan2(dy, dx) * 180.0 / 3.14159;
            int percent = (int)((angle + 180) / 360.0 * 100);
            ESP_LOGI("touch", "Outer ring touched at %d%%", percent);
          }
```

## Integrating with Home Assistant Dashboards

You can create a custom dashboard card to display the M5Dial's current state:

```yaml
# In your Home Assistant configuration.yaml or dashboards
type: entities
title: M5Dial Controller
entities:
  - entity: sensor.dial_encoder
    name: Encoder Position
  - entity: binary_sensor.dial_button
    name: Button State
  - entity: light.dial_led
    name: Status LED
  - entity: number.light_brightness_control
    name: Current Value
```

## Troubleshooting

### Display not working

1. Check your SPI pin connections match the configuration
2. Verify the display driver is correct (GC9A01 for M5Dial)
3. Try different `rotation` values (0, 90, 180, 270) in the display config

### Encoder not responding

1. Verify GPIO pins 40 and 41 are correctly configured
2. Try changing the `resolution` parameter (1, 2, or 4)
3. Check the pullup resistors are enabled

### Wi-Fi connection issues

1. Ensure you're using a 2.4 GHz network (not 5 GHz)
2. Check signal strength near the M5Dial location
3. Use the fallback hotspot to reconfigure Wi-Fi

### LED not lighting up

1. Verify GPIO21 is the correct pin for your M5Dial revision
2. Check the `chipset` setting (WS2812 is correct for most models)
3. Try adjusting `rgb_order` between GRB, RGB, or other combinations

## Removing the Configuration

If you want to reset your M5Dial or remove it from Home Assistant:

1. In Home Assistant, go to {% my integrations title="**Settings** > **Devices & services**" %}.
2. Find the **ESPHome** integration.
3. Locate your M5Dial device and select it.
4. Select the three-dot menu and choose **Delete**.
5. To erase the firmware from the M5Dial itself:
   - Connect it to your computer via USB-C
   - Use the ESPHome dashboard or ESP Web Tools to flash a blank firmware or factory reset

## Additional Resources

- [ESPHome Display Component Documentation](https://esphome.io/components/display/)
- [ESPHome Rotary Encoder Sensor](https://esphome.io/components/sensor/rotary_encoder.html)
- [ESPHome GC9A01 Display](https://esphome.io/components/display/gc9a01.html)
- [M5Stack M5Dial Hardware Documentation](https://docs.m5stack.com/en/core/M5Dial)
- [Home Assistant ESPHome Integration](/integrations/esphome/)

## Next Steps

Now that you have your M5Dial set up, you can:

1. Create custom automations based on encoder movements
2. Design unique UIs for different rooms or scenarios
3. Combine multiple M5Dials for whole-home control
4. Integrate with voice assistants for multimodal control
5. Share your configurations with the community
