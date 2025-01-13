# Raspberry Pi Pico W Doorbell Extension

![A_photo-realistic,_front-facing_image_of_a_traditional_rectangular__doorbell,_taller_than_wide,_attached_to_a_wooden_door_frame._The_metallic__doorbell_features_intricate_details,_and_the_circular_button_has_been__replaced_with_a_vibrant,_realistic_raspberry_fruit,_clearly_distinguishable__with_its_signature_bumpy_texture._The_raspberry_retains_a_small_portion_of__its_green_stem_for_a_natural_touch_and_emits_glowing_WiFi_signal_lines,__symbolizing_modern_connectivity._The_doorbell_occupies_most_of_the_frame,__emphasizing_the_raspberry_and_its_WiFi_signals_as_the_focal_point,_while__the_wooden_frame_is_minimally_visible.](./assets/raspberry-pi-pico-w-doorbell.png)

## Overview
This **Raspberry Pi Pico W** project extends a traditional doorbell to send notifications through multiple channels including Telegram, WhatsApp, SMS, Slack, Discord, and more. It uses **uasyncio** for non-blocking tasks, ensuring the doorbell is monitored continuously while handling network operations efficiently. The system connects to Wi-Fi only when needed, preserving power and bandwidth.

## Features
- **Doorbell Signal Monitoring**: Detects doorbell button presses and sends notifications.
- **Asynchronous Design**: Utilizes `uasyncio` for concurrent LED heartbeats and pin monitoring without blocking.
- **Multiple Notification Channels**:
  - **Telegram**: Messages via bot API
  - **WhatsApp**: Through Twilio's API
  - **SMS**: Via Twilio
  - **Slack**: Using webhooks
  - **Discord**: Using webhooks
  - **Pushover**: Native notifications
  - **Node-RED**: HTTP endpoints
  - **Simple GET**: Basic HTTP requests
- **LED Status Indicator**: 
  - Normal operation: Regular heartbeat pattern
  - WiFi connecting: Fast blink (4x speed)
  - Sending notifications: Solid ON
  - Can be disabled in settings
- **Power-Efficient Networking**: Single WiFi connection for all notifications

![chat_example](./assets/chat.png)

## Pre-Setup
1. **WiFi Network**
   - Have your WiFi SSID and password ready

