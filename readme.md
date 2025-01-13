# Raspberry Pi Pico W Doorbell Extension (v2)

## Overview
This **Raspberry Pi Pico W** project extends a traditional doorbell to send notifications asynchronously via **Telegram** and **Node-RED**. It uses **uasyncio** for non-blocking tasks, ensuring the doorbell is monitored continuously while handling network operations efficiently. The system connects to Wi-Fi only when needed, preserving power and bandwidth.

## Features
- **Doorbell Signal Monitoring**: Detects doorbell button presses and sends notifications.
- **Asynchronous Design**: Utilizes `uasyncio` for concurrent LED heartbeats and pin monitoring without blocking.
- **Notifications**:
  - **Telegram**: Sends messages to configured chat IDs via a bot token.
  - **Node-RED**: Triggers HTTP GET requests to a Node-RED flow for further processing or automation.
- **LED Heartbeat**: Onboard LED simulates a “heartbeat” pattern to indicate the system is running.
- **Power-Efficient Networking**: Connects to Wi-Fi only when sending notifications, then disconnects.

## Pre-Setup
1. **Telegram Bot**  
   - Create a Telegram bot via [BotFather](https://core.telegram.org/bots#6-botfather).  
   - Retrieve the Bot Token and Chat IDs.
2. **Node-RED Flow**  
   - Set up a Node-RED flow with an **HTTP In** node listening on the path you specify (default: `/timbre`).
   - Connect it to a **Debug** or other nodes to handle the received `payload`.
3. **Credentials**  
   - Fill in `src/config/credentials.py` with your actual Wi-Fi SSID/password, Telegram token, chat IDs, and Node-RED server details.

## Hardware Setup

> **Note**: The core wiring for the doorbell input pin is similar to a pull-up configuration, with the doorbell line pulled to ground when pressed.

Example circuit

```
    +------------------+
    |          (signal)|        (2.2k)
    |             GP21 +--------/\/\/\--------------------------- Signal (+)
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


1. **GP21** is configured as the doorbell pin (adjust if needed in `settings.
   py`).
2. **LED** can be the onboard LED, referenced as `"LED"` in code.
3. **Power** the Raspberry Pi Pico W via USB or another stable 5V-3.3V supply.

## Software Components
- **`main.py`**  
  Entry point; starts `uasyncio` tasks for doorbell monitoring and LED heartbeat.
- **`config/credentials.py`** & **`config/settings.py`**  
  Store sensitive credentials and general configuration.
- **`core/doorbell.py`**  
  Monitors the doorbell pin, logs activity, triggers notifications.
- **`core/heart_led.py`**  
  Runs a simple heartbeat pattern on the onboard LED.
- **`core/network.py`**  
  Manages Wi-Fi connectivity (connect/disconnect).
- **`notifications/providers`**  
  Houses specific notification providers (e.g., `telegram_provider.py`, `node_red_provider.py`), each implementing `NotificationProvider`.
- **`notifications/factory.py`** & **`notifications/notifier.py`**  
  - `factory.py` selects which providers to enable based on `settings.ENABLED_PROVIDERS`.  
  - `notifier.py` orchestrates sending messages to all active providers.
- **`utils/logging.py`**  
  Minimal logger respecting `SERIAL_LOGS` from `settings.py`.

## Installation
1. **Clone the repository** or download the project folder.
2. **Update Credentials**  
   - In `src/config/credentials.py`, set:
     - `WIFI_SSID` and `WIFI_PASS`
     - `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_IDS`
     - `NODE_RED_HOST`, `NODE_RED_PORT`, `NODE_RED_PATH`
3. **Adjust Settings**  
   - In `src/config/settings.py`, confirm `ENABLED_PROVIDERS` includes the services you want: `['telegram', 'node_red']`.
4. **Copy files** to your Raspberry Pi Pico W via `mpremote`, `Thonny`, or another method.

## Configuration
- **Wi-Fi**: The system connects to the network using `network.py` whenever a notification is needed.
- **Notification Providers**:
  - **Telegram**: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_IDS` must be valid.
  - **Node-RED**: `NODE_RED_CONFIG` should match your Node-RED server IP/port/path.
- **LED & Doorbell Pins**:
  - Change `LED_PIN` (`"LED"`) or `DOORBELL_PIN` (`10`) in `settings.py` if you use different pins.

## Usage
1. **Power on** the Raspberry Pi Pico W (USB or external 5V supply).
2. The system will attempt to connect to Wi-Fi (see console output if `SERIAL_LOGS` is `True`).
3. **Heartbeat**:
   - The onboard LED will blink in a recurring pattern, indicating the device is running.
4. **When the doorbell is pressed**:
   - `Doorbell` logs “Doorbell pressed”.
   - LED turns off briefly.
   - A notification is sent to the enabled providers (Telegram, Node-RED, or both).
5. **Node-RED**:
   - The request is made to `http://<NODE_RED_HOST>:<NODE_RED_PORT>/<NODE_RED_PATH>?payload=Doorbell pressed`.
6. **Telegram**:
   - Messages are sent to each `TELEGRAM_CHAT_IDS` via your bot token.

![chat](./assets/chat.png)

## Limitations and Improvements
- **Asynchronous but not interrupt-based**: The doorbell uses a polling approach in an async loop. Future improvements might integrate interrupts for faster response.
- **Single Wi-Fi SSID**: If you want to handle multiple Wi-Fi networks, you’d extend `credentials.py` or add logic to `network.py`.
- **Memory constraints**: MicroPython on the Pico W has limited RAM. The project’s modular design helps, but keep an eye on memory usage if you add complex features.

## Contributing
Pull requests, issues, and suggestions are welcome! Please ensure your changes align with best practices for MicroPython and embedded devices.

## License
This project is licensed under the MIT License — see [licence.txt](./licence.txt) for details.
