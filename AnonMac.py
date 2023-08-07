#------------------------------------------#
#   ANONMAC v1.0                           #
#   Created by: TheUnknownDev              #
#   Change your MAC with ease & style!     #
#------------------------------------------#

import os
import random
import subprocess
import time

# Functions for generating and testing MAC addresses
def generate_mac_address():
    """Generate a random MAC address."""
    # Ensure the first byte is even for valid MAC addresses
    mac = [random.randint(0, 254) & 0b11111110]
    for _ in range(5):
        mac.append(random.randint(0, 255))
    return ":".join(["{:02x}".format(byte) for byte in mac])

def test_mac_speed():
    """Run the speedtest-cli tool to measure download and upload speeds."""
    try:
        results = subprocess.check_output(["speedtest-cli", "--simple"]).decode('utf-8')
        download_speed = float(results.split("Download: ")[1].split(" Mbit/s")[0])
        upload_speed = float(results.split("Upload: ")[1].split(" Mbit/s")[0])
        return download_speed + upload_speed
    except Exception as e:
        print(f"Error during speed test: {e}")
        return 0

def apply_mac_address(interface, mac_address):
    """Apply the given MAC address to the specified interface."""
    try:
        os.system(f"sudo ifconfig {interface} down")
        os.system(f"sudo ifconfig {interface} hw ether {mac_address}")
        os.system(f"sudo ifconfig {interface} up")
        return True
    except:
        return False

def select_best_mac(interface='eth0'):
    """Test multiple MAC addresses and select the best one based on speed."""
    mac_addresses = [generate_mac_address() for _ in range(5)]
    best_score = 0
    best_mac = None
    for mac in mac_addresses:
        apply_mac_address(interface, mac)
        time.sleep(5)  # Give the network some time to adjust after the MAC change
        score = test_mac_speed()
        if score > best_score:
            best_score = score
            best_mac = mac
    return best_mac

# Functions for checking prerequisites and providing installation instructions
def check_prerequisites():
    """Check for required tools and utilities."""
    missing_tools = []
    if os.system("which ifconfig") != 0 and os.system("which ip") != 0:
        missing_tools.append("ifconfig/ip")
    if os.system("which speedtest-cli") != 0:
        missing_tools.append("speedtest-cli")
    if os.system("which crontab") != 0:
        missing_tools.append("crontab")
    return missing_tools

def provide_installation_instructions(missing_tools):
    """Provide instructions to install the missing tools."""
    instructions = []
    if "ifconfig/ip" in missing_tools:
        instructions.append("Install net-tools for ifconfig or iproute2 for ip. On Debian/Ubuntu: sudo apt-get install net-tools iproute2")
    if "speedtest-cli" in missing_tools:
        instructions.append("Install speedtest-cli using pip: pip install speedtest-cli")
    if "crontab" in missing_tools:
        instructions.append("Crontab is typically pre-installed on many systems. If missing, install cron. On Debian/Ubuntu: sudo apt-get install cron")
    return instructions

# Functions for setting up MAC change frequency
def setup_mac_change_frequency():
    """Ask the user about the frequency of MAC address changes and set up the corresponding cron job."""
    print("\nHow often would you like to change the MAC address?")
    choices = ["Every few minutes", "Every few hours", "Every day", "On every reboot", "Just once (No recurring change)"]
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    user_choice = input("Enter your choice (1/2/3/4/5): ")
    script_path = os.path.realpath(__file__)
    cron_command = ""
    if user_choice == "1":
        minutes = input("Enter the number of minutes between each change: ")
        cron_command = f"*/{minutes} * * * * python3 {script_path}"
    elif user_choice == "2":
        hours = input("Enter the number of hours between each change: ")
        cron_command = f"0 */{hours} * * * python3 {script_path}"
    elif user_choice == "3":
        cron_command = f"0 0 * * * python3 {script_path}"
    elif user_choice == "4":
        cron_command = f"@reboot python3 {script_path}"
    elif user_choice == "5":
        print("The MAC address will be changed just once. No recurring changes will be set up.")
        return
    else:
        print("Invalid choice.")
        return

    # Update the cron jobs while ensuring the script is not already scheduled
    os.system(f"(crontab -l | grep -v '{script_path}'; echo \"{cron_command}\") | crontab")
    print("MAC change frequency set successfully!")


# Functions for cleanup and anonymity maintenance
def flush_dns_cache():
    """Flush the DNS cache."""
    os.system("sudo systemd-resolve --flush-caches")

