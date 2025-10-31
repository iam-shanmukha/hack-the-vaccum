# Security Policy

## Sensitive Data Protection

This repository contains code to control IoT devices. **DO NOT** commit the following:

### Never Commit

- [ ] API Keys (`apiKey` in tinytuya.json)
- [ ] API Secrets (`apiSecret` in tinytuya.json)
- [ ] Device IDs (`dev_id`)
- [ ] Local Keys (`local_key`)
- [ ] IP Addresses (when device-specific)
- [ ] Network captures (*.pcap files)
- [ ] Any file containing credentials

### Files with Sensitive Data

The following files contain sensitive information and are in `.gitignore`:

```
data/tinytuya.json          # API credentials
**/tinytuya.json            # Any tinytuya.json in any folder
*.pcap, *.pcapng           # Network captures (MAC addresses)
raw/                        # May contain credentials
credentials.txt             # Any credentials file
.env                        # Environment variables
```

### Credential Locations in Code

Update these with YOUR credentials (already gitignored):

1. **data/tinytuya.json** - Cloud API credentials
2. **control/vacuum_controller.py** lines 7-11 - Device credentials
3. **mapping/*.py** scripts - Device credentials in Device() initialization
4. **discovery/tuya_get_local.py** lines 5-8 - API credentials

### Before Committing

Run this checklist:

```bash
# Check for exposed credentials
git diff | grep -i "apiKey\|apiSecret\|local_key\|dev_id"

# Check gitignore is working
git status --ignored

# Verify sensitive files are ignored
ls data/tinytuya.json  # Should exist locally
git ls-files data/tinytuya.json  # Should be empty (not tracked)
```

### Recommended Practices

#### 1. Use Environment Variables

Instead of hardcoding:

```python
import os

vacuum = tinytuya.Device(
    dev_id=os.getenv('TUYA_DEVICE_ID'),
    address=os.getenv('TUYA_IP'),
    local_key=os.getenv('TUYA_LOCAL_KEY'),
    version=3.3
)
```

Then create `.env` file (already in .gitignore):
```bash
TUYA_DEVICE_ID=your_device_id
TUYA_IP=192.168.x.x
TUYA_LOCAL_KEY=your_local_key
```

#### 2. Create Template Files

For sharing, create `data/tinytuya.json.template`:

```json
{
    "apiKey": "YOUR_API_KEY_HERE",
    "apiSecret": "YOUR_API_SECRET_HERE",
    "apiRegion": "in",
    "apiDeviceID": "YOUR_DEVICE_ID_HERE"
}
```

Users copy to `tinytuya.json` and fill in their values.

#### 3. Sanitize Before Sharing

If sharing logs or screenshots:

```bash
# Remove sensitive data from logs
sed 's/dev_id="[^"]*"/dev_id="REDACTED"/g' output.log
sed 's/local_key="[^"]*"/local_key="REDACTED"/g' output.log
sed 's/"apiKey": "[^"]*"/"apiKey": "REDACTED"/g' output.log
```

### Git Safety Commands

```bash
# Check what will be committed
git status
git diff --cached

# Remove accidentally staged credentials
git reset HEAD data/tinytuya.json
git restore --staged control/vacuum_controller.py

# Remove from history (if already committed)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch data/tinytuya.json" \
  --prune-empty --tag-name-filter cat -- --all
```

### Security Risks

#### Local Key Compromise

The `local_key` provides **FULL CONTROL** over the device:
- Start/stop vacuum
- Access map data
- Modify all settings
- No authentication required

**Protection:**
- Never share local key
- Use firewall to restrict device access
- Keep device on isolated network if possible

#### API Credentials

API Key + Secret provides:
- Access to ALL devices in your account
- Device registration
- Cloud control
- User data access

**Protection:**
- Rotate keys regularly in Tuya IoT platform
- Use separate project for testing
- Revoke access when no longer needed

#### Network Captures

PCAP files may contain:
- MAC addresses
- Local keys (if captured during handshake)
- Device identifiers
- Network topology

**Protection:**
- `.gitignore` blocks *.pcap
- Sanitize before sharing
- Use dummy/test devices for captures

## Reporting Security Issues

If you find security vulnerabilities:

1. **DO NOT** create public GitHub issues
2. Document the issue privately
3. Check if it's a Tuya platform issue (report to Tuya)
4. For this project: Create private disclosure

## Responsible Use

This project is for:
- ✅ Personal use and learning
- ✅ Local device control
- ✅ Reverse engineering for interoperability
- ✅ Educational purposes

**NOT** for:
- ❌ Accessing devices you don't own
- ❌ Circumventing security for malicious purposes
- ❌ Distributed attacks
- ❌ Service disruption

## Compliance

Users are responsible for:
- Compliance with local laws
- Tuya IoT Platform Terms of Service
- Device warranty terms
- Network security policies

## Questions?

For security questions, review:
- [docs/PROTOCOL.md](docs/PROTOCOL.md) - Protocol security analysis
- [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Security best practices
- Tuya IoT Platform security documentation
