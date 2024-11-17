import logging
import sys

class HardwareManager:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_devices(self):
        endpoint = "/proxy/access/api/v2/devices"
        return self.api_client.get(endpoint)
    
    def restart_device(self, device_id):
        endpoint = f"/proxy/access/api/v2/device/{device_id}/restart"
        return self.api_client.post(endpoint)
    
    def set_access_method(self, device_id, enabled_methods):
        endpoint = f"/proxy/access/api/v2/device/{device_id}/configs"
        payload = []

        if "nfc" in enabled_methods:
            payload.append({"key":"nfc","tag":"open_door_mode","value":"yes"})
        elif "nfc" not in enabled_methods:
            payload.append({"key":"nfc","tag":"open_door_mode","value":"no"})
        if "wave" in enabled_methods:
            payload.append({"key":"wave","tag":"open_door_mode","value":"yes"})
        elif "wave" not in enabled_methods:
            payload.append({"key":"wave","tag":"open_door_mode","value":"no"})
        if "mobile_button" in enabled_methods:
            payload.append({"key":"bt_button","tag":"open_door_mode","value":"yes"})
        elif "mobile_button" not in enabled_methods:
            payload.append({"key":"bt_button","tag":"open_door_mode","value":"no"})

        if "nfc" in enabled_methods and "wave" in enabled_methods:
            logging.error('Cannot enable both NFC and Wave')
            sys.exit(1)

        print(payload)

        return self.api_client.put(endpoint, payload)