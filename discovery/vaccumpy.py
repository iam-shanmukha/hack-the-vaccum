import socket
import struct
from datetime import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 6667))

print("Listening for Eureka Forbes LVAC Voice Pro broadcasts...")
print("Press Ctrl+C to stop\n")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"[{timestamp}] Packet from {addr[0]}:{addr[1]}")
        print(f"Length: {len(data)} bytes")
        
        # Look for magic bytes
        if data[0:2] == b'\x00\x00' and data[2:4] == b'\x55\xaa':
            print("✓ Magic header found: 0x55aa")
            
            # Try to parse header
            if len(data) >= 16:
                packet_type = struct.unpack('>H', data[10:12])[0]
                length = struct.unpack('>H', data[14:16])[0]
                print(f"  Packet type: 0x{packet_type:04x} ({packet_type})")
                print(f"  Payload length: {length}")
        
        # Check for magic footer
        if data[-4:-2] == b'\xaa\x55':
            print("✓ Magic footer found: 0xaa55")
        
        # Print hex dump
        print("\nHex dump:")
        for i in range(0, len(data), 16):
            hex_str = ' '.join(f'{b:02x}' for b in data[i:i+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
            print(f"  {i:04x}: {hex_str:<48} {ascii_str}")
        
        print("-" * 80)
        
except KeyboardInterrupt:
    print("\nStopped listening")
finally:
    sock.close()