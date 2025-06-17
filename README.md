# BirdNET-Pi Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![maintainer](https://img.shields.io/badge/maintainer-%40djiesr-blue.svg)](https://github.com/djiesr)
[![fr](https://img.shields.io/badge/lang-fr-yellow.svg)](https://github.com/djiesr/birdnet-ha/blob/main/README.md)

This Home Assistant integration allows you to connect your BirdNET-Pi instance to Home Assistant, providing real-time bird detection monitoring and statistics.

## Features

- Real-time bird detection monitoring
- Daily species detection statistics
- Total detections count per day
- List of detected species
- Server connection status
- Customizable update interval

## Prerequisites

- A working BirdNET-Pi instance (see [BirdNET-Pi](https://github.com/mcguirepr89/BirdNET-Pi))
- Home Assistant version 2023.8.0 or higher
- HACS (optional, but recommended for installation)

## Installation

### Method 1: Via HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed
2. In HACS, go to "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add `https://github.com/djiesr/birdnet-ha`
6. Search for "BirdNET-Pi" in HACS
7. Click "Download"

### Method 2: Manual Installation

1. Download this repository
2. Copy the `birdnet-pi` folder to your `custom_components` folder
3. Restart Home Assistant

## Configuration

1. In Home Assistant, go to "Settings" > "Devices & Services"
2. Click "Add Integration"
3. Search for "BirdNET-Pi"
4. Enter your BirdNET-Pi server's IP address and port
5. Configure the update interval according to your needs

## Available Entities

### Sensors
- Latest detections
- Total detections today
- Number of species detected today
- List of species detected today
- Daily statistics

### Binary Sensors
- Server connection status

## Customization

You can customize the update interval in the integration options:
1. Go to "Settings" > "Devices & Services"
2. Find the BirdNET-Pi integration
3. Click "Configure"
4. Adjust the update interval according to your needs

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Verify that your BirdNET-Pi server is accessible
- Make sure the ports are correctly configured

## Contributing

Contributions are welcome! Feel free to:
- Open an issue to report a bug
- Submit a pull request to improve the integration
- Improve the documentation

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.