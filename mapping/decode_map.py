import base64
import struct
import json

# The map data from DPS 15
map_data_b64 = 'qgABFxeqAAMpAQAqqgBcGwUABAEWAzIDlQMyA5UB2AEWAdgABAW+ArAHIAKwByAAxAW+AMQABP4q/+UAQP/lAED+vf4q/r0ABP+1/KECivyhAor6Bf+1+gUABADk/vUBrv71Aa7+KgDk/iqQqgACEwATqgADFQEAFg=='

# Decode from base64
decoded = base64.b64decode(map_data_b64)

print("="*60)
print("MAP DATA DECODER")
print("="*60)

print(f"\nDecoded size: {len(decoded)} bytes")
print(f"Hex dump (first 100 bytes):\n{decoded[:100].hex()}")

# Save raw binary
with open('map_raw.bin', 'wb') as f:
    f.write(decoded)
print("\n✓ Saved to map_raw.bin")

# Parse the structure
print("\n" + "="*60)
print("PARSING MAP STRUCTURE")
print("="*60)

# Tuya map format analysis
# Common structure: [header][metadata][compressed_data]

offset = 0

# Try to parse header
if len(decoded) >= 4:
    # First 2 bytes often indicate protocol/version
    magic = struct.unpack('>H', decoded[0:2])[0]
    print(f"\nMagic/Version: 0x{magic:04x}")
    
    # Check if it's a known format
    if magic == 0xaa00 or magic == 0xaa01:
        print("✓ Tuya map format detected!")

# Look for patterns
print("\nSearching for patterns...")

# Convert to hex string for pattern matching
hex_data = decoded.hex()

# Look for coordinate patterns (int16 or int32 values)
print("\nAttempting to extract coordinates...")
coords = []
for i in range(0, len(decoded) - 3, 2):
    try:
        x = struct.unpack('<h', decoded[i:i+2])[0]  # signed int16
        y = struct.unpack('<h', decoded[i+2:i+4])[0]
        
        # Sanity check: coordinates usually in range -10000 to 10000
        if -10000 < x < 10000 and -10000 < y < 10000:
            coords.append((x, y))
    except:
        pass

if coords:
    print(f"Found {len(coords)} potential coordinate pairs")
    print(f"Sample coordinates: {coords[:10]}")
    
    # Save as JSON for visualization
    with open('map_coords.json', 'w') as f:
        json.dump(coords, f, indent=2)
    print("✓ Saved to map_coords.json")

# Try to identify sections
print("\n" + "="*60)
print("ANALYZING STRUCTURE")
print("="*60)

# Look for null terminators or section markers
sections = []
for i in range(len(decoded)):
    if decoded[i:i+2] == b'\xaa\x00':
        sections.append(i)
        print(f"Section marker at offset {i}")

# ASCII dump for readable parts
print("\nASCII representation (first 200 bytes):")
ascii_repr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in decoded[:200])
print(ascii_repr)

# Detailed byte-by-byte analysis of header
print("\n" + "="*60)
print("HEADER ANALYSIS (first 32 bytes)")
print("="*60)

for i in range(min(32, len(decoded))):
    byte = decoded[i]
    print(f"Offset {i:2d}: 0x{byte:02x} ({byte:3d}) '{chr(byte) if 32 <= byte < 127 else '.'}'")