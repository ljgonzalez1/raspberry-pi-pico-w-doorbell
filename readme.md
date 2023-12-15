# Raspberry Pi Pico Doorbell Extension

## Overview
This Raspberry Pi Pico project extends a traditional doorbell, enabling it to send notifications via Telegram and Node-RED when the doorbell button is pressed. It's ideal for those instances where you might not hear the doorbell. The system is designed to connect to the network only when necessary, minimizing its online presence.

## Features
- **Doorbell Signal Monitoring:** Detects doorbell button presses and sends notifications.
- **Notification Services:** Integrates with Telegram and Node-RED for sending alerts.
- **LED Indicator:** An onboard LED indicates that the board is functioning correctly and not stuck in a loop.
- **Power-Efficient Networking:** Connects to the network only as needed to send messages, although it reconnects for each message.

## Pre-Setup
Before installation, create a Telegram bot following [this tutorial](https://core.telegram.org/bots#6-botfather) to obtain your bot token and chat IDs.

## Hardware Setup
The circuit includes a Raspberry Pi Pico board with a voltage divider to ensure it receives an ideal voltage between 3V and 5V.

### Circuit Diagram

```
+------------------+
|          (signal)|        (2.2k)
|             GP10 +--------/\/\/\------------------ Signal (+)
| Raspberry        |
| Pi        (~3.3V)|
| Pico W      VSYS +--------/\/\/\-----------+------ VCC
|                  |                         |
|              GND +----------+----/\/\/\----+
|      |LED|       |          |
+------+---+-------+        --+--
                             ---
```


## Software Components
The software consists of several Python modules, each handling a specific aspect of the project.

## Installation
1. Clone the repository to your local machine.
2. Update `credentials.py` with your WiFi and Telegram information.
3. Modify `settings.py` to fit your needs (e.g., enabling Telegram or Node-RED).
4. Upload all files to your Raspberry Pi Pico.

## Configuration
Modify `settings.py` and `credentials.py` to match your network and notification preferences.

## Usage
After powering up, the Pi Pico monitors the doorbell pin. Pressing the doorbell triggers the sending of notifications to the configured channels.

![chat](./assets/chat.png)

## Limitations and Improvements
- Uses single-core polling for button press detection; interrupts were considered but not implemented.
- Network efficiency is limited as it reconnects for each message sent.
- Future versions might explore using interrupts for improved efficiency.

## Contributing
Contributions, suggestions, and improvements are welcome. Please feel free to open issues or pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

