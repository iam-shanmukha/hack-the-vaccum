import base64
import struct
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class TuyaRoomMapDecoder:
    def __init__(self, base64_data):
        self.data = base64.b64decode(base64_data)
        self.offset = 0
        
    def read_byte(self):
        val = self.data[self.offset]
        self.offset += 1
        return val
    
    def read_int16(self):
        val = struct.unpack('<h', self.data[self.offset:self.offset+2])[0]
        self.offset += 2
        return val
    
    def read_uint16(self):
        val = struct.unpack('<H', self.data[self.offset:self.offset+2])[0]
        self.offset += 2
        return val
    
    def decode_rooms(self):
        """Decode room boundary data"""
        print("="*60)
        print("TUYA ROOM MAP DECODER")
        print("="*60)
        
        # Skip magic bytes and header
        magic = self.read_uint16()
        version = self.read_byte()
        
        print(f"Magic: 0x{magic:04x}")
        print(f"Version: {version}")
        
        rooms = []
        room_id = 0
        
        # Parse room boundaries
        while self.offset < len(self.data) - 3:
            # Each room might be defined by:
            # - 4 coordinates (rectangle corners)
            # - Or variable number of points (polygon)
            
            # Try to read as groups of 4 points (rectangles)
            if self.offset + 8 <= len(self.data):
                coords = []
                for i in range(4):
                    if self.offset + 4 <= len(self.data):
                        x = self.read_int16()
                        y = self.read_int16()
                        coords.append((x, y))
                
                if len(coords) == 4:
                    # Check if it forms a valid rectangle
                    xs = [c[0] for c in coords]
                    ys = [c[1] for c in coords]
                    
                    # Valid if it has 2 unique x values and 2 unique y values
                    if len(set(xs)) == 2 and len(set(ys)) == 2:
                        min_x, max_x = min(xs), max(xs)
                        min_y, max_y = min(ys), max(ys)
                        
                        room = {
                            'id': room_id,
                            'type': 'rectangle',
                            'bounds': {
                                'min_x': min_x,
                                'max_x': max_x,
                                'min_y': min_y,
                                'max_y': max_y
                            },
                            'corners': coords,
                            'area': abs(max_x - min_x) * abs(max_y - min_y)
                        }
                        rooms.append(room)
                        room_id += 1
                        print(f"\nRoom {room_id}: Rectangle")
                        print(f"  Bounds: ({min_x}, {min_y}) to ({max_x}, {max_y})")
                        print(f"  Size: {abs(max_x - min_x)} x {abs(max_y - min_y)}")
                        print(f"  Area: {room['area']} sq units")
        
        return rooms
    
    def visualize_rooms(self, rooms, output_file='room_map_proper.png'):
        """Visualize the room map properly"""
        if not rooms:
            print("No rooms to visualize!")
            return
        
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Define colors for different rooms
        colors = plt.cm.Set3(np.linspace(0, 1, len(rooms)))
        
        # Plot each room
        for i, room in enumerate(rooms):
            if room['type'] == 'rectangle':
                bounds = room['bounds']
                width = bounds['max_x'] - bounds['min_x']
                height = bounds['max_y'] - bounds['min_y']
                
                # Create rectangle patch
                rect = patches.Rectangle(
                    (bounds['min_x'], bounds['min_y']),
                    width,
                    height,
                    linewidth=2,
                    edgecolor='black',
                    facecolor=colors[i],
                    alpha=0.5,
                    label=f"Room {room['id'] + 1}"
                )
                ax.add_patch(rect)
                
                # Add room label
                center_x = (bounds['min_x'] + bounds['max_x']) / 2
                center_y = (bounds['min_y'] + bounds['max_y']) / 2
                ax.text(center_x, center_y, f"R{room['id'] + 1}", 
                       ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Set axis properties
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        ax.set_xlabel('X coordinate (mm)', fontsize=12)
        ax.set_ylabel('Y coordinate (mm)', fontsize=12)
        ax.set_title('Vacuum Cleaner Room Map', fontsize=14, fontweight='bold')
        
        # Add coordinate origin
        ax.axhline(y=0, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.axvline(x=0, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=200, bbox_inches='tight')
        print(f"\n✓ Saved room map to {output_file}")
        plt.close()

# Decode the map
map_data_b64 = 'qgABFxeqAAMpAQAqqgBcGwUABAEWAzIDlQMyA5UB2AEWAdgABAW+ArAHIAKwByAAxAW+AMQABP4q/+UAQP/lAED+vf4q/r0ABP+1/KECivyhAor6Bf+1+gUABADk/vUBrv71Aa7+KgDk/iqQqgACEwATqgADFQEAFg=='

decoder = TuyaRoomMapDecoder(map_data_b64)
rooms = decoder.decode_rooms()

# Save room data
output_data = {
    'total_rooms': len(rooms),
    'rooms': rooms
}

with open('rooms_decoded.json', 'w') as f:
    json.dump(output_data, f, indent=2)
print(f"\n✓ Saved room data to rooms_decoded.json")

# Visualize
if rooms:
    decoder.visualize_rooms(rooms)

# Print summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total rooms detected: {len(rooms)}")
print(f"Total mapped area: {sum(r['area'] for r in rooms)} sq units")

# Convert units (assuming millimeters)
for room in rooms:
    area_sqm = room['area'] / 1_000_000  # mm² to m²
    print(f"Room {room['id'] + 1}: {area_sqm:.2f} m²")