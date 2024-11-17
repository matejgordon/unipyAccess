import logging
import sys

class HardwareManager:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_devices(self):
        endpoint = "/proxy/access/api/v2/devices"
        return self.api_client.get(endpoint)
    
    def get_device(self, device_id):
        endpoint = f"/proxy/access/api/v2/device/{device_id}"
        return self.api_client.get(endpoint)
    
    def restart_device(self, device_id):
        endpoint = f"/proxy/access/api/v2/device/{device_id}/restart"
        return self.api_client.post(endpoint)
    
    def set_access_method(self, device_id, enabled_methods):
        endpoint = f"/proxy/access/api/v2/device/{device_id}/configs"
        payload = []

        methods_map = {
            "nfc": "nfc",
            "wave": "wave",
            "mobile_button": "bt_button",
            "mobile_tap": "bt_tap",
        }

        for method, key in methods_map.items():
            value = "yes" if method in enabled_methods else "no"
            payload.append({"key": key, "tag": "open_door_mode", "value": value})

        if "nfc" in enabled_methods and "wave" in enabled_methods:
            logging.error("Cannot enable both NFC and Wave")
            sys.exit(1)

        device_capabilities = self.get_device(device_id)['data']['capabilities']
        
        if "pin" in enabled_methods and "pin_code" not in device_capabilities:
            logging.error("PIN is not supported on this device")
            sys.exit(1)

        if "wave" in enabled_methods and "sensitivity" not in device_capabilities:
            logging.error("Wave is not supported on this device")
            sys.exit(1)

        response = self.api_client.put(endpoint, payload)
        logging.info(f"Set access method for device {device_id} to {enabled_methods}")
        return response
