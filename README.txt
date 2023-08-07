AnonMac - Version 1.0
Developed by: TheUnknownDev

Summary:
AnonMac is a powerful script designed to enhance user anonymity by periodically changing their MAC address or allowing customization based on user preference. The script intelligently tests various generated MAC addresses for speed and ping performance, applying the best one to the specified interface. For added privacy, AnonMac also offers utilities to perform cleanup operations.

Usage:
To run the script, execute it using Python 3: python3 AnonMac.py

Follow the on-screen instructions to select your desired test method and MAC change frequency.

Optionally, utilize the cleanup operations as prompted.

Important Notes:

Network Disruptions:

Please be aware that running speed tests can saturate your network and may cause temporary disruptions.

Changing the MAC address will momentarily disconnect you from the network. If you are connected via SSH or any remote management tool, you may lose your connection.

Using AnonMac on VPS/Remote Servers:

Exercise caution when using this script on a VPS or remote server, as changing the MAC address might result in disconnection.

In case of disconnection without the ability to reconnect, consider performing a server reboot from the VPS control panel.

Always ensure you have an alternative way to manage your VPS outside of SSH, such as a web control panel, before executing this script.

The script offers utilities to:

Flush the DNS cache
Clear the ARP cache
Clear temporary files
Using these utilities can enhance anonymity but may also disrupt ongoing network activities.

Crontab:
The script can set up a cron job to change the MAC address at specified intervals. Make sure that you have cron installed and running on your system.

Known Issues:
Network Interruptions: During testing and MAC address changes, you might experience brief network interruptions.

VPS/Remote Servers: Changing the MAC on a VPS or remote server can lead to disconnection. Ensure you have an alternate way to access the server.

To remove the cron job set by the script, follow these steps:

Open your crontab in the default text editor:

crontab -e

Look for the line that runs the AnonMac.py script and delete it.

Save and exit the editor.

The cron job is now removed, and the script will no longer run at the previously specified intervals.

If you are not familiar with the vi editor (which is often the default for crontab -e), you can temporarily change the default editor to a more familiar one like nano:

export VISUAL=nano; crontab -e

This will open the crontab in nano, which some users find more intuitive than vi.

Feel free to update the script as needed in the future, and enjoy the added anonymity it provides. Much love!