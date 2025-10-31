import tinytuya
import base64
import json
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

class LiveMapMonitor:
    def __init__(self):
        self.vacuum = tinytuya.Device(
            dev_id="YOUR_DEVICE_ID_HERE",
            address="YOUR_VACUUM_IP_HERE",
            local_key="YOUR_LOCAL_KEY_HERE",
            version=3.3
        )
        self.vacuum.set_socketPersistent(True)
        self.current_map = None
        
    def request_full_map(self):
        """Request the complete map data"""
        print("Requesting full map...")
        
        # Try different request types
        for request_type in ['get_map', 'get_both', 'get_path']:
            try:
                # DPS 121 or 122 seems to work for requests
                result = self.vacuum.set_value(121, request_type)
                print(f"Request '{request_type}': {result}")
                time.sleep(1)
                
                # Check if we got map data in DPS 15
                status = self.vacuum.status()
                if 'dps' in status and '15' in status['dps']:
                    map_data = status['dps']['15']
                    print(f"✓ Got map data: {len(map_data)} chars")
                    return map_data
            except Exception as e:
                print(f"Error with {request_type}: {e}")
        
        return None
    
    def decode_map_data(self, base64_data):
        """Decode map data into rooms"""
        try:
            data = base64.b64decode(base64_data)
            offset = 3  # Skip header
            
            rooms = []
            room_id = 0
            
            while offset < len(data) - 7:
                coords = []
                for _ in range(4):
                    x = int.from_bytes(data[offset:offset+2], 'little', signed=True)
                    y = int.from_bytes(data[offset+2:offset+4], 'little', signed=True)
                    coords.append((x, y))
                    offset += 4
                
                xs = [c[0] for c in coords]
                ys = [c[1] for c in coords]
                
                if len(set(xs)) == 2 and len(set(ys)) == 2:
                    rooms.append({
                        'id': room_id,
                        'min_x': min(xs),
                        'max_x': max(xs),
                        'min_y': min(ys),
                        'max_y': max(ys)
                    })
                    room_id += 1
            
            return rooms
        except Exception as e:
            print(f"Decode error: {e}")
            return []
    
    def monitor_and_visualize(self):
        """Monitor vacuum and show live map"""
        print("Starting live monitor...")
        print("Press Ctrl+C to stop\n")
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        def update(frame):
            # Get current status
            status = self.vacuum.status()
            
            if 'dps' in status:
                # Check for map data
                if '15' in status['dps']:
                    map_data = status['dps']['15']
                    rooms = self.decode_map_data(map_data)
                    
                    if rooms:
                        ax.clear()
                        
                        # Plot rooms
                        for room in rooms:
                            width = room['max_x'] - room['min_x']
                            height = room['max_y'] - room['min_y']
                            
                            rect = patches.Rectangle(
                                (room['min_x'], room['min_y']),
                                width, height,
                                linewidth=2,
                                edgecolor='blue',
                                facecolor='lightblue',
                                alpha=0.3
                            )
                            ax.add_patch(rect)
                        
                        # Show vacuum position if available
                        vac_status = status['dps'].get('5', 'unknown')
                        battery = status['dps'].get('26', 0)
                        
                        ax.set_title(f'Vacuum Map - Status: {vac_status} | Battery: {battery}%', 
                                   fontweight='bold')
                        ax.set_xlabel('X coordinate')
                        ax.set_ylabel('Y coordinate')
                        ax.grid(True, alpha=0.3)
                        ax.set_aspect('equal')
        
        ani = FuncAnimation(fig, update, interval=2000)  # Update every 2 seconds
        plt.show()

# Usage
if __name__ == "__main__":
    print("Choose an option:")
    print("1. Decode current map data")
    print("2. Request and decode full map")
    print("3. Live monitor (experimental)")
    
    choice = input("Choice: ").strip()
    
    if choice == "1":
        # Use the existing map data
        map_data = 'qgABFxeqAAMpAQAqqgBcGwUABAEWAzIDlQMyA5UB2AEWAdgABAW+ArAHIAKwByAAxAW+AMQABP4q/+UAQP/lAED+vf4q/r0ABP+1/KECivyhAor6Bf+1+gUABADk/vUBrv71Aa7+KgDk/iqQqgACEwATqgADFQEAFg=='
        decoder = TuyaRoomMapDecoder(map_data)
        rooms = decoder.decode_rooms()
        decoder.visualize_rooms(rooms)
        
    elif choice == "2":
        monitor = LiveMapMonitor()
        map_data = monitor.request_full_map()
        if map_data:
            decoder = TuyaRoomMapDecoder(map_data)
            rooms = decoder.decode_rooms()
            decoder.visualize_rooms(rooms)
    
    elif choice == "3":
        monitor = LiveMapMonitor()
        monitor.monitor_and_visualize()
