![licence](https://img.shields.io/badge/license-MIT-green)
![issues](https://img.shields.io/github/issues/matejgordon/unipyaccess)
[![deploy](https://img.shields.io/github/actions/workflow/status/matejgordon/unipyaccess/deploy.yml)](https://github.com/matejgordon/unipyaccess/actions/workflows/deploy.yml) 
![tag](https://img.shields.io/github/v/tag/matejgordon/unipyaccess)

# unipyaccess

`unipyaccess` is a Python package designed to interface with the **Unifi Access** system. This package provides a simple and efficient way to manage users in Unifi Access, including authentication, retrieval, creation, activation, deactivation, deletion, and updating of user groups.

> [!NOTE]  
> This implementation uses Unifi API endpoints with admin user authentication. It does **not** utilize the latest, in my opinion half-baked Unifi API.

> [!WARNING]  
> 🚧 This project is under active development, and breaking changes are expected in upcoming releases.


# NEW DOCUMENTATION WIP

```
unipy = UnipyAccess(base_url=os.getenv('UNIFI_CONTROLLER_ADDRESS'),username=os.getenv("UNIFI_LOGIN"),password=os.getenv('UNIFI_PASSWORD'), verify=os.getenv('VERIFY_SSL'))

#Features
users = unipy.users.get_users()

new_user = {
    "first_name": "Python",
    "last_name": "Test",
    "PersonId": 98765,
}

unipy.users.create_user(new_user)
unipy.users.deactivate_user(uuid)
unipy.users.activate_user(uuid)
unipy.users.set_user_group(uuid, group_uuid)
unipy.users.delete_user(uuid)

unipy.hardware.get_devices()
unipy.hardware.get_device(device_id)
unipy.hardware.set_access_method(device_id,["pin", "nfc", "mobile_tap", "mobile_button"])
unipy.hardware.set_doorbell_trigger(device_id, "tap")
unipy.hardware.set_status_light(device_id, "on")
unipy.hardware.set_display_brightness(device_id, 50)
unipy.hardware.set_status_sound("f4e2c6d3085d", 30) #For models other than UA G2 Pro use "on" or "off"
unipy.hardware.get_device_capabilities(device_id)
unipy.hardware.get_device_model(device_id)
unipy.hardware.restart_device(device_id)
```
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
