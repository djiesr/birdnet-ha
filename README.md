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

## Dashboard

This integration includes a comprehensive dashboard template that provides a beautiful and functional interface for monitoring your BirdNET-Pi data.

### Dashboard Features

The dashboard is organized into four main views:

#### 1. **Oiseaux** (Birds) - Main View
- **Latest Detection**: Shows the most recent bird detection with photo and audio player
- **Quick Statistics**: Displays detections, species count, activity status, and hourly detections
- **Daily Trends**: 7-day graph showing detections and species counts
- **Hourly Activity**: Real-time chart of detections by hour for the current day
- **Detection Statistics**: Detailed breakdown by time period (today, week, month, year)
- **Top Species**: Auto-generated list of the most detected species today

#### 2. **Analyses** (Analysis) - Advanced Analytics
- **Period Comparison**: Side-by-side comparison of daily, weekly, and monthly data
- **Hourly Activity Chart**: Detailed hourly breakdown with data labels
- **Species Selection**: Interactive dropdown to select and analyze specific species
- **Species Details**: Shows scientific name, confidence level, and last detection time
- **Species Timeline**: 30-day chart showing detection patterns for selected species

#### 3. **Statistiques** (Statistics) - Historical Data
- **Detection Evolution**: 90-day trend analysis with stacked charts
- **Daily Comparisons**: Side-by-side graphs for daily detections and species counts
- **Top 10 Species**: Pie chart showing the most detected species overall
- **Statistical Summary**: Comprehensive overview of all time periods

#### 4. **Liste des Espèces** (Species List) - Complete Inventory
- **All Detected Species**: Complete list of all species with detection counts
- **Species Details**: Popup with scientific names and detection statistics
- **Sortable List**: Species sorted by detection frequency

### Dashboard Installation

#### Prerequisites

Install the following HACS frontend modules:

```bash
# Required HACS Frontend Modules
- ApexCharts Card (custom:apexcharts-card)
- Mushroom Cards (custom:mushroom-chips-card)
- Mini Graph Card (custom:mini-graph-card)
- Auto Entities (custom:auto-entities)
- Mushroom Template Card (custom:mushroom-template-card)
- Multiple Entity Row (custom:multiple-entity-row)
- Browser Mod (browser_mod)
```

#### Installation Steps

1. **Download the dashboard file**:
   - Copy `packages/birdnet-dashboard.yaml` to your Home Assistant configuration

2. **Update the IP address**:
   - Replace `{{ birdnet_pi_ip }}` with your BirdNET-Pi device IP address in the dashboard file

3. **Create image directory** (optional):
   ```bash
   # Create directory for bird images
   mkdir -p config/www/images/birds/
   ```

4. **Add to your configuration**:
   ```yaml
   # In your configuration.yaml or dashboard configuration
   views: !include packages/birdnet-dashboard.yaml
   ```

5. **Restart Home Assistant**

### Dashboard Customization

#### Image Setup
- Place bird images in `config/www/images/birds/`
- Use the format: `species_name.jpg` (e.g., `merle_damerique.jpg`)
- Images should be in JPG format for best compatibility

#### Audio Configuration
- The dashboard includes audio players for bird calls
- Audio files are streamed directly from your BirdNET-Pi device at `http://{{ birdnet_pi_ip }}:5000/api/audio/`
- Ensure your BirdNET-Pi device is accessible on the network

#### Color Themes
- The dashboard uses Home Assistant's CSS variables for theming
- Colors automatically adapt to your current theme
- Custom colors can be modified in the dashboard configuration

### Dashboard Features

#### Real-time Updates
- All charts and statistics update automatically
- Data refreshes based on your BirdNET-Pi update interval
- Historical data is preserved and displayed in trends

#### Interactive Elements
- Click on species to view detailed information
- Audio playback for bird calls
- Expandable statistics sections
- Responsive design for mobile devices

#### Data Visualization
- Multiple chart types (line, bar, area, pie)
- Color-coded data for easy interpretation
- Zoom and pan capabilities on charts
- Export functionality for data analysis

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