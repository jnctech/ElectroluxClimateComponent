# CLAUDE.md - AI Assistant Guide for ElectroluxClimateComponent

## Project Overview

**ElectroluxClimateComponent** is a Home Assistant custom component for controlling Electrolux air conditioners via the Broadlink protocol. It enables local network control of Electrolux AC units through Home Assistant's climate integration.

- **Domain:** `electrolux_climate`
- **Version:** 0.0.2
- **License:** Apache 2.0
- **IoT Class:** local_polling (5-second update interval)
- **Primary Dependency:** `broadlink==0.19.0`

## Repository Structure

```
ElectroluxClimateComponent/
├── custom_components/electrolux_climate/
│   ├── __init__.py          # Component entry point, config entry setup/migration
│   ├── climate.py           # Climate entity (HVAC modes, fan, swing, temperature)
│   ├── switch.py            # LED display switch entity
│   ├── config_flow.py       # Home Assistant config flow UI wizard
│   ├── const.py             # Constants (domain, temperatures, platforms)
│   ├── electrolux.py        # Core device protocol implementation
│   ├── manifest.json        # Component metadata and DHCP discovery config
│   ├── strings.json         # Config flow localization strings
│   └── translations/
│       └── en.json          # English UI translations
├── .gitignore               # Standard Python gitignore (pycache, venv, etc.)
├── README.md                # Basic project description
├── info.md                  # Additional project info
├── requirements.txt         # Python dependencies (broadlink==0.19.0)
├── hacs.json                # HACS integration metadata
└── LICENSE                  # Apache 2.0 license
```

## Git Configuration

### .gitignore
Standard Python `.gitignore` covering:
- **Bytecode:** `__pycache__/`, `*.py[cod]`, `*.so`
- **Packaging:** `build/`, `dist/`, `*.egg-info/`, `wheels/`
- **Testing:** `.pytest_cache/`, `.coverage`, `htmlcov/`, `.tox/`
- **Environments:** `.env`, `.venv`, `venv/`, `env/`
- **IDE/Tools:** `.mypy_cache/`, `.DS_Store`, `.ropeproject/`

### Branch Naming
- Feature branches: `feature/<description>`
- Bug fixes: `fix/<description>`
- AI assistant branches: `claude/<description>-<session-id>`

## Key Files and Their Purposes

### electrolux.py - Device Protocol
The core communication layer with Electrolux devices via Broadlink protocol.

- **Class:** `electrolux(Device)` extending `broadlink.Device`
- **Device Type:** `0x4f9b`
- **Enums:** `mode` (AUTO, COOL, HEAT, DRY, FAN, HEAT_8) and `fan` (AUTO, LOW, MID, HIGH, TURBO, QUIET)
- **Key Methods:**
  - `get_status()` - Returns device state as JSON
  - `set_temp(temp)` - Set target temperature (0-40°C)
  - `set_power(power_on)` - Turn device on/off
  - `set_mode(mode)` - Set operation mode
  - `set_fan(fan)` - Set fan speed
  - `set_swing(swing_on)` - Control vertical air direction
  - `set_led(led_on)` - Control LED display

### climate.py - Climate Entity
Home Assistant climate platform integration.

- **Class:** `ElectroluxClimateEntity(ClimateEntity)`
- **HVAC Modes:** OFF, AUTO, HEAT, COOL, DRY, FAN_ONLY, HEAT_COOL
- **Fan Modes:** AUTO, LOW, MEDIUM, HIGH, QUIET, TURBO
- **Swing Modes:** OFF, VERTICAL
- **Temperature:** 1°C precision, configurable min/max range

### switch.py - LED Switch Entity
Simple switch for controlling the AC's LED display.

### config_flow.py - Configuration Wizard
Multi-step configuration flow supporting:
- DHCP auto-discovery (recognizes 8 MAC address prefixes)
- Manual IP entry
- Temperature range configuration

### const.py - Constants
```python
DOMAIN = "electrolux_climate"
MIN_TEMP = 0
MAX_TEMP = 40
DEFAULT_MIN = 17
DEFAULT_MAX = 30
SCAN_INTERVAL = timedelta(seconds=5)
```

## Development Commands

