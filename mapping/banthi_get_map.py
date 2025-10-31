import tinytuya
import json
import base64
import time
import struct

class VacuumMapper:
    def __init__(self):
        # TODO: Replace with your device credentials
        self.vacuum = tinytuya.Device(
            dev_id="YOUR_DEVICE_ID_HERE",
            address="YOUR_VACUUM_IP_HERE",
            local_key="YOUR_LOCAL_KEY_HERE",
            version=3.3
        )
        self.vacuum.set_socketPersistent(True)
    
    def request_map(self, request_type="get_both"):
        """
        Request map data
        request_type: 'get_map', 'get_path', or 'get_both'
        """
        print(f"Requesting: {request_type}")
        
        # Find the DPS for 'request' function
        # Common DPS for map requests: 106, 121, 122, 123
        for dps in [106, 121, 122, 123, 'request']:
            try:
                result = self.vacuum.set_value(dps, request_type)
                print(f"DPS {dps}: {result}")
                time.sleep(2)
            except Exception as e:
                print(f"DPS {dps} failed: {e}")
    
    def get_path_data(self):
        """Get path data (DPS for path_data)"""
        # Common DPS: 107, 110, 111, 112
        for dps in [107, 110, 111, 112, 'path_data']:
            try:
                result = self.vacuum.get_value(dps)
                if result:
                    print(f"\nPath data from DPS {dps}:")
                    print(f"Type: {type(result)}")
                    print(f"Length: {len(str(result))}")
                    
                    if isinstance(result, str):
                        # Try to decode base64
                        try:
                            decoded = base64.b64decode(result)
                            self.save_map_data(decoded, f'path_{dps}.bin')
                            self.analyze_map_format(decoded)
                        except:
                            print(f"Raw data: {result[:200]}...")
                    else:
                        print(f"Data: {result}")
            except Exception as e:
                pass
    
    def monitor_for_map(self, duration=60):
        """Monitor all DPS updates for map data"""
        print(f"Monitoring for {duration} seconds...")
        print("Now open the Smart Life app and view the map!")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                data = self.vacuum.receive()
                if data and 'dps' in data:
                    for key, value in data['dps'].items():
                        # Look for large data (maps)
                        if isinstance(value, str) and len(value) > 100:
                            print(f"\n[Map Data Found] DPS {key}")
                            print(f"Length: {len(value)} bytes")
                            
                            # Try to decode
                            try:
                                decoded = base64.b64decode(value)
                                filename = f'map_dps_{key}_{int(time.time())}.bin'
                                self.save_map_data(decoded, filename)
                                self.analyze_map_format(decoded)
                            except:
                                filename = f'map_dps_{key}_{int(time.time())}.txt'
                                with open(filename, 'w') as f:
                                    f.write(value)
                                print(f"Saved as text to {filename}")
                
                time.sleep(0.5)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
    
    def save_map_data(self, data, filename):
        """Save binary map data"""
        with open(filename, 'wb') as f:
            f.write(data)
        print(f"✓ Saved to {filename}")
    
    def analyze_map_format(self, data):
        """Analyze map data format"""
        print("\n=== Map Data Analysis ===")
        print(f"Total size: {len(data)} bytes")
        
        # Check header (first 16 bytes)
        if len(data) >= 16:
            header = data[:16]
            print(f"Header (hex): {header.hex()}")
            print(f"Header (ascii): {header}")
            
            # Try to parse as different formats
            # Common formats: PNG, JSON, proprietary binary
            
            # Check for PNG signature
            if data[:8] == b'\x89PNG\r\n\x1a\n':
                print("✓ Format: PNG image!")
                with open('map.png', 'wb') as f:
                    f.write(data)
                print("Saved as map.png")
            
            # Check for JSON
            elif data[0:1] == b'{':
                try:
                    json_data = json.loads(data.decode('utf-8'))
                    print("✓ Format: JSON!")
                    print(json.dumps(json_data, indent=2))
                except:
                    pass
            
            # Check for Tuya's proprietary format
            else:
                # Try to parse as structured data
                try:
                    # Common structure: [header][width][height][data]
                    if len(data) >= 8:
                        width = struct.unpack('<I', data[0:4])[0]
                        height = struct.unpack('<I', data[4:8])[0]
                        print(f"Possible dimensions: {width}x{height}")
                        
                        if width < 10000 and height < 10000:  # Sanity check
                            print("✓ Likely a bitmap grid map")
                            self.decode_bitmap_map(data, width, height)
                except:
                    print("Unknown format - saved as binary")
    
    def decode_bitmap_map(self, data, width, height):
        """Try to decode as bitmap grid map"""
        try:
            # Skip header (usually 8-16 bytes)
            offset = 16
            map_data = data[offset:]
            
            expected_size = width * height
            print(f"Expected map size: {expected_size} bytes")
            print(f"Actual data size: {len(map_data)} bytes")
            
            # Save as PGM (Portable Gray Map) - ROS compatible!
            if len(map_data) >= expected_size:
                with open('map.pgm', 'wb') as f:
                    f.write(f'P5\n{width} {height}\n255\n'.encode())
                    f.write(map_data[:expected_size])
                print("✓ Saved as map.pgm (ROS-compatible format)")
        except Exception as e:
            print(f"Bitmap decode failed: {e}")

# Usage
if __name__ == "__main__":
    mapper = VacuumMapper()
    
    print("="*60)
    print("VACUUM MAPPER")
    print("="*60)
    print("\n1. Request Map Data")
    print("2. Monitor for Map Updates (60s)")
    print("3. Get Current Path Data")
    print("4. Manual Control Test")
    
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        mapper.request_map("get_both")
        time.sleep(3)
        mapper.get_path_data()
    
    elif choice == "2":
        print("\nStarting monitor...")
        print("Open Smart Life app and view the map NOW!")
        mapper.monitor_for_map(60)
    
    elif choice == "3":
        mapper.get_path_data()
    
    elif choice == "4":
        # Test manual control
        print("Testing manual control...")
        mapper.vacuum.set_value('direction_control', 'forward')
        time.sleep(2)
        mapper.vacuum.set_value('direction_control', 'stop')