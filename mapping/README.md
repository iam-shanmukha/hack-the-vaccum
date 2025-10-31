# Mapping Scripts

Tools for extracting, decoding, and visualizing vacuum cleaner map data.

## Scripts Overview

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| banthi_get_map.py | Request and capture map data | Live vacuum | Binary files, JSON |
| decode_map.py | Decode base64 map data | Base64 string | JSON coordinates |
| visualize_map.py | Multi-format visualization | Binary data | PNG images |
| map_visualizer_v2.py | Room boundary decoder | Base64 string | PNG, JSON |
| tuya_decoder.py | Generic Tuya map decoder | Base64 string | JSON |
| live_map.py | Real-time monitoring | Live vacuum | Live plot |
| vaccum_map_test.py | Cloud API map retrieval | Cloud API | JSON |

## Detailed Script Information

### banthi_get_map.py (RECOMMENDED)

**Advanced map retrieval with multiple methods.**

**Features:**
- Request map via DPS
- Monitor for map updates
- Automatic format detection (PNG/JSON/binary)
- Multiple DPS testing
- Save to multiple formats

**Usage:**
```bash
python3 banthi_get_map.py
```

**Menu:**
1. Request Map Data - Sends map request to vacuum
2. Monitor for Map Updates (60s) - Passive monitoring
3. Get Current Path Data - Retrieve path only
4. Manual Control Test - Test movement commands

**When to use:**
- First time extracting map
- Vacuum is actively cleaning
- Want to capture real-time updates

**Output files:**
- `map_dps_*.bin` - Binary map data
- `map_dps_*.txt` - Text format if not binary
- `map.png` - If PNG format detected
- `map.pgm` - ROS-compatible format

### map_visualizer_v2.py

**Decode and visualize room boundaries.**

**Best for:**
- Understanding room layout
- Calculating room areas
- Floor plan visualization

**Usage:**
```bash
python3 map_visualizer_v2.py
```

**Hardcoded with sample data** - Edit line 145 to use your own:
```python
map_data_b64 = 'your_base64_data_here'
```

**Output:**
- `room_map_proper.png` - Visual floor plan
- `rooms_decoded.json` - Room data with measurements

### visualize_map.py

**Multiple visualization methods.**

**Tries:**
1. Path coordinates plot
2. Bitmap interpretations (various sizes)
3. Structure analysis
4. Tuya format detection

**Usage:**
```bash
python3 visualize_map.py
```

**Output:**
- `vacuum_path.png` - Path visualization
- `map_bitmap_*.png` - Various bitmap attempts

### decode_map.py

**Low-level map decoder.**

**Features:**
- Binary analysis
- Hex dump
- Header parsing
- Coordinate extraction
- Pattern detection

**Usage:**
```bash
python3 decode_map.py
```

**Output:**
- `map_raw.bin` - Raw binary
- `map_coords.json` - Extracted coordinates

### tuya_decoder.py

**Generic Tuya map format decoder.**

**Handles:**
- Path data
- Compressed maps (gzip)
- Unknown formats

**Usage:**
```bash
python3 tuya_decoder.py
```

**Output:**
- `map_decoded.json` - Decoded structure
- `map_decompressed.bin` - If compressed

### live_map.py

**Real-time map monitoring with visualization.**

**Features:**
- Live matplotlib display
- Updates every 2 seconds
- Room boundary plotting
- Status overlay (battery, state)

**Usage:**
```bash
python3 live_map.py
```

**Choose:**
1. Decode current map data
2. Request and decode full map
3. Live monitor (experimental)

**Requirements:**
- matplotlib with GUI backend
- Active vacuum cleaning

### vaccum_map_test.py

**Cloud API map retrieval.**

**Tests multiple endpoints:**
- Device properties
- Device functions
- Map-specific API

**Usage:**
```bash
python3 vaccum_map_test.py
```

**Requires:** Cloud API credentials configured

## Map Data Workflow

### Extraction Workflow