### Installation for Development
```bash
# Clone to Home Assistant custom components directory
cp -r custom_components/electrolux_climate ~/.homeassistant/custom_components/

# Restart Home Assistant
ha core restart
```

### Dependencies
```bash
pip install broadlink==0.19.0
```

### Git Operations
```bash
# Standard commit workflow
git add <files>
git commit -m "Description of changes"
git push origin <branch>
```

## Code Conventions

### Python Style
- **Async/Await:** All Home Assistant lifecycle methods use `async def`
- **Type Hints:** Used throughout with `import typing as t`
- **Blocking Calls:** Wrapped with `async_add_executor_job()` for Broadlink operations

### Home Assistant Patterns
- Config entries use versioning for migrations (currently v2)
- Unique IDs based on device MAC address
- Device info registered for Home Assistant device registry
- Platform setup via `async_forward_entry_setups()`

### Mode Conversion Pattern
The codebase converts between device modes and Home Assistant modes using `match/case`:
```python
match mode:
    case HVACMode.OFF:
        return None
    case HVACMode.AUTO:
        return electrolux.mode.AUTO
    # ... etc
```

## Device Communication Protocol

### Packet Structure
- **Header:** Magic bytes `0xa5a55a5a` at offset 0x02
- **Checksum:** 16-bit at offset 0x06-0x07
- **Payload:** JSON commands (e.g., `{"temp":24}`)

### Command IDs
| ID   | Purpose                          |
|------|----------------------------------|
| 0x0e | Get status                       |
| 0x17 | Set temperature                  |
| 0x18 | Set power/sleep/self-clean       |
| 0x19 | Set mode/fan/swing/LED           |
| 0x1f | Set timer                        |

### Status JSON Fields
| Field     | Description                                    |
|-----------|------------------------------------------------|
| `sn`      | Serial number                                  |
| `ac_pwr`  | Power state (0=off, 1=on)                      |
| `envtemp` | Current room temperature                       |
| `temp`    | Target temperature                             |
| `ac_mode` | Mode (0=COOL, 1=HEAT, 2=DRY, 3=FAN, 4=AUTO)    |
| `ac_mark` | Fan (0=AUTO, 1=LOW, 2=MID, 3=HIGH, 4=TURBO, 5=QUIET) |
| `ac_vdir` | Swing (0=off, 1=on)                            |
| `scrdisp` | LED display (0=off, 1=on)                      |

## Supported Devices

DHCP discovery recognizes these Broadlink MAC prefixes:
- 34EA34*, 24DFA7*, A043B0*, B4430D*
- C8F742*, E81656*, E87072*, EC0BAE*

## Important Implementation Notes

### Serial Number Handling
Devices may not always have a serial number in the status JSON. The code falls back to MAC address if `sn` is unavailable (see `climate.py:212`).

### Error Handling
The codebase handles these exceptions:
- `NetworkTimeoutError` - Device discovery timeouts
- `OSError` with errno checking - Network issues
- `AuthenticationError` - Broadlink auth failures
- `BroadlinkException` - General device errors
- `ConfigEntryNotReady` - Temporary setup failures

### Config Entry Migration
Version 1 to 2 migration converts:
- `ip` field to `CONF_HOST`
- Base64-encoded MAC to hex format
- Adds temperature min/max defaults

## Testing Considerations

- Requires physical Electrolux AC with Broadlink-compatible module
- Device must be on local network (no cloud dependency)
- MAC address must match known prefixes or use manual setup
- 5-second polling interval for status updates

## Extension Points

Potential areas for future development:
- Additional switch entities (sleep mode, self-clean)
- Climate entity feature expansion
- Support for additional device types
- Improved error recovery and reconnection logic

## Common Tasks

### Adding a New Device Feature
1. Add command method in `electrolux.py`
2. Expose in `climate.py` or create new entity
3. Update `const.py` if new constants needed
4. Add translations in `strings.json` and `translations/en.json`

### Debugging Device Communication
1. Enable Home Assistant debug logging for `electrolux_climate`
2. Check `get_status()` JSON response
3. Verify checksum calculations in `_send()` method

### Updating Broadlink Library
1. Update version in `requirements.txt` and `manifest.json`
2. Test device discovery and communication
3. Verify protocol compatibility
