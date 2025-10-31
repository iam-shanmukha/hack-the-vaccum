# Eureka Forbes LVAC Voice Pro Vacuum Cleaner - Reverse Engineering Project

A comprehensive toolkit for controlling and reverse engineering the Eureka Forbes LVAC Voice Pro vacuum cleaner robot using the Tuya IoT protocol.

## Project Overview

This project provides local control over the Eureka Forbes LVAC Voice Pro vacuum cleaner without relying on cloud services. It includes tools for:

- Full vacuum control (start/stop, modes, scheduling)
- Map data extraction and visualization
- Real-time status monitoring
- Protocol analysis and debugging

## Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

Required Python packages:
- `tinytuya` - Tuya device communication
- `matplotlib` - Map visualization
- `numpy` - Data processing

### Basic Usage

**Control your vacuum:**
```bash
python control/vacuum_controller.py
```

This launches an interactive menu where you can:
1. View vacuum status
2. Start/stop cleaning
3. Return to dock
4. Adjust suction modes
5. Set water levels
6. And more...

## Project Structure

```
banthi-decoder/
├── control/           # Vacuum control scripts
│   ├── vacuum_controller.py      # Main controller (RECOMMENDED)
│   └── vacuum_controller_v1.py   # Earlier version
│
├── discovery/         # Device discovery tools
│   ├── tuyatest.py               # Network scanner for Tuya devices
│   ├── tuya_get_local.py         # Cloud API connector
│   └── vaccumpy.py               # UDP broadcast listener
│
├── mapping/           # Map extraction and visualization
│   ├── banthi_get_map.py         # Advanced map retrieval
│   ├── decode_map.py             # Base64 map decoder
│   ├── visualize_map.py          # Path visualization
│   ├── map_visualizer_v2.py      # Room boundary visualization
│   ├── tuya_decoder.py           # Generic Tuya map decoder
│   ├── live_map.py               # Real-time map monitoring
│   └── vaccum_map_test.py        # Cloud map API tests
│
├── utils/             # Utility scripts
│   └── banthi_dps_mapping.py     # DPS discovery tool
│
├── data/              # Sample data and captures
│   ├── tinytuya.json             # Device credentials
│   ├── map_coords.json           # Extracted coordinates
│   ├── map_decoded.json          # Decoded map data
│   ├── *.pcap                    # Network captures
│   └── *.png                     # Map visualizations
│
├── docs/              # Documentation
│   ├── SETUP_GUIDE.md            # Step-by-step setup
│   └── PROTOCOL.md               # Protocol documentation
│
└── raw/               # Original unorganized scripts
```

## Step-by-Step Guides

### 1. Initial Setup

See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed instructions on:
- Getting device credentials
- Network configuration
- First connection

### 2. Controlling Your Vacuum

**Run the main controller:**
```bash
python control/vacuum_controller.py
```

Available commands:
- Start/stop cleaning
- Return to charging dock
- Set suction mode (gentle/normal/max)
- Set water level (low/medium/high)
- Find robot (beep)
- Toggle Do Not Disturb mode
- Toggle auto carpet boost
- View maintenance status

### 3. Extracting Map Data

**Option A: Request map from vacuum**
```bash
python mapping/banthi_get_map.py
# Choose option 1 or 2
```

**Option B: Monitor live map updates**
```bash
python mapping/live_map.py
# Choose option 3 for real-time monitoring
```

**Option C: Decode existing map data**
```bash
python mapping/map_visualizer_v2.py
```

### 4. Device Discovery

If you don't have your device credentials:

```bash
# Scan network for Tuya devices
python discovery/tuyatest.py

# Or listen for UDP broadcasts
python discovery/vaccumpy.py
```

## Device Configuration

Edit `data/tinytuya.json` with your device details:

```json
{
    "apiKey": "your_api_key",
    "apiSecret": "your_api_secret",
    "apiRegion": "in",
    "apiDeviceID": "your_device_id"
}
```

Or hardcode in the scripts:
```python
DEVICE_ID = "your_device_id"
IP_ADDRESS = "192.168.x.x"
LOCAL_KEY = "your_local_key"
```