2. **Telegram Bot**  
   - Create a bot via [BotFather](https://core.telegram.org/bots#6-botfather)
   - Get the Bot Token and Chat IDs

3. **Twilio Account** (for WhatsApp/SMS)
   - Create account at [twilio.com](https://www.twilio.com)
   - Note your Account SID and Auth Token
   - Set up WhatsApp sandbox or SMS number

4. **Slack Integration**
   - Go to your Slack workspace
   - Create new app or use existing
   - Enable Incoming Webhooks
   - Create and copy webhook URL

5. **Discord Webhook**
   - Open server settings
   - Go to Integrations → Webhooks
   - Create webhook and copy URL

6. **Pushover**
   - Create account at [pushover.net](https://pushover.net)
   - Create application
   - Note your user key and application token

7. **Node-RED**
   - Set up flow with HTTP input node
   - Configure endpoint path
   - Note server IP and port

## Hardware Setup

> **Note**: The doorbell input uses a pull-up configuration, triggered when grounded.

```
    +------------------+
    |          (signal)|        (2.2k)
    |             GP10 +--------/\/\/\--------------------------- Signal (+)
    | Raspberry        |
    | Pi        (~3.3V)|       +-------------------------+
    | Pico W      VSYS +-------+                     VCC +------- VCC
    |                  |       |  Boost-Buck Converter   |  
    |              GND +-------+                         |
    |      |LED|       |       |                     GND +-------+
    +------+---+-------+       +-------------------------+       |
                                                                 |
                                                               --+--
                                                                ---
```

1. **GP10** is the default doorbell pin (configurable in `settings.py`)
2. **LED** uses onboard LED (referenced as `"LED"` in code)
3. **Power** via USB or regulated 5V-3.3V supply

## Software Components
- **`main.py`**: Entry point and async task orchestration
- **`config/`**:
  - `credentials.py`: All sensitive configuration
  - `settings.py`: General settings and provider configuration
- **`core/`**:
  - `heart_led.py`: LED status indicator
  - `network_manager.py`: WiFi connection handling
- **`notifications/`**:
  - `notifier.py`: Notification orchestrator
  - `base_provider.py`: Provider interface
  - **`providers/`**:
    - `telegram.py`: Telegram bot implementation
    - `twilio_whatsapp.py`: WhatsApp via Twilio
    - `twilio_sms.py`: SMS via Twilio
    - `slack_webhook.py`: Slack integration
    - `discord_webhook.py`: Discord integration
    - `pushover.py`: Pushover notifications
    - `node_red.py`: Node-RED integration
    - `simple_get.py`: Basic GET requests
- **`utils/`**:
  - `logging.py`: Debug logging utilities

## Installation
1. **Get the Code**
   ```bash
   git clone https://github.com/yourusername/raspberry-pi-pico-w-doorbell.git
   cd raspberry-pi-pico-w-doorbell
   ```

2. **Configure Credentials**
   In `src/config/credentials.py`:
   ```python
   # WiFi
   WIFI_SSID = "your_wifi_ssid"
   WIFI_PASS = "your_wifi_password"

   # Telegram
   TELEGRAM_BOT_TOKEN = "your_bot_token"
   TELEGRAM_CHAT_IDS = ["chat_id_1", "chat_id_2"]

   # Twilio
   TWILIO_ACCOUNT_SID = "your_account_sid"
   TWILIO_AUTH_TOKEN = "your_auth_token"
   TWILIO_FROM_PHONE = "+1234567890"
   TWILIO_TO_PHONES = [
    "+1234567890",
    "+0987654321"
   ]
   
   TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"
   TWILIO_WHATSAPP_TO = [
    "whatsapp:+1234567890"
   ]

   # Slack
   SLACK_WEBHOOK_URLS = [
       "https://hooks.slack.com/services/YOUR/WEBHOOK/URL1",
       "https://hooks.slack.com/services/YOUR/WEBHOOK/URL2"
   ]

   # Discord
   DISCORD_WEBHOOK_URLS = [
       "https://discord.com/api/webhooks/YOUR/WEBHOOK/URL1",
       "https://discord.com/api/webhooks/YOUR/WEBHOOK/URL2"
   ]

   # Pushover
   PUSHOVER_TOKEN = "your_app_token"
   PUSHOVER_USER_KEYS = [
    "user_key_1",
    "user_key_2"
   ]

   # Node-RED
   NODE_RED_HOST = "10.0.0.10"
   NODE_RED_PORT = "1880"
   ```

3. **Adjust Settings**
   In `src/config/settings.py`, enable/disable providers:
   ```python
   # Provider Enablement
   PROVIDER_TELEGRAM_ENABLED = True
   PROVIDER_TWILIO_WHATSAPP_ENABLED = True
   PROVIDER_TWILIO_SMS_ENABLED = True
   PROVIDER_SLACK_ENABLED = True
   PROVIDER_DISCORD_ENABLED = True
   PROVIDER_PUSHOVER_ENABLED = True
   PROVIDER_NODE_RED_ENABLED = True
   PROVIDER_SIMPLE_GET_ENABLED = True

   # LED Configuration
   LED_ENABLED = True
   LED_PATTERNS = {
       'normal': {'pattern': [(0, 300), (1, 300)], 'repetitions': 1},
       'connecting': {'pattern': [(0, 75), (1, 75)], 'repetitions': 1},
       'sending': {'pattern': [(1, 1000)], 'repetitions': 1}
   }
   ```

4. **Upload to Pico W**
   - Using Thonny: Open files and "Save as" to Pico W
   - Using mpremote:
     ```bash
     mpremote cp -r src/ :
     ```

## Configuration Details
- **WiFi**: Single connection shared among all providers
- **LED Patterns**: 
  - Normal: 300ms on/off
  - Connecting: 75ms on/off
  - Sending: Solid on
- **Providers**:
  - Each can be independently enabled/disabled
  - Separate configuration in settings
  - Individual error handling
  - Multiple recipients where supported

## Usage
1. **Power Up**
   - Connect Pico W to power
   - LED starts heartbeat pattern if enabled

2. **Operation States**
   - **Normal**: Regular LED heartbeat with "Alive" messages
   - **Doorbell Press**: 
     1. LED changes to connection pattern
     2. WiFi connects
     3. LED goes solid
     4. Notifications sent
     5. WiFi disconnects
     6. Returns to normal heartbeat

3. **Monitoring**
   - Enable `SERIAL_LOGS = True` for detailed operation logs
   - Each provider reports success/failure
   - Network status is logged

4. **LED States**
   ```
   Normal:     ▁▁▁▁▆▆▆▆▁▁▁▁▆▆▆▆▁▁▁▁▆▆▆▆▁▁▁▁▆▆▆▆
   Connecting: ▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆▁▆
   Sending:    ▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆
   ```

## Troubleshooting
- **No LED**: Check `LED_ENABLED` in settings
- **No Notifications**: Verify provider credentials and enable flags
- **WiFi Issues**: Check network credentials and connection timeout
- **Provider Errors**: Enable logging and check specific provider messages

## Memory Management
- Enable only needed providers
- Providers are loaded only if enabled
- Single network connection for all notifications
- Resources cleaned up after each notification

## Limitations and Improvements
- **Async but Not Interrupt-Based**: Uses polling for doorbell
- **Single WiFi Network**: No failover or multiple networks
- **Memory Constraints**: Enable only necessary providers
- **Network Dependency**: All providers require internet

## Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Follow code style
4. Tests your code
5. Submit pull request

## License
MIT License - see [license](./LICENSE)

## Support
- Open issues on GitHub
- Enable logging for troubleshooting
- Check provider documentation for specific issues
