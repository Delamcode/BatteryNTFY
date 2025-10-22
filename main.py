import requests
import psutil
import platform
from time import sleep

topic = "battery"
battery_target = 20
force_all_battery = False

uname = platform.uname()
battery_notified = False # if it has been notified that the battery is low
power_plugged_notified = True # the last state, notified when changed

print("Running...")

def get_battery_status():
    """Retrieve the battery percentage using psutil."""
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent
    return null
try:
    while True:
        try:
            sleep(5)
            battery = get_battery_status()
            if (battery < battery_target and battery_notified == False) or force_all_battery == True:
                response = requests.put(
                    f"https://ntfy.sh/{topic}",
                    data=f"Battery on {uname.system} is at {battery}%!",
                    headers={"Title": "Battery Low", "Tags": "battery,rotating_light", "Priority": "max"}
                )
                battery_notified = True
            if (battery > battery_target and battery_notified == True) or force_all_battery == True:
                response = requests.put(
                    f"https://ntfy.sh/{topic}",
                    data=f"Battery on {uname.system} is at {battery}%",
                    headers={"Title": "Battery Charged", "Tags": "battery,white_check_mark", "Priority": "default"}
                )
                battery_notified = False
            force_all_battery = False
            power_plugged = psutil.sensors_battery().power_plugged
            power_plugged_name = "Plugged in" if power_plugged else "Unplugged"
            plugged_priority = "default" if power_plugged else "high"
            plugged_tags = "battery,white_check_mark" if power_plugged else "battery,warning"
            if power_plugged != power_plugged_notified:
                response = requests.put(
                    f"https://ntfy.sh/{topic}",
                    data=f"{uname.system} was {power_plugged_name}!",
                    headers={"Title": f"Device {power_plugged_name}", "Tags": plugged_tags, "Priority": plugged_priority}
                )
                power_plugged_notified = power_plugged
        except KeyboardInterrupt:
            print("Stopping...")
except Exception as e:
    print(f"An error occoured: {e}")
