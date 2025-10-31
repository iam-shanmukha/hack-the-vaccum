# Tuya Protocol - Eureka Forbes LVAC Voice Pro Reverse Engineering

## Overview

The Eureka Forbes LVAC Voice Pro vacuum cleaner uses the Tuya IoT protocol for communication. This document details the reverse-engineered protocol structure, data points, and map formats.

## Table of Contents

1. [Network Protocol](#network-protocol)
2. [DPS (Data Points)](#dps-data-points)
3. [Map Data Format](#map-data-format)
4. [Command Reference](#command-reference)
5. [Status Codes](#status-codes)
6. [Reverse Engineering Methods](#reverse-engineering-methods)

## Network Protocol

### Connection Details

- **Protocol**: Tuya Protocol v3.3
- **Transport**: TCP/IP
- **Control Port**: 6668 (TCP)
- **Broadcast Port**: 6667 (UDP)
- **Encryption**: AES-128 (ECB mode)
- **Encoding**: JSON payload

### Packet Structure

```
┌─────────────────────────────────────────────────────┐
│ Header (16 bytes)                                   │
├─────────────────────────────────────────────────────┤
│ Magic: 0x000055AA (4 bytes)                        │
│ Sequence: uint32 (4 bytes)                         │
│ Command: uint32 (4 bytes)                          │
│ Length: uint32 (4 bytes)                           │
├─────────────────────────────────────────────────────┤
│ Encrypted Payload (variable length)                │
│ - JSON data encrypted with AES                     │
│ - Key: local_key (from device credentials)        │
├─────────────────────────────────────────────────────┤
│ CRC32: uint32 (4 bytes)                            │
│ Footer: 0x0000AA55 (4 bytes)                       │
└─────────────────────────────────────────────────────┘
```

### Example Packet (Hex Dump)

```
0000: 00 00 55 aa 00 00 00 01 00 00 00 07 00 00 00 20  ..U...........
0010: 7b 22 64 70 73 22 3a 7b 22 31 22 3a 74 72 75 65  {"dps":{"1":true
0020: 7d 7d 00 00 00 00 12 34 56 78 00 00 aa 55        }}......4Vx..ąU
```

### UDP Broadcast Format

```
┌─────────────────────────────────────────────────────┐
│ Magic: 0x0000 (2 bytes)                             │
│ Magic: 0x55AA (2 bytes)                             │
├─────────────────────────────────────────────────────┤
│ Payload:                                            │
│ - Device ID                                         │
│ - IP Address                                        │
│ - Active/Idle status                               │
│ - Protocol version                                  │
└─────────────────────────────────────────────────────┘
```

## DPS (Data Points)

DPS (Data Point Specifications) are Tuya's way of addressing device features. Each feature has a unique DPS number.

### Complete DPS Mapping

#### Power and Control

| DPS | Name | Type | Values | Description |
|-----|------|------|--------|-------------|
| 1 | power | boolean | true/false | Main power on/off |
| 2 | pause | boolean | true/false | Pause cleaning |
| 3 | mode | string | 'auto', 'spot', 'edge', 'single' | Cleaning mode |
| 4 | command | string | 'chargego', 'stop', etc | Direct commands |

#### Status Information

| DPS | Name | Type | Values | Description |
|-----|------|------|--------|-------------|
| 5 | status | string | See status codes | Current robot status |
| 26 | battery | integer | 0-100 | Battery percentage |
| 102 | error_code | integer | See error codes | Error status |

#### Cleaning Settings

| DPS | Name | Type | Values | Description |
|-----|------|------|--------|-------------|
| 9 | suction_mode | string | 'gentle', 'normal', 'max' | Fan power level |
| 10 | water_level | string | 'low', 'medium', 'high' | Mop water flow |
| 103 | auto_boost | boolean | true/false | Auto carpet boost |

#### Maintenance

| DPS | Name | Type | Values | Description |
|-----|------|------|--------|-------------|
| 7 | side_brush_life | integer | 0-100 | Side brush % remaining |
| 8 | filter_life | integer | 0-100 | Filter % remaining |
| 29 | main_brush_life | integer | 0-180 | Main brush cycles left |

#### Statistics

| DPS | Name | Type | Values | Description |
|-----|------|------|--------|-------------|
| 17 | cleaning_time | integer | seconds | Current session time |
| 21 | cleaning_area | integer | cm² | Current session area |
| 30 | total_cleanings | integer | count | Lifetime cleaning count |
| 31 | total_area | integer | m² | Lifetime total area |

#### Features

| DPS | Name | Type | Values | Description |
|-----|------|------|--------|-------------|
| 25 | find_robot | boolean | true/false | Make beeping sound |
| 27 | dnd_mode | boolean | true/false | Do Not Disturb mode |

#### Map Related

| DPS | Name | Type | Values | Description |
|-----|------|------|--------|-------------|
| 15 | map_data | string | base64 | Current map data |
| 106 | map_request | string | 'get_map', 'get_path' | Request map update |
| 121 | request | string | 'get_both', 'get_map' | Alternative map request |
| 122 | request_alt | string | Various | Alternative request |
| 199 | map_id | string | ID | Current map identifier |

### DPS Discovery Process

Testing was done using `utils/banthi_dps_mapping.py`:

```python
# Test range of DPS values
for dps in range(1, 250):
    try:
        value = vacuum.status()['dps'].get(str(dps))
        if value is not None:
            print(f"DPS {dps}: {value}")
    except:
        pass
```

### Command Examples

**Start Cleaning:**
```python
vacuum.set_value('1', True)
```

**Return to Dock:**
```python
vacuum.set_value('4', 'chargego')
```

**Set Suction Mode:**
```python
vacuum.set_value('9', 'max')  # 'gentle', 'normal', 'max'
```

**Request Map:**
```python
vacuum.set_value('121', 'get_both')
```

**Find Robot:**
```python
vacuum.set_value('25', True)
time.sleep(2)
vacuum.set_value('25', False)
```

## Map Data Format

### Overview

Map data is transmitted in DPS 15 as base64-encoded binary data.

### Map Data Structure

```
┌─────────────────────────────────────────────────────┐
│ Header (2-3 bytes)                                  │
├─────────────────────────────────────────────────────┤
│ Magic: 0xAA00 (uint16, little-endian)              │
│ Version: 0x01 (uint8)                               │
├─────────────────────────────────────────────────────┤
│ Room Data (variable length)                         │
├─────────────────────────────────────────────────────┤
│ Each room: 4 coordinate pairs (16 bytes)           │
│   - Corner 1: X (int16), Y (int16)                 │
│   - Corner 2: X (int16), Y (int16)                 │
│   - Corner 3: X (int16), Y (int16)                 │
│   - Corner 4: X (int16), Y (int16)                 │
├─────────────────────────────────────────────────────┤
│ Path Data (optional)                                │
├─────────────────────────────────────────────────────┤
│ Sequence of coordinate pairs                        │
│   - X (int16, little-endian)                       │
│   - Y (int16, little-endian)                       │
└─────────────────────────────────────────────────────┘
```

### Example Map Data

**Base64 encoded:**
```
qgABFxeqAAMpAQAqqgBcGwUABAEWAzIDlQMyA5UB2AEWAdgABAW+ArAHIAKwByAAxAW+AMQABP4q/+UAQP/lAED+vf4q/r0ABP+1/KECivyhAor6Bf+1+gUABADk/vUBrv71Aa7+KgDk/iqQqgACEwATqgADFQEAFg==
```

**Decoded structure:**
```
Offset  Hex        Decoded
0x00    AA 00      Magic bytes
0x02    01         Version 1
0x03    17 17      Room 1 data begins
        AA 00      Section marker
        03 29      Coordinate pair
        01 00
        2A AA
        ...
```

### Coordinate System

- **Units**: Millimeters (mm)
- **Origin**: Charging dock position (0, 0)
- **X-axis**: Left/Right from dock
- **Y-axis**: Forward/Backward from dock
- **Range**: Typically -10000 to +10000 mm (-10m to +10m)

### Room Boundary Format

Rooms are defined by 4 corners forming a rectangle:

```
(x1,y1) ────────── (x2,y1)
   │                  │
   │     Room 1       │
   │                  │
(x1,y2) ────────── (x2,y2)
```

**Decoding algorithm:**
```python
# Read 4 coordinate pairs
coords = []
for i in range(4):
    x = struct.unpack('<h', data[offset:offset+2])[0]
    y = struct.unpack('<h', data[offset+2:offset+4])[0]
    coords.append((x, y))
    offset += 4

# Extract rectangle bounds
xs = [c[0] for c in coords]
ys = [c[1] for c in coords]

if len(set(xs)) == 2 and len(set(ys)) == 2:
    # Valid rectangle
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    room = {
        'bounds': (min_x, min_y, max_x, max_y),
        'width': max_x - min_x,
        'height': max_y - min_y,
        'area_mm2': (max_x - min_x) * (max_y - min_y),
        'area_m2': ((max_x - min_x) * (max_y - min_y)) / 1_000_000
    }
```

### Path Data Format

Cleaning path is a sequence of coordinates:

```
Point 1: (x1, y1)
Point 2: (x2, y2)
Point 3: (x3, y3)
...
Point N: (xn, yn)
```

**Decoding:**
```python
path = []
while offset < len(data) - 3:
    x = struct.unpack('<h', data[offset:offset+2])[0]
    y = struct.unpack('<h', data[offset+2:offset+4])[0]
    if -10000 < x < 10000 and -10000 < y < 10000:
        path.append((x, y))
    offset += 2
```

### Alternative Formats

Some maps may use:

1. **PNG format** - Magic bytes: `89 50 4E 47` (PNG)
2. **Compressed** - Magic bytes: `1F 8B` (gzip)
3. **JSON** - Starts with `{` (0x7B)

Detection:
```python
if data[:8] == b'\x89PNG\r\n\x1a\n':
    format = 'PNG'
elif data[:2] == b'\x1f\x8b':
    format = 'gzip'
elif data[0:1] == b'{':
    format = 'JSON'
else:
    format = 'proprietary'
```

## Command Reference

### Basic Commands

```python
# Power control
vacuum.set_value('1', True)   # Start
vacuum.set_value('1', False)  # Stop

# Pause
vacuum.set_value('2', True)   # Pause
vacuum.set_value('2', False)  # Resume

# Return to dock
vacuum.set_value('4', 'chargego')
```

### Cleaning Modes

```python
# Cleaning mode
vacuum.set_value('3', 'auto')    # Automatic
vacuum.set_value('3', 'spot')    # Spot cleaning
vacuum.set_value('3', 'edge')    # Edge cleaning
vacuum.set_value('3', 'single')  # Single room
```

### Settings

```python
# Suction power
vacuum.set_value('9', 'gentle')  # Quiet
vacuum.set_value('9', 'normal')  # Standard
vacuum.set_value('9', 'max')     # Turbo

# Water level (mopping)
vacuum.set_value('10', 'low')
vacuum.set_value('10', 'medium')
vacuum.set_value('10', 'high')

# Auto boost on carpet
vacuum.set_value('103', True)   # Enable
vacuum.set_value('103', False)  # Disable

# Do Not Disturb
vacuum.set_value('27', True)    # Enable
vacuum.set_value('27', False)   # Disable
```

### Map Requests

```python
# Request map data
vacuum.set_value('121', 'get_map')   # Map only
vacuum.set_value('121', 'get_path')  # Path only
vacuum.set_value('121', 'get_both')  # Both

# Alternative DPS
vacuum.set_value('106', 'get_both')
vacuum.set_value('122', 'get_both')
```

### Special Functions

```python
# Find robot (beep)
vacuum.set_value('25', True)
time.sleep(2)
vacuum.set_value('25', False)

# Reset filter life
vacuum.set_value('8', 100)

# Reset brush life
vacuum.set_value('7', 100)
vacuum.set_value('29', 180)
```

## Status Codes

### Robot Status (DPS 5)

| Value | Description | Meaning |
|-------|-------------|---------|
| `standby` | Standby | Idle, ready for commands |
| `cleaning` | Cleaning | Active cleaning |
| `charging` | Charging | On dock, charging |
| `paused` | Paused | Cleaning paused |
| `goto_charge` | Returning | Going back to dock |
| `locating` | Locating | Find robot active |
| `docking` | Docking | Aligning with dock |
| `full` | Full | Dustbin full |
| `sleep` | Sleep | Low power mode |

### Error Codes (DPS 102)

| Code | Description | Solution |
|------|-------------|----------|
| 0 | No error | Normal operation |
| 1 | Wheel stuck | Check wheels for obstruction |
| 2 | Side brush stuck | Clear side brush |
| 3 | Main brush stuck | Clear main brush |
| 4 | Cliff sensor | Move away from edge |
| 5 | Bumper stuck | Check bumper mechanism |
| 6 | Low battery | Return to dock |
| 7 | Dustbin missing | Install dustbin |
| 8 | Filter dirty | Clean filter |
| 9 | Wheel suspended | Place on floor |
| 10 | Magnetic strip | Trapped by virtual wall |

## Reverse Engineering Methods

### 1. Network Packet Capture

**Tools used:**
- Wireshark
- tcpdump
- tshark

**Capture filter:**
```bash
tcpdump -i any port 6668 or port 6667 -w vacuum.pcap
```

**Analysis:**
See `data/*.pcap` files for examples

### 2. UDP Broadcast Monitoring

**Script:** `discovery/vaccumpy.py`

Listens on port 6667 for device broadcasts:
```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 6667))

while True:
    data, addr = sock.recvfrom(1024)
    # Analyze packet structure
```

### 3. DPS Enumeration

**Script:** `utils/banthi_dps_mapping.py`

Tests DPS values 1-250:
```python
for dps in range(1, 250):
    try:
        result = vacuum.status()
        if str(dps) in result['dps']:
            print(f"Found DPS {dps}: {result['dps'][str(dps)]}")
    except:
        pass
```

### 4. Map Data Analysis

**Scripts:**
- `mapping/decode_map.py` - Raw binary analysis
- `mapping/tuya_decoder.py` - Format detection
- `mapping/visualize_map.py` - Multiple visualization attempts

**Process:**
1. Capture map data from DPS 15
2. Decode base64
3. Analyze binary structure
4. Identify patterns (coordinates, headers)
5. Visualize to verify

### 5. Smart Life App Monitoring

**Method:**
1. Set up transparent proxy (mitmproxy)
2. Configure phone to use proxy
3. Open Smart Life app
4. Capture HTTPS traffic
5. Extract API calls and responses

**Alternative:**
Monitor local network while using app:
```bash
python3 mapping/banthi_get_map.py
# Choose option 2 (Monitor mode)
# Open app and view map
# Script captures transmitted data
```

## Protocol Versions

### Version 3.3 (Current)

- AES encryption
- JSON payload
- 16-byte header
- CRC32 checksum
- Persistent socket support

### Version 3.1 (Legacy)

- Similar to 3.3
- Different header format
- No persistent socket

### Differences:

| Feature | v3.1 | v3.3 |
|---------|------|------|
| Encryption | AES-ECB | AES-ECB |
| Header size | 16 bytes | 16 bytes |
| Persistent | No | Yes |
| Sequence | Optional | Required |

## Security Considerations

### Encryption

- AES-128 in ECB mode (not CBC)
- Key: Device local key (16 bytes)
- No salt or IV
- ECB mode means identical plaintext → identical ciphertext

### Authentication

- No mutual authentication
- Local key is sufficient for full control
- No session tokens
- No rate limiting

### Vulnerabilities

1. **Local key exposure** - Anyone with key has full control
2. **No authentication** - No verification of client identity
3. **Replay attacks** - Possible without sequence validation
4. **ECB mode** - Pattern analysis possible

### Best Practices

1. Keep local key secret
2. Use firewall to restrict access
3. Monitor for unauthorized connections
4. Change credentials periodically
5. Use local network only (no internet exposure)

## Future Work

### Unexplored DPS Values

Possible undiscovered features:
- Room-specific cleaning (DPS 200-210?)
- Zone editing (DPS 150-160?)
- Schedule management (DPS 50-60?)
- Voice settings (DPS 70-80?)

### Map Editing

Potential for:
- Virtual walls
- No-go zones
- Specific room selection
- Zone cleaning

### Advanced Features

To be explored:
- Multi-floor maps
- Carpet detection
- Object recognition (if supported)
- Custom cleaning patterns

## References

- [TinyTuya Documentation](https://github.com/jasonacox/tinytuya)
- [Tuya IoT Platform API](https://developer.tuya.com/en/docs/iot)
- [Tuya Protocol Analysis](https://github.com/codetheweb/tuyapi/blob/master/docs/PROTOCOL.md)

## Appendix: Full Status Example

```json
{
  "dps": {
    "1": false,
    "2": false,
    "4": "standby",
    "5": "standby",
    "7": 85,
    "8": 90,
    "9": "normal",
    "10": "medium",
    "15": "qgABFxeqAAMpAQAqqgBcGwUA...",
    "17": 0,
    "21": 0,
    "25": false,
    "26": 100,
    "27": false,
    "29": 150,
    "30": 42,
    "31": 1250,
    "102": 0,
    "103": true,
    "199": "0"
  }
}
```

This represents:
- Vacuum off (1: false)
- Not paused (2: false)
- Standby mode (4, 5: "standby")
- Side brush 85% life (7: 85)
- Filter 90% life (8: 90)
- Normal suction (9: "normal")
- Medium water (10: "medium")
- Map data available (15: base64)
- Not currently cleaning (17, 21: 0)
- Find robot off (25: false)
- 100% battery (26: 100)
- DND off (27: false)
- Main brush 150 cycles (29: 150)
- 42 lifetime cleans (30: 42)
- 1250m² lifetime (31: 1250)
- No errors (102: 0)
- Auto boost on (103: true)
- Map 0 selected (199: "0")
