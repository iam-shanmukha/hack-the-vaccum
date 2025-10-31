# Complete Scripts Index

Comprehensive reference for all scripts in the project.

## Control Scripts

### vacuum_controller.py ⭐ CURRENT VERSION
**Location:** `control/vacuum_controller.py`

**Purpose:** Full-featured vacuum control interface

**Features:**
- Interactive menu
- All basic controls (start/stop/pause/dock)
- Suction mode control
- Water level control
- Find robot
- DND mode
- Auto boost
- Status display
- Maintenance tracking

**Usage:**
```bash
python3 control/vacuum_controller.py
```

**Configuration:** Lines 7-11 (device credentials)

**DPS Used:** 1, 2, 4, 5, 7, 8, 9, 10, 17, 21, 25, 26, 27, 29, 30, 31, 102, 103

---

### vacuum_controller_v1.py
**Location:** `control/vacuum_controller_v1.py`

**Purpose:** Legacy controller (simpler version)

**Use case:** Reference implementation, minimal features

---

## Discovery Scripts

### tuyatest.py
**Location:** `discovery/tuyatest.py`

**Purpose:** Network scanner for Tuya devices

**Output:** IP addresses, versions, device IDs

**Usage:**
```bash
python3 discovery/tuyatest.py
```

**When to use:** Finding vacuum's IP address

---

### tuya_get_local.py
**Location:** `discovery/tuya_get_local.py`

**Purpose:** Cloud API connection

**Requirements:** API credentials (lines 5-8)

**Gets:**
- Device info
- All devices
- Status from cloud

**Usage:**
```bash
python3 discovery/tuya_get_local.py
```

---

### vaccumpy.py
**Location:** `discovery/vaccumpy.py`

**Purpose:** UDP broadcast listener

**Port:** 6667 UDP

**Usage:**
```bash
python3 discovery/vaccumpy.py
```

**When to use:**
- Protocol analysis
- Device discovery without cloud
- Packet structure examination

---

## Mapping Scripts

### banthi_get_map.py ⭐ RECOMMENDED
**Location:** `mapping/banthi_get_map.py`

**Purpose:** Advanced map retrieval

**Features:**
- Request map via DPS
- Monitor for updates
- Auto format detection
- Multiple output formats

**Usage:**
```bash
python3 mapping/banthi_get_map.py
```

**Options:**
1. Request Map Data
2. Monitor for Map Updates (60s)
3. Get Current Path Data
4. Manual Control Test

**Output:**
- `map_dps_*.bin`
- `map.png` (if PNG)
- `map.pgm` (ROS format)

**DPS Used:** 15, 106, 107, 110-115, 121-123

---

### map_visualizer_v2.py
**Location:** `mapping/map_visualizer_v2.py`

**Purpose:** Room boundary decoder and visualizer

**Input:** Base64 map data (line 145)

**Output:**
- `room_map_proper.png`
- `rooms_decoded.json`

**Usage:**
```bash
python3 mapping/map_visualizer_v2.py
```

**Best for:** Understanding room layout

---

### visualize_map.py
**Location:** `mapping/visualize_map.py`

**Purpose:** Multiple visualization methods

**Tries:**
- Path coordinates
- Bitmap interpretations
- Structure analysis
- Tuya format detection

**Output:**
- `vacuum_path.png`
- `map_bitmap_*.png`

**Usage:**
```bash
python3 mapping/visualize_map.py
```

---

### decode_map.py
**Location:** `mapping/decode_map.py`

**Purpose:** Low-level binary decoder

**Features:**
- Hex dump
- Header parsing
- Coordinate extraction
- Pattern detection

**Output:**
- `map_raw.bin`
- `map_coords.json`

**Usage:**
```bash
python3 mapping/decode_map.py
```

---

### tuya_decoder.py
**Location:** `mapping/tuya_decoder.py`

**Purpose:** Generic Tuya map decoder

**Handles:**
- Path data
- Compressed maps
- Unknown formats

**Output:**
- `map_decoded.json`
- `map_decompressed.bin`

**Usage:**
```bash
python3 mapping/tuya_decoder.py
```

---

### live_map.py
**Location:** `mapping/live_map.py`

**Purpose:** Real-time map monitoring

**Features:**
- Live matplotlib display
- 2-second updates
- Status overlay

**Usage:**
```bash
python3 mapping/live_map.py
```

**Requirements:** matplotlib with GUI backend

---

