import base64
import struct
import matplotlib.pyplot as plt
import numpy as np

map_data_b64 = 'qgABFxeqAAMpAQAqqgBcGwUABAEWAzIDlQMyA5UB2AEWAdgABAW+ArAHIAKwByAAxAW+AMQABP4q/+UAQP/lAED+vf4q/r0ABP+1/KECivyhAor6Bf+1+gUABADk/vUBrv71Aa7+KgDk/iqQqgACEwATqgADFQEAFg=='

decoded = base64.b64decode(map_data_b64)

print("Attempting to visualize map data...")

# Method 1: Try as coordinate pairs (path)
print("\n1. Parsing as path coordinates...")
coords = []
offset = 4  # Skip header

while offset < len(decoded) - 3:
    try:
        x = struct.unpack('<h', decoded[offset:offset+2])[0]
        y = struct.unpack('<h', decoded[offset+2:offset+4])[0]
        
        if -10000 < x < 10000 and -10000 < y < 10000:
            coords.append((x, y))
        offset += 2
    except:
        break

if coords:
    print(f"Found {len(coords)} coordinates")
    
    # Plot the path
    plt.figure(figsize=(10, 10))
    xs, ys = zip(*coords) if coords else ([], [])
    plt.plot(xs, ys, 'b-', linewidth=1, label='Path')
    plt.plot(xs[0], ys[0], 'go', markersize=10, label='Start')
    if len(xs) > 1:
        plt.plot(xs[-1], ys[-1], 'ro', markersize=10, label='End')
    
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.legend()
    plt.title('Vacuum Path')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.savefig('vacuum_path.png', dpi=150, bbox_inches='tight')
    print("✓ Saved path visualization to vacuum_path.png")
    plt.close()

# Method 2: Try as bitmap
print("\n2. Trying bitmap interpretation...")
# Skip possible header and try different sizes
for header_size in [4, 8, 16]:
    map_bytes = decoded[header_size:]
    
    # Try different dimensions
    sizes = [
        (50, 50), (100, 100), (128, 128), (200, 200),
        (int(np.sqrt(len(map_bytes))), int(np.sqrt(len(map_bytes))))
    ]
    
    for width, height in sizes:
        if width * height <= len(map_bytes):
            try:
                img = np.frombuffer(map_bytes[:width*height], dtype=np.uint8)
                img = img.reshape((height, width))
                
                plt.figure(figsize=(8, 8))
                plt.imshow(img, cmap='gray')
                plt.title(f'Map as {width}x{height} bitmap (header={header_size})')
                plt.savefig(f'map_bitmap_{width}x{height}_h{header_size}.png')
                print(f"  ✓ Saved map_bitmap_{width}x{height}_h{header_size}.png")
                plt.close()
            except:
                pass

# Method 3: Analyze as structured data
print("\n3. Analyzing structure...")

# The data might be: [type][count][coords...]
if len(decoded) >= 8:
    # Try reading as little-endian integers
    possible_header = struct.unpack('<4H', decoded[0:8])
    print(f"First 4 uint16 values: {possible_header}")
    
    possible_header32 = struct.unpack('<2I', decoded[0:8])
    print(f"First 2 uint32 values: {possible_header32}")

# Method 4: Look for Tuya's specific format
print("\n4. Checking Tuya vacuum map format...")

# Tuya format often has:
# - Magic bytes
# - Map ID
# - Coordinate scale
# - Room boundaries
# - Cleaning path

idx = 0
segments = []

try:
    while idx < len(decoded) - 2:
        # Look for 0xAA markers (common in Tuya protocol)
        if decoded[idx] == 0xAA:
            seg_type = decoded[idx + 1] if idx + 1 < len(decoded) else 0
            segments.append((idx, seg_type))
            print(f"Segment at {idx}: type={seg_type}")
        idx += 1
except:
    pass

print("\n" + "="*60)
print("Summary:")
print(f"Total size: {len(decoded)} bytes")
print(f"Coordinate pairs found: {len(coords)}")
print(f"Segments found: {len(segments)}")
print("="*60)