def clear_arp_cache():
    """Clear the ARP cache."""
    os.system("sudo ip -s -s neigh flush all")

def clear_temp_files():
    """Clear temporary files."""
    os    .system("sudo rm -rf /tmp/*")

def perform_cleanup():
    """Perform cleanup operations for enhanced anonymity."""
    flush_dns_cache()
    clear_arp_cache()
    clear_temp_files()
    print("Cleanup completed!")

def get_mac_address(interface):
    """Retrieve the current MAC address for a given interface."""
    try:
        result = subprocess.check_output(f"ifconfig {interface} | grep ether | awk '{{print $2}}'", shell=True).decode('utf-8').strip()
        return result
    except:
        return None

def get_network_interfaces():
    """Retrieve a list of available network interfaces."""
    try:
        result = subprocess.check_output("ip -br link show up", shell=True).decode('utf-8')
        interfaces = [line.split()[0] for line in result.strip().split('\n')]
        return interfaces
    except:
        return []

def get_interface_ip_addresses():
    """Retrieve IP addresses for available network interfaces."""
    try:
        result = subprocess.check_output("ip -br addr show up", shell=True).decode('utf-8')
        lines = result.strip().split('\n')
        ip_map = {}
        for line in lines:
            parts = line.split()
            interface = parts[0]
            ip_address = parts[2] if len(parts) > 2 else "No IP"
            ip_map[interface] = ip_address
        return ip_map
    except:
        return {}
    
def flush_dns_cache():
    """Flush the DNS cache."""
    if os.system("which systemd-resolve") == 0:
        os.system("sudo systemd-resolve --flush-caches")
    else:
        print("Warning: Unable to find 'systemd-resolve'. DNS cache might not have been flushed.")


# Main function with debug points
def main():
    print("[DEBUG] Starting the script...")
    
    # Check prerequisites
    missing = check_prerequisites()
    if missing:
        print("[DEBUG] Missing tools detected.")
        instructions = provide_installation_instructions(missing)
        for instruction in instructions:
            print(instruction)
        return
    else:
        print("[DEBUG] All required tools are installed!")

    # Retrieve interface and its MAC address
    ip_map = get_interface_ip_addresses()
    interfaces = list(ip_map.keys())
    if not interfaces:
        print("[DEBUG] No active network interfaces detected.")
        return

    # If 'eth0' is not in the list, prompt the user to choose an interface
    if 'eth0' not in interfaces:
        print("[DEBUG] The default 'eth0' interface was not found. Please choose from the available interfaces:")
        for i, iface in enumerate(interfaces, 1):
            print(f"{i}. {iface} - IP: {ip_map[iface]}")
        choice = int(input("Enter the number of your choice: "))
        interface = interfaces[choice-1]
    else:
        interface = "eth0"

    current_mac = get_mac_address(interface)
    print(f"Current MAC address for {interface}: {current_mac}")
    
    # Test and apply best MAC
    print("[DEBUG] Testing MAC addresses...")

    # Display the warning in orange color
    print("Running a speed test can saturate your network and might cause temporary disruptions.")
    print("Choose a test method:")
    print("1. Speed test (comprehensive, may disrupt network) - Expected time: 1-10 mins")
    print("2. Ping test (less disruptive) - Expected time: 10 secs - 5 mins")
    print("3. Both (speed test followed by ping test) - Expected time: 1-10 mins")
    print("4. Skip tests (choose MAC randomly)")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        best_mac = select_best_mac(interface)
    elif choice == "2":
        # For now, we'll just choose a random MAC if they choose ping test. 
        # This can be expanded later to do ping tests.
        best_mac = generate_mac_address()
    elif choice == "3":
        best_mac = select_best_mac(interface)  # This can be modified to do both tests sequentially
    elif choice == "4":
        best_mac = generate_mac_address()
    else:
        print("Invalid choice.")
        return

    print(f"[DEBUG] Applying MAC address {best_mac} to {interface}...")
    if apply_mac_address(interface, best_mac):
        print(f"Successfully applied the best MAC address ({best_mac}) to {interface}.")
    else:
        print(f"Failed to apply the MAC address to {interface}.")

    # Setting up the MAC change frequency
    setup_mac_change_frequency()
    
    # Cleanup and anonymity maintenance
    choice = input("\nWould you like to perform cleanup operations for enhanced anonymity? (yes/no): ").lower()
    if choice == 'yes':
        print("[DEBUG] Performing cleanup operations...")
        perform_cleanup()

    print("[DEBUG] Script execution completed.")


# To run the script
if __name__ == '__main__':
    main()