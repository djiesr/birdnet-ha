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
- **Comprehensive YAML package** with additional sensors, automations, and templates

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

## Package Installation

This integration includes a comprehensive YAML package that provides additional sensors, automations, and templates for enhanced functionality.

### Package Features

- **Template sensors** for trends and statistics
- **Automations** for notifications and data management
- **REST sensors** for historical data
- **Media player integration** for audio playback
- **Input select** for species selection

### Installing the Package

1. Download the `packages/birdnet-pi-package.yaml` file
2. Replace `{{ birdnet_pi_ip }}` with your BirdNET-Pi device IP address
3. Copy the file to your Home Assistant `config/packages/` directory
4. Add the following to your `configuration.yaml`:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

5. Restart Home Assistant

### Package Configuration

Before using the package, make sure to:

1. **Replace the IP address**: Edit the package file and replace all instances of `{{ birdnet_pi_ip }}` with your actual BirdNET-Pi device IP address
2. **Configure media players**: Update the `media_player.living_room_speaker` reference in the package with your actual media player entity
3. **Adjust notification settings**: Modify the notification entity in automations to match your setup

### Package Components

The package includes:

- **Template sensors** for timeline data, trends, and statistics
- **REST sensors** for daily, weekly, monthly, and yearly statistics
- **Automations** for species selection updates and notifications
- **Scripts** for audio playback
- **Media player** configuration for audio output

## Available Entities

### Sensors
- Latest detections
- Total detections today
- Number of species detected today
- List of species detected today
- Daily statistics

### Binary Sensors
- Server connection status

### Package Sensors

The package adds additional sensors for:
- Historical trends (daily, weekly, monthly, yearly)
- Hourly detection counts
- Top 10 species rankings
- Statistical summaries

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

## Acknowledgments

- [BirdNET-Pi](https://github.com/mcguirepr89/BirdNET-Pi) - The original BirdNET-Pi project
- [Home Assistant](https://www.home-assistant.io/) - The home automation platform
- [HACS](https://hacs.xyz/) - Home Assistant Community Store

## Changelog

### Version 0.1.0
- Initial release
- Basic sensor integration
- Multi-language support (English/French)
- Comprehensive YAML package
- Audio playback functionality