### vaccum_map_test.py
**Location:** `mapping/vaccum_map_test.py`

**Purpose:** Cloud API map retrieval

**Tests:**
- Device properties
- Device functions
- Map API endpoints

**Usage:**
```bash
python3 mapping/vaccum_map_test.py
```

**Requires:** Cloud credentials (lines 32-36)

---

## Utility Scripts

### banthi_dps_mapping.py
**Location:** `utils/banthi_dps_mapping.py`

**Purpose:** DPS discovery tool

**Tests:**
- Map-related DPS (106, 121-125)
- Path data DPS (107, 110-114)
- Command DPS (108, 115-117)

**Usage:**
```bash
python3 utils/banthi_dps_mapping.py
```

**When to use:**
- Discovering new features
- Testing unknown DPS
- Protocol exploration

---

## Quick Reference Table

| Task | Script | Location |
|------|--------|----------|
| Control vacuum | vacuum_controller.py | control/ |
| Find IP address | tuyatest.py | discovery/ |
| Get credentials | tuya_get_local.py | discovery/ |
| Extract map | banthi_get_map.py | mapping/ |
| Visualize rooms | map_visualizer_v2.py | mapping/ |
| Visualize path | visualize_map.py | mapping/ |
| Live monitor | live_map.py | mapping/ |
| Test DPS | banthi_dps_mapping.py | utils/ |
| Network analysis | vaccumpy.py | discovery/ |

## Typical Workflow

### First Time Setup
```bash
1. python3 discovery/tuyatest.py          # Find IP
2. python3 discovery/tuya_get_local.py    # Get credentials
3. # Edit control/vacuum_controller.py    # Configure
4. python3 control/vacuum_controller.py   # Test
```

### Daily Usage
```bash
python3 control/vacuum_controller.py      # Control vacuum
```

### Map Extraction
```bash
1. python3 control/vacuum_controller.py   # Start cleaning
2. python3 mapping/banthi_get_map.py      # Extract map
3. python3 mapping/map_visualizer_v2.py   # Visualize
```

### Exploration
```bash
1. python3 utils/banthi_dps_mapping.py    # Test DPS
2. python3 discovery/vaccumpy.py          # Capture packets
3. # Analyze results
```

## Script Dependencies

### All Scripts Require
- Python 3.7+
- tinytuya

### Visualization Scripts Require
- matplotlib
- numpy

### Network Scripts Require
- socket (built-in)
- struct (built-in)

## Configuration Locations

| Script | Config Location | What to Edit |
|--------|----------------|--------------|
| vacuum_controller.py | Lines 7-11 | Device credentials |
| tuya_get_local.py | Lines 5-8 | API credentials |
| banthi_get_map.py | Lines 9-13 | Device credentials |
| All mapping scripts | Lines ~9-13 | Device credentials |
| vaccum_map_test.py | Lines 32-36 | API & device info |

## DPS Usage by Script

| DPS | Purpose | Used By |
|-----|---------|---------|
| 1 | Power | vacuum_controller.py |
| 4 | Commands | vacuum_controller.py |
| 9 | Suction | vacuum_controller.py |
| 10 | Water | vacuum_controller.py |
| 15 | Map data | All mapping scripts |
| 25 | Find | vacuum_controller.py |
| 26 | Battery | vacuum_controller.py |
| 27 | DND | vacuum_controller.py |
| 103 | Auto boost | vacuum_controller.py |
| 121 | Map request | banthi_get_map.py |

## Script Compatibility

All scripts tested with:
- Eureka Forbes LVAC Voice Pro
- Tuya Protocol 3.3
- Python 3.8+
- tinytuya 1.13.0+

## Modification Guide

### Change Device Credentials
Edit the `Device()` initialization in each script:
```python
vacuum = tinytuya.Device(
    dev_id="your_id",
    address="your_ip",
    local_key="your_key",
    version=3.3
)
```

### Add New Command
1. Find DPS in `docs/PROTOCOL.md`
2. Add to `vacuum_controller.py`:
```python
def new_command(self):
    return self.vacuum.set_value(dps_number, value)
```
3. Add menu option in `main()`

### Create Custom Visualization
Use `map_visualizer_v2.py` as template:
```python
import base64, struct, matplotlib.pyplot as plt

# Your custom decoder
# Your custom visualization
```

## See Also

- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - 5-minute guide
- [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Detailed setup
- [docs/PROTOCOL.md](docs/PROTOCOL.md) - Protocol specs
- Per-directory README files for details
