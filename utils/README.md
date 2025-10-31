# Utility Scripts

Helper scripts for protocol exploration and testing.

## Scripts

### banthi_dps_mapping.py

**DPS discovery and testing tool.**

Tests various DPS (Data Point Specification) values to discover device capabilities.

**What it does:**
- Tests map-related DPS values (106, 121-125)
- Tests path data DPS (107, 110-114)
- Tests command DPS (108, 115-117)
- Attempts to request map data via each DPS
- Displays current values if available

**Usage:**
```bash
python3 banthi_dps_mapping.py
```

**Expected output:**
```
Testing map-related DPS...

Testing request_map:
  DPS 106: None
  DPS 121: get_both
  DPS 122: None
  ...

Testing path_data:
  DPS 107: [binary data]
  ...

Requesting map data...
Request via DPS 121: {'success': True}
Request via DPS 122: {'error': 'Invalid DPS'}
...

Checking status after request...
{
  "dps": {
    "15": "qgABFxeqAAMpAQ...",
    ...
  }
}
```

## DPS Discovery Process

### Method 1: Systematic Testing

```python
# Test range of DPS values
for dps in range(1, 250):
    try:
        value = vacuum.status()['dps'].get(str(dps))
        if value is not None:
            print(f"DPS {dps}: {value} (type: {type(value).__name__})")
    except Exception as e:
        pass
```

### Method 2: Known Patterns

Tuya devices typically use:
- 1-50: Basic controls (power, mode, etc.)
- 100-130: Advanced features (auto boost, errors)
- 200-250: Extended features (multi-floor maps)

### Method 3: Write Testing

```python
# Test if DPS accepts writes
test_values = [True, False, 0, 1, "test"]
for dps in range(1, 50):
    for val in test_values:
        try:
            result = vacuum.set_value(dps, val)
            if result:
                print(f"DPS {dps} accepts {val}")
        except:
            pass
```

## Discovered DPS Values

### Confirmed Working

| DPS | Function | Type | Found By |
|-----|----------|------|----------|
| 1 | Power | bool | Status read |
| 4 | Command | string | Status read |
| 5 | Status | string | Status read |
| 9 | Suction mode | string | Status read |
| 10 | Water level | string | Status read |
| 15 | Map data | string | Status read |
| 25 | Find robot | bool | Testing |
| 26 | Battery | int | Status read |
| 121 | Map request | string | Testing |

### Unconfirmed (To Test)

| DPS Range | Likely Function |
|-----------|-----------------|
| 50-70 | Schedule/Timer |
| 80-99 | Voice/Language |
| 130-150 | Room management |
| 200-220 | Multi-floor maps |

## Custom Testing

### Test Specific DPS

```python
import tinytuya

vacuum = tinytuya.Device(
    dev_id="your_id",
    address="192.168.x.x",
    local_key="your_key",
    version=3.3
)

# Test read
dps_to_test = 150
value = vacuum.status()['dps'].get(str(dps_to_test))
print(f"DPS {dps_to_test}: {value}")

# Test write
test_values = [True, False, "test", 0, 1, 100]
for val in test_values:
    try:
        result = vacuum.set_value(dps_to_test, val)
        print(f"DPS {dps_to_test} = {val}: {result}")
    except Exception as e:
        print(f"Failed: {e}")
```

### Monitor All DPS Changes

```python
# Monitor for new DPS values
import time

previous = {}
while True:
    current = vacuum.status()['dps']

    # Check for new DPS
    for key in current:
        if key not in previous:
            print(f"NEW DPS {key}: {current[key]}")

    # Check for changes
    for key in current:
        if key in previous and previous[key] != current[key]:
            print(f"DPS {key} changed: {previous[key]} → {current[key]}")

    previous = current.copy()
    time.sleep(2)
```

## Safety Notes

### Safe to Test

- Reading any DPS value (won't harm device)
- Boolean toggles (can be undone)
- String values from known list
- Numeric values in reasonable ranges

### Potentially Unsafe

- Random numeric values (could damage motors)
- Unknown command strings (unpredictable behavior)
- DPS values >200 (may be factory settings)
- Rapid repeated writes (could crash firmware)

### Testing Best Practices

1. **Read before write** - Know current value
2. **Test one at a time** - Identify what changed
3. **Document everything** - Keep notes
4. **Have escape plan** - Know how to reset
5. **Start conservative** - Boolean before numbers

## Common DPS Patterns

### Boolean Controls

```python
# Usually toggles
vacuum.set_value(dps, True)   # Enable
vacuum.set_value(dps, False)  # Disable
```

### Mode Selection

```python
# Usually from predefined list
modes = ['mode1', 'mode2', 'mode3']
vacuum.set_value(dps, modes[0])
```

### Numeric Settings

```python
# Usually percentage or level
vacuum.set_value(dps, 50)  # Often 0-100
```

## Troubleshooting

### No response from DPS

**Possible reasons:**
- DPS doesn't exist on this device
- Wrong data type
- Feature requires different state (e.g., must be cleaning)
- Read-only DPS

### Command accepted but nothing happens

**Check:**
- Current device state (must be ready)
- Dependencies (other DPS must be set first)
- Timing (may take time to execute)
- Preconditions (battery, position, etc.)

### Device becomes unresponsive

**Recovery:**
1. Power cycle vacuum (turn off/on)
2. Reset via button (hold 5 seconds)
3. Re-pair with Smart Life app if needed
4. Check for firmware updates

## Advanced Exploration

### Cloud API Function List

```bash
# Get list of all device functions
python3 << EOF
from tinytuya import Cloud
cloud = Cloud(
    apiRegion="in",
    apiKey="your_key",
    apiSecret="your_secret"
)
functions = cloud.cloudrequest('/v1.0/devices/your_id/functions')
print(functions)
EOF
```

### Packet Capture Analysis

```bash
# Capture traffic while using app
tcpdump -i any port 6668 -w vacuum_test.pcap

# Then analyze what DPS changed
# Use Wireshark to decrypt and view
```

## See Also

- [../docs/PROTOCOL.md](../docs/PROTOCOL.md) - Complete DPS reference
- [../control/](../control/) - Use discovered DPS values
- [../discovery/](../discovery/) - Network analysis tools
