# Control Scripts

Scripts for directly controlling the vacuum cleaner.

## Scripts

### vacuum_controller.py (RECOMMENDED)

**Main vacuum control interface with full functionality.**

**Usage:**
```bash
python3 vacuum_controller.py
```

**Features:**
- Interactive menu-driven interface
- Start/stop cleaning
- Return to charging dock
- Suction mode control (gentle/normal/max)
- Water level control (low/medium/high)
- Find robot (beep)
- Do Not Disturb mode
- Auto carpet boost
- Real-time status display
- Maintenance status tracking
- Battery monitoring
- Error code display

**Configuration:**
Edit lines 7-11 to set your device credentials:
```python
self.vacuum = tinytuya.Device(
    dev_id="your_device_id",
    address="192.168.x.x",
    local_key="your_local_key",
    version=3.3
)
```

### vacuum_controller_v1.py

**Earlier version with basic functionality.**

Simpler implementation, fewer features. Use `vacuum_controller.py` instead unless you need a minimal version.

## Quick Start

1. **Install dependencies:**
```bash
pip3 install tinytuya
```

2. **Edit credentials** in `vacuum_controller.py`

3. **Run:**
```bash
python3 vacuum_controller.py
```

4. **Try these first:**
   - Option 1: Show Status
   - Option 7: Find Robot (safe test)
   - Option 4: Return to Dock

## Command Reference

| Menu Option | Function | DPS | Safe? |
|-------------|----------|-----|-------|
| 1 | Show Status | - | Yes |
| 2 | Start Cleaning | 1 | Yes |
| 3 | Stop/Pause | 1 | Yes |
| 4 | Return to Dock | 4 | Yes |
| 5 | Set Suction Mode | 9 | Yes |
| 6 | Set Water Level | 10 | Yes |
| 7 | Find Robot | 25 | Yes |
| 8 | Toggle DND | 27 | Yes |
| 9 | Toggle Auto Boost | 103 | Yes |
| 10 | Maintenance Status | 7,8,29 | Yes |

All commands are safe to use.

## See Also

- [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md) - Complete setup instructions
- [../docs/PROTOCOL.md](../docs/PROTOCOL.md) - DPS reference and protocol details