## Key Features by Script

### Control Scripts

**vacuum_controller.py** (CURRENT VERSION)
- Complete vacuum control
- Interactive menu
- Status monitoring
- Maintenance tracking
- Battery levels
- Error codes

### Mapping Scripts

**banthi_get_map.py**
- Request full map data
- Monitor for map updates
- Multiple format detection (PNG, JSON, binary)
- Automatic decoding

**map_visualizer_v2.py**
- Decode room boundaries
- Visualize floor plan
- Calculate room areas
- Export to JSON

**live_map.py**
- Real-time monitoring
- Live path visualization
- Status overlay

### Discovery Scripts

**tuyatest.py**
- Scan local network
- Detect Tuya devices
- Show device versions

**vaccumpy.py**
- Listen for broadcasts
- Packet analysis
- Protocol debugging

### Utilities

**banthi_dps_mapping.py**
- Test DPS values
- Discover new commands
- Protocol exploration

## Tuya DPS (Data Point) Reference

| DPS | Function | Values |
|-----|----------|--------|
| 1   | Power | true/false |
| 2   | Pause | true/false |
| 4   | Command | 'chargego', etc |
| 5   | Status | Various states |
| 7   | Side Brush Life | 0-100% |
| 8   | Filter Life | 0-100% |
| 9   | Suction Mode | 'gentle', 'normal', 'max' |
| 10  | Water Level | 'low', 'medium', 'high' |
| 15  | Map Data | Base64 encoded |
| 17  | Cleaning Time | Seconds |
| 21  | Cleaning Area | Square meters |
| 25  | Find Robot | true/false (beep) |
| 26  | Battery | 0-100% |
| 27  | DND Mode | true/false |
| 29  | Main Brush Life | Cycles remaining |
| 30  | Total Cleanings | Count |
| 31  | Total Area | Square meters |
| 102 | Error Code | Integer |
| 103 | Auto Boost | true/false |
| 121 | Map Request | 'get_map', 'get_path', 'get_both' |
| 199 | Map ID | String |

See [docs/PROTOCOL.md](docs/PROTOCOL.md) for complete protocol documentation.

## Troubleshooting

### Connection Issues
- Ensure vacuum is on the same WiFi network
- Check IP address hasn't changed
- Verify local key is correct
- Try restarting the vacuum

### Map Not Loading
- Request map while vacuum is active
- Check DPS 15 for map data
- Try different request types ('get_map', 'get_both')
- Monitor with `live_map.py`

### Command Not Working
- Check vacuum status first
- Ensure vacuum is not in error state
- Verify DPS values in `utils/banthi_dps_mapping.py`
- Check battery level

## Protocol Details

The vacuum uses Tuya Protocol version 3.3 over local network:
- Port: 6668 (TCP)
- Broadcast: 6667 (UDP)
- Encryption: AES with local key
- Format: JSON over encrypted payload

Map data format:
- Base64 encoded binary
- Header: Magic bytes (0xAA00) + version
- Payload: Coordinate pairs (int16) for room boundaries
- Optional compression (zlib/gzip)

## Security Notes

This project is for educational and personal use. Keep your credentials secure:
- Never commit API keys to version control
- Use environment variables for sensitive data
- Local key provides full device access

## Contributing

This is a reverse engineering research project. Contributions welcome:
- New DPS discoveries
- Protocol insights
- Additional features
- Bug fixes

## License

Educational and personal use only.

## Acknowledgments

- TinyTuya library for Tuya protocol implementation
- Tuya IoT Platform for device API
- Community reverse engineering efforts

## Further Reading

- [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Complete setup walkthrough
- [docs/PROTOCOL.md](docs/PROTOCOL.md) - Detailed protocol analysis
- [TinyTuya Documentation](https://github.com/jasonacox/tinytuya)
- [Tuya IoT Platform](https://iot.tuya.com/)

## Support

For issues or questions:
1. Check existing documentation
2. Review troubleshooting section
3. Examine network captures in `data/`
4. Test with DPS mapping tools