```
1. Start vacuum cleaning
   ↓
2. Run banthi_get_map.py
   ↓
3. Choose option 1 (Request) or 2 (Monitor)
   ↓
4. Wait for map data in DPS 15
   ↓
5. Data saved to files
```

### Visualization Workflow

```
Map Data (base64)
   ↓
decode_map.py → Extract coordinates
   ↓
map_visualizer_v2.py → Room boundaries
   ↓
visualize_map.py → Path visualization
```

### Live Monitoring Workflow

```
1. Start live_map.py (option 3)
   ↓
2. Start vacuum cleaning
   ↓
3. Watch real-time updates
   ↓
4. Map displays in matplotlib window
```

## Map Data Format

### Structure

```
Base64 Encoded String
    ↓ decode
Binary Data:
  - Header: 0xAA00 + version (3 bytes)
  - Room Data: 4 corners × N rooms (16 bytes per room)
  - Path Data: coordinate pairs (4 bytes per point)
```

### Coordinate System

- **Origin**: Charging dock (0, 0)
- **Units**: Millimeters
- **Range**: -10000 to +10000 mm
- **Format**: int16 little-endian

### Example

```python
# Room boundary
Corner 1: (100, 100)
Corner 2: (5000, 100)
Corner 3: (5000, 3000)
Corner 4: (100, 3000)
# = Rectangle: 4900mm × 2900mm = 14.21 m²
```

## Quick Reference

### Get Map (First Time)

```bash
# Method 1: Request from vacuum
python3 banthi_get_map.py  # Choose option 1

# Method 2: Monitor passively
python3 banthi_get_map.py  # Choose option 2
# Then open Smart Life app to trigger map transmission

# Method 3: Cloud API
python3 vaccum_map_test.py
```

### Visualize Existing Map

```bash
# Room boundaries
python3 map_visualizer_v2.py

# Path visualization
python3 visualize_map.py

# Low-level analysis
python3 decode_map.py
```

### Live Monitoring

```bash
python3 live_map.py  # Choose option 3
```

## Troubleshooting

### No map data received

**Solutions:**
1. Ensure vacuum is cleaning (not idle)
2. Try different request types ('get_map', 'get_both')
3. Use monitor mode and trigger via app
4. Check DPS 15 directly:
```python
status = vacuum.status()
print(status['dps'].get('15'))
```

### Map data but decode fails

**Check format:**
```python
decoded = base64.b64decode(map_data)
print(decoded[:16].hex())  # Check magic bytes
print(decoded[:4])  # Check if PNG/JSON
```

### Visualization shows garbage

**Possible issues:**
- Wrong coordinate interpretation
- Incorrect header offset
- Compressed data (try tuya_decoder.py)
- Wrong data type (bitmap vs coordinates)

### Empty/corrupted files

**Fixes:**
- Request during active cleaning
- Check disk space
- Verify base64 decode success
- Try different DPS values (106, 121, 122)

## Advanced Usage

### Extract Map During Cleaning

```bash
# Terminal 1: Start monitoring
python3 banthi_get_map.py  # Option 2

# Terminal 2: Start cleaning
python3 ../control/vacuum_controller.py  # Option 2

# Map data will be captured automatically
```

### Compare Maps Over Time

```bash
# Capture map 1
python3 banthi_get_map.py  # Save with timestamp
mv map_dps_15_*.bin map_day1.bin

# Later... capture map 2
python3 banthi_get_map.py
mv map_dps_15_*.bin map_day2.bin

# Visualize both
# Edit visualize_map.py to compare
```

### Create Custom Visualization

```python
import json
import matplotlib.pyplot as plt

# Load decoded map
with open('rooms_decoded.json') as f:
    data = json.load(f)

# Custom plotting
for room in data['rooms']:
    # Your visualization code
    pass
```

## See Also

- [../docs/PROTOCOL.md](../docs/PROTOCOL.md) - Map format specification
- [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md) - Setup instructions
- [../data/](../data/) - Sample map data
