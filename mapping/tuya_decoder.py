import base64
import struct
import json
import zlib

class TuyaMapDecoder:
    def __init__(self, base64_data):
        self.data = base64.b64decode(base64_data)
        self.offset = 0
        
    def read_byte(self):
        val = self.data[self.offset]
        self.offset += 1
        return val
    
    def read_uint16(self):
        val = struct.unpack('<H', self.data[self.offset:self.offset+2])[0]
        self.offset += 2
        return val
    
    def read_int16(self):
        val = struct.unpack('<h', self.data[self.offset:self.offset+2])[0]
        self.offset += 2
        return val
    
    def read_uint32(self):
        val = struct.unpack('<I', self.data[self.offset:self.offset+4])[0]
        self.offset += 4
        return val
    
    def decode(self):
        print("="*60)
        print("TUYA MAP DECODER")
        print("="*60)
        
        result = {
            'raw_size': len(self.data),
            'hex_preview': self.data[:32].hex(),
        }
        
        try:
            # Parse header
            magic = self.read_uint16()
            result['magic'] = f"0x{magic:04x}"
            print(f"Magic: {result['magic']}")
            
            # Version or type
            version = self.read_byte()
            result['version'] = version
            print(f"Version/Type: {version}")
            
            # Parse based on common patterns
            # Pattern 1: Path data (list of coordinates)
            if magic == 0x00aa or magic == 0xaa00:
                result['type'] = 'path'
                coords = []
                
                while self.offset < len(self.data) - 3:
                    x = self.read_int16()
                    y = self.read_int16()
                    coords.append([x, y])
                
                result['coordinates'] = coords
                result['point_count'] = len(coords)
                print(f"Path with {len(coords)} points")
            
            # Pattern 2: Compressed map
            elif magic == 0x1f8b:  # gzip magic
                result['type'] = 'compressed'
                try:
                    decompressed = zlib.decompress(self.data)
                    result['decompressed_size'] = len(decompressed)
                    print(f"Compressed map, decompressed to {len(decompressed)} bytes")
                    
                    with open('map_decompressed.bin', 'wb') as f:
                        f.write(decompressed)
                except:
                    print("Decompression failed")
            
            else:
                result['type'] = 'unknown'
                print("Unknown format")
                
        except Exception as e:
            print(f"Parse error: {e}")
            result['error'] = str(e)
        
        return result

# Decode the actual data
map_data_b64 = 'qgABFxeqAAMpAQAqqgBcGwUABAEWAzIDlQMyA5UB2AEWAdgABAW+ArAHIAKwByAAxAW+AMQABP4q/+UAQP/lAED+vf4q/r0ABP+1/KECivyhAor6Bf+1+gUABADk/vUBrv71Aa7+KgDk/iqQqgACEwATqgADFQEAFg=='

decoder = TuyaMapDecoder(map_data_b64)
result = decoder.decode()

print("\n" + json.dumps(result, indent=2))

with open('map_decoded.json', 'w') as f:
    json.dump(result, f, indent=2)
print("\n✓ Saved to map_decoded.json")