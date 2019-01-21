import os
import subprocess
import json
import time

MOUNT_DIR = "/media/usb"
WPA_SUPPLICANT_FILE = "/etc/wpa_supplicant/wpa_supplicant.conf"

def mount_usb():
    if not os.path.exists(MOUNT_DIR):
        os.makedirs(MOUNT_DIR)
    cmd = "mount /dev/sda1 %s" % MOUNT_DIR
    subprocess.call(cmd, shell=True)
    print('%s mounted' % MOUNT_DIR)

def get_creds():
    wifi_path = os.path.join(MOUNT_DIR, "wifi.json")
    if os.path.exists(wifi_path):
        with open(wifi_path) as f:
            wifi_json = json.loads(f.read())
            return wifi_json["ssid"], wifi_json["psk"]
    return None, None

def already_has_creds(ssid, psk):
    if os.path.exists(WPA_SUPPLICANT_FILE):
        with open(WPA_SUPPLICANT_FILE, "r") as f:
            existing = f.read()
        return  ssid in existing and psk in existing
    else:
        return False

def add_creds(ssid, psk):
    cmd = 'wpa_passphrase "%s" "%s" >> /etc/wpa_supplicant/wpa_supplicant.conf' % (ssid, psk)
    subprocess.call(cmd, shell=True)
    time.sleep(1)
    cmd = "sudo wpa_cli reconfigure"
    subprocess.call(cmd, shell=True)
    time.sleep(3)

if __name__ == '__main__':
    mount_usb()
    # TODO change_hostname
    # TODO authorisation
    ssid, psk = get_creds()
    if ssid is not None and not already_has_creds(ssid, psk):
        print("Adding SSID=%s and PASSWORD=%s to wpa_supplicant.conf" % (ssid, psk))
        add_creds(ssid, psk)
