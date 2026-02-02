# Electrolux Climate Component

Custom Home Assistant integration for local control of Electrolux and Kelvinator air conditioners via Broadlink protocol.

## Features

- 🌡️ Full climate control (temperature, modes, fan speed)
- 🔄 Swing control (vertical air direction)
- 💡 LED display control
- 🔍 Automatic DHCP device discovery
- 📱 Home Assistant UI configuration
- 🏠 Local polling (no cloud required)

## Supported Devices

Compatible with Electrolux air conditioners using Broadlink protocol (device type 0x4f9b):
- Electrolux air conditioners with Broadlink modules
- Kelvinator models (e.g., KSV25HWH)
- Supported MAC address prefixes: 34EA34*, 24DFA7*, A043B0*, B4430D*, C8F742*, E81656*, E87072*, EC0BAE*

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Click "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add: `https://github.com/jnctech/ElectroluxClimateComponent`
6. Category: Integration
7. Click "Install"
8. Restart Home Assistant

### Manual Installation

1. Download the latest release
2. Copy `custom_components/electrolux_climate` to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Electrolux Climate"
4. The integration will automatically discover devices on your network via DHCP
5. Follow the configuration wizard to:
   - Confirm device selection
   - Set device name
   - Configure temperature range (default: 17-30°C)

## Entities Created

For each device, the integration creates:
- **Climate entity** - Full HVAC control
- **Switch entity** - LED display control

## HVAC Modes

- **Off** - Turn device off
- **Cool** - Cooling mode
- **Heat** - Heating mode
- **Dry** - Dehumidification mode
- **Fan Only** - Circulation without cooling/heating
- **Auto** - Automatic temperature control

## Fan Speeds

- Auto
- Low
- Medium
- High
- Turbo
- Quiet

## Troubleshooting

### Device Not Discovered

- Ensure device is on the same network as Home Assistant
- Check that device MAC address matches supported prefixes
- Try manual IP entry in configuration wizard

### LED Switch Not Created

- Some device models (e.g., Kelvinator KSV25HWH) don't provide serial numbers
- Fixed in version 0.0.3+ with MAC address fallback
- Update to latest version if experiencing this issue

### Connection Timeout

- Verify device is powered on and connected to network
- Check firewall rules allow local network communication
- Ensure Broadlink device is authenticated

## Device Communication

This integration uses local network communication via the Broadlink protocol:
- **Protocol:** Broadlink device type 0x4f9b
- **Update interval:** 5 seconds
- **IoT Class:** Local polling (no cloud dependency)

## Contributing

Issues and pull requests are welcome!

- **Report bugs:** [GitHub Issues](https://github.com/jnctech/ElectroluxClimateComponent/issues)
- **Feature requests:** [GitHub Discussions](https://github.com/jnctech/ElectroluxClimateComponent/discussions)

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details

## Credits

Original development by [@DotEfekts](https://github.com/DotEfekts)
