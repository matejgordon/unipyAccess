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

    def get_device_capabilities(self, device_id):
        device_capabilities = self.get_device(device_id)['data']['capabilities']
        return device_capabilities
    
    def get_device_model(self, device_id):
        device_model = self.get_device(device_id)['data']['device_type']
        return device_model
    
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
            "pin": "pin_code",
        }

        for method, key in methods_map.items():
            value = "yes" if method in enabled_methods else "no"
            payload.append({"key": key, "tag": "open_door_mode", "value": value})

        if "nfc" in enabled_methods and "wave" in enabled_methods:
            logging.error("Cannot enable both NFC and Wave")
            sys.exit(1)
        
        device_capabilities = self.get_device_capabilities(device_id)

        if "pin" in enabled_methods and "pin_code" not in device_capabilities:
            logging.error("PIN is not supported on this device")
            sys.exit(1)

        if "wave" in enabled_methods and "sensitivity" not in device_capabilities:
            logging.error("Wave is not supported on this device")
            sys.exit(1)

        response = self.api_client.put(endpoint, payload)
        logging.info(f"Set access method for device {device_id} to {enabled_methods}")
        return response

    def set_doorbell_trigger(self, device_id, doorbell_trigger):

        device_capabilities = self.get_device_capabilities(device_id)

        if "hold_to_call" not in device_capabilities:
            logging.error("Doorbell trigger is not supported on this device")
            sys.exit(1)

        valid_triggers = ["swipe", "tap", "off"]
        if doorbell_trigger not in valid_triggers:
            logging.error(f"Invalid doorbell trigger: {doorbell_trigger}. Must be one of {valid_triggers}")
            sys.exit(1)
    
        endpoint = f"/proxy/access/api/v2/device/{device_id}/configs"
        payload = [{"tag":"device_setting","key":"door_bell_trigger_type","value":doorbell_trigger}]
        response = self.api_client.put(endpoint, payload)
        logging.info(f"Set doorbell trigger for device {device_id} to {doorbell_trigger}")
        return response
    
    def set_status_light(self, device_id, status_light):
        brightness = None

        # Validate input
        if status_light not in ["off", "on"]:
            logging.error(f"Invalid status light: {status_light}. Must be one of ['off', 'on']")
            sys.exit(1)

        device_model = self.get_device_model(device_id)

        if status_light == "on":
            brightness = 20
        elif status_light == "off":
            brightness = 0
            
        if status_light == "on" and device_model == "UA-G2-PRO":
            brightness = "yes"
        elif status_light == "off" and device_model == "UA-G2-PRO":
            brightness = "no"

        endpoint = f"/proxy/access/api/v2/device/{device_id}/configs"

        if device_model == "UA-G2-PRO":
            payload = [{"key": "status_led", "tag": "device_setting", "value": str(brightness)}]
        else:
            payload = [{"key": "brightness", "tag": "device_setting", "value": str(brightness)}]

        # Send request to API
        response = self.api_client.put(endpoint, payload)
        logging.info(f"Set status light for device {device_id} to {status_light}")

        return response
    
    def set_status_sound(self, device_id, status_sound):
        sound = None
        device_model = self.get_device_model(device_id)

        if device_model == "UA-G2-PRO":
            if isinstance(status_sound, int) and 0 <= status_sound <= 100:
                sound = status_sound
            else:
                logging.error(f"Invalid status sound: {status_sound}. For device model {device_model} value must be a number between 0 and 100.")
                return
        else:
            if status_sound == "on":
                sound = "yes"
            elif status_sound == "off":
                sound = "no"
            else:
                logging.error(f"Invalid status sound: {status_sound}. Must be one of ['off', 'on']")
                return

        endpoint = f"/proxy/access/api/v2/device/{device_id}/configs"
        payload = [{"key": "volume", "tag": "device_setting", "value": str(sound)}]
        response = self.api_client.put(endpoint, payload)
        logging.info(f"Set status sound for device {device_id} to {status_sound}")
        return response

    def set_display_brightness(self, device_id, brightness):
        device_model = self.get_device_model(device_id)

        unsupported_models = ["UA-G2-MINI"]
        if device_model in unsupported_models:
            logging.error(f"Display brightness is not supported on this device")
            sys.exit(1)

        if not isinstance(brightness, int) or not 0 <= brightness <= 100:
            logging.error(f"Invalid display brightness: {brightness}. Must be a number between 0 and 100.")
            sys.exit(1)

        endpoint = f"/proxy/access/api/v2/device/{device_id}/configs"
        payload = [{"key": "brightness", "tag": "device_setting", "value": str(brightness)}]
        response = self.api_client.put(endpoint, payload)
        logging.info(f"Set display brightness for device {device_id} to {brightness}")
        return response