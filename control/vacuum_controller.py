import tinytuya
import json
import time

class EurekaLVACVoiceProController:
    def __init__(self):
        # TODO: Replace with your device credentials
        # Get these from: https://iot.tuya.com or see docs/SETUP_GUIDE.md
        self.vacuum = tinytuya.Device(
            dev_id="YOUR_DEVICE_ID_HERE",           # e.g., "d7921b8722a14bbf3da8di"
            address="YOUR_VACUUM_IP_HERE",          # e.g., "192.168.1.100"
            local_key="YOUR_LOCAL_KEY_HERE",        # e.g., "Vwel'|(#;Nkbc{^o"
            version=3.3
        )
        self.vacuum.set_socketPersistent(True)
    
    def get_status(self):
        """Get current vacuum status"""
        status = self.vacuum.status()
        if 'dps' in status:
            dps = status['dps']
            return {
                'power': dps.get('1', False),
                'status': dps.get('5', 'unknown'),
                'command': dps.get('4', 'unknown'),
                'battery': dps.get('26', 0),
                'suction_mode': dps.get('9', 'unknown'),
                'water_level': dps.get('10', 'unknown'),
                'side_brush_life': dps.get('7', 0),
                'filter_life': dps.get('8', 0),
                'main_brush_life': dps.get('29', 0),
                'cleaning_time': dps.get('17', 0),
                'cleaning_area': dps.get('21', 0),
                'total_cleanings': dps.get('30', 0),
                'total_area': dps.get('31', 0),
                'error_code': dps.get('102', 0),
                'auto_boost': dps.get('103', False),
                'dnd_mode': dps.get('27', False),
                'map_id': dps.get('199', '0')
            }
        return status
    
    def start_cleaning(self):
        """Start automatic cleaning"""
        print("Starting cleaning...")
        return self.vacuum.set_value('1', True)
    
    def stop_cleaning(self):
        """Stop cleaning"""
        print("Stopping...")
        return self.vacuum.set_value('1', False)
    
    def pause_cleaning(self):
        """Pause cleaning"""
        print("Pausing...")
        return self.vacuum.set_value('2', True)
    
    def return_to_dock(self):
        """Return to charging dock"""
        print("Returning to dock...")
        return self.vacuum.set_value('4', 'chargego')
    
    def set_suction_mode(self, mode):
        """
        Set suction power mode
        Options: 'gentle', 'normal', 'max'
        """
        valid_modes = ['gentle', 'normal', 'max']
        if mode not in valid_modes:
            print(f"Invalid mode. Choose from: {valid_modes}")
            return
        print(f"Setting suction to {mode}...")
        return self.vacuum.set_value('9', mode)
    
    def set_water_level(self, level):
        """
        Set water/mop level
        Options: 'low', 'medium', 'high'
        """
        valid_levels = ['low', 'medium', 'high']
        if level not in valid_levels:
            print(f"Invalid level. Choose from: {valid_levels}")
            return
        print(f"Setting water level to {level}...")
        return self.vacuum.set_value('10', level)
    
    def find_robot(self):
        """Make robot beep to locate it"""
        print("Finding robot (beeping)...")
        self.vacuum.set_value('25', True)
        time.sleep(2)
        return self.vacuum.set_value('25', False)
    
    def set_dnd_mode(self, enabled):
        """Enable/disable Do Not Disturb mode"""
        print(f"Setting DND mode: {enabled}")
        return self.vacuum.set_value('27', enabled)
    
    def set_auto_boost(self, enabled):
        """Enable/disable auto carpet boost"""
        print(f"Setting auto boost: {enabled}")
        return self.vacuum.set_value('103', enabled)
    
    def get_maintenance_status(self):
        """Get maintenance information"""
        status = self.vacuum.status()
        if 'dps' in status:
            dps = status['dps']
            return {
                'side_brush': f"{dps.get('7', 0)}% life remaining",
                'filter': f"{dps.get('8', 0)}% life remaining",
                'main_brush': f"{dps.get('29', 0)} cycles remaining"
            }
        return {}
    
    def print_status(self):
        """Print formatted status"""
        status = self.get_status()
        print("\n" + "="*50)
        print("VACUUM STATUS")
        print("="*50)
        print(f"Power:          {status['power']}")
        print(f"Status:         {status['status']}")
        print(f"Command:        {status['command']}")
        print(f"Battery:        {status['battery']}%")
        print(f"Suction Mode:   {status['suction_mode']}")
        print(f"Water Level:    {status['water_level']}")
        print(f"DND Mode:       {status['dnd_mode']}")
        print(f"Auto Boost:     {status['auto_boost']}")
        print("\nMAINTENANCE:")
        print(f"Side Brush:     {status['side_brush_life']}%")
        print(f"Filter:         {status['filter_life']}%")
        print(f"Main Brush:     {status['main_brush_life']} cycles")
        print("\nSTATISTICS:")
        print(f"Current Clean:  {status['cleaning_time']}s / {status['cleaning_area']}m²")
        print(f"Total Cleans:   {status['total_cleanings']}")
        print(f"Total Area:     {status['total_area']}m²")
        print(f"Error Code:     {status['error_code']}")
        print("="*50 + "\n")

# Interactive Menu
def main():
    controller = EurekaLVACVoiceProController()
    
    while True:
        print("\n" + "="*50)
        print("EUREKA FORBES LVAC VOICE PRO CONTROLLER")
        print("="*50)
        print("1.  Show Status")
        print("2.  Start Cleaning")
        print("3.  Stop/Pause")
        print("4.  Return to Dock")
        print("5.  Set Suction Mode (gentle/normal/max)")
        print("6.  Set Water Level (low/medium/high)")
        print("7.  Find Robot (Beep)")
        print("8.  Toggle DND Mode")
        print("9.  Toggle Auto Boost")
        print("10. Maintenance Status")
        print("0.  Exit")
        print("="*50)
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            controller.print_status()
        elif choice == '2':
            controller.start_cleaning()
            time.sleep(2)
            controller.print_status()
        elif choice == '3':
            controller.stop_cleaning()
            time.sleep(2)
            controller.print_status()
        elif choice == '4':
            controller.return_to_dock()
            time.sleep(2)
            controller.print_status()
        elif choice == '5':
            mode = input("Enter mode (gentle/normal/max): ").strip()
            controller.set_suction_mode(mode)
            time.sleep(2)
            controller.print_status()
        elif choice == '6':
            level = input("Enter level (low/medium/high): ").strip()
            controller.set_water_level(level)
            time.sleep(2)
            controller.print_status()
        elif choice == '7':
            controller.find_robot()
        elif choice == '8':
            enabled = input("Enable DND? (y/n): ").strip().lower() == 'y'
            controller.set_dnd_mode(enabled)
        elif choice == '9':
            enabled = input("Enable Auto Boost? (y/n): ").strip().lower() == 'y'
            controller.set_auto_boost(enabled)
        elif choice == '10':
            maintenance = controller.get_maintenance_status()
            print("\nMaintenance Status:")
            for key, value in maintenance.items():
                print(f"  {key}: {value}")
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()