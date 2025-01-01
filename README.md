![licence](https://img.shields.io/badge/license-MIT-green)
![issues](https://img.shields.io/github/issues/matejgordon/unipyaccess)
[![deploy](https://img.shields.io/github/actions/workflow/status/matejgordon/unipyaccess/deploy.yml)](https://github.com/matejgordon/unipyaccess/actions/workflows/deploy.yml)
![tag](https://img.shields.io/github/v/tag/matejgordon/unipyaccess)

# unipyaccess

`unipyaccess` is a Python package designed to interface with the **Unifi Access** system. This package provides a simple and efficient way to manage users in Unifi Access, including authentication, retrieval, creation, activation, deactivation, deletion, and updating of user groups and hardware settings.

> [!NOTE]  
> This implementation uses Unifi API endpoints with admin user authentication. It does **not** utilize the latest, in my opinion half-baked Unifi API.

> [!WARNING]  
> 🚧 This project is under active development, and breaking changes are expected in upcoming releases.

## Features

- Authenticate with Unifi Access using admin credentials.
- Retrieve, create, activate, deactivate, and delete user accounts.
- Update user group assignments.
- Manage Unifi Access hardware, including access methods, display brightness, and device status.

## Installation

Install the package via `pip`:

```bash
pip install unipyaccess
```

## Requirements

- Python 3.x
- `requests` library

Install the requirements with:

```bash
pip install requests
```

## Environment Setup

Store your configuration details in a `.env` file:

```bash
UNIFI_CONTROLLER_ADDRESS=https://unifi-controller.local
UNIFI_LOGIN=admin
UNIFI_PASSWORD=password123
VERIFY_SSL=False
```

## Usage

Import `unipyaccess` and use it in your Python script:

```python
from unipyaccess import UnipyAccess
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the UnipyAccess API client
unipy = UnipyAccess(
    base_url=os.getenv('UNIFI_CONTROLLER_ADDRESS'),
    username=os.getenv('UNIFI_LOGIN'),
    password=os.getenv('UNIFI_PASSWORD'),
    verify=os.getenv('VERIFY_SSL')
)

# Features
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

# Hardware management
devices = unipy.hardware.get_devices()

unipy.hardware.get_device(device_id)
unipy.hardware.set_access_method(device_id, ["pin", "nfc", "mobile_tap", "mobile_button"])
unipy.hardware.set_doorbell_trigger(device_id, "tap")
unipy.hardware.set_status_light(device_id, "on")
unipy.hardware.set_display_brightness(device_id, 50)
unipy.hardware.set_status_sound("f4e2c6d3085d", 30)  # For models other than UA G2 Pro use "on" or "off"
unipy.hardware.get_device_capabilities(device_id)
unipy.hardware.get_device_model(device_id)
unipy.hardware.restart_device(device_id)
```

## Methods

### User Management

#### 1. `unipy.users.create_user(new_user)`
Creates a new user.

**Parameters:**
- `new_user` (dict): Dictionary containing user details:
  - `first_name` (str): User's first name.
  - `last_name` (str): User's last name.
  - `PersonId` (str): Optional employee number.
  - `group_ids` (list): Optional list of group IDs.

**Usage:**

```python
new_user = {
    "first_name": "Jane",
    "last_name": "Doe",
    "PersonId": "789",
    "group_ids": ["group-123"]
}
unipy.users.create_user(new_user)
```

#### 2. `unipy.users.deactivate_user(uuid)`
Deactivates a user.

**Parameters:**
- `uuid` (str): User’s unique identifier.

**Usage:**

```python
unipy.users.deactivate_user("user-123")
```

#### 3. `unipy.users.activate_user(uuid)`
Activates a user.

**Parameters:**
- `uuid` (str): User’s unique identifier.

**Usage:**

```python
unipy.users.activate_user("user-123")
```

#### 4. `unipy.users.set_user_group(uuid, group_uuid)`
Updates the user group assignment.

**Parameters:**
- `uuid` (str): User’s unique identifier.
- `group_uuid` (str): Group’s unique identifier.

**Usage:**

```python
unipy.users.set_user_group("user-123", "group-789")
```

#### 5. `unipy.users.delete_user(uuid)`
Deletes a user.

**Parameters:**
- `uuid` (str): User’s unique identifier.

**Usage:**

```python
unipy.users.delete_user("user-123")
```

### Hardware Management

#### 1. `unipy.hardware.get_devices()`
Fetches a list of hardware devices.

**Usage:**

```python
devices = unipy.hardware.get_devices()
```

#### 2. `unipy.hardware.get_device(device_id)`
Fetches details of a specific device.

**Usage:**

```python
device = unipy.hardware.get_device("device-123")
```

#### 3. `unipy.hardware.set_access_method(device_id, enabled_methods)`
Sets the access methods for a device.

**Usage:**

```python
unipy.hardware.set_access_method("device-123", ["pin", "nfc"])
```

#### 4. `unipy.hardware.set_doorbell_trigger(device_id, doorbell_trigger)`
Sets the doorbell trigger type for a device.

**Usage:**

```python
unipy.hardware.set_doorbell_trigger("device-123", "tap")
```

#### 5. `unipy.hardware.set_status_light(device_id, status_light)`
Sets the status light for a device.

**Usage:**

```python
unipy.hardware.set_status_light("device-123", "on")
```

#### 6. `unipy.hardware.set_display_brightness(device_id, brightness)`
Sets the display brightness for a device.

**Usage:**

```python
unipy.hardware.set_display_brightness("device-123", 50)
```

#### 7. `unipy.hardware.set_status_sound(device_id, status_sound)`
Sets the status sound for a device.

**Usage:**

```python
unipy.hardware.set_status_sound("device-123", 30)
```

#### 8. `unipy.hardware.get_device_capabilities(device_id)`
Fetches the capabilities of a device.

**Usage:**

```python
capabilities = unipy.hardware.get_device_capabilities("device-123")
```

#### 9. `unipy.hardware.get_device_model(device_id)`
Fetches the model of a device.

**Usage:**

```python
model = unipy.hardware.get_device_model("device-123")
```

#### 10. `unipy.hardware.restart_device(device_id)`
Restarts a device.

**Usage:**

```python
unipy.hardware.restart_device("device-123")
```

## Example Code

```python
from unipyaccess import UnipyAccess
from dotenv import load_dotenv
import os

load_dotenv()

unipy = UnipyAccess(
    base_url=os.getenv('UNIFI_CONTROLLER_ADDRESS'),
    username=os.getenv('UNIFI_LOGIN'),
    password=os.getenv('UNIFI_PASSWORD'),
    verify=os.getenv('VERIFY_SSL')
)

# Retrieve users
users = unipy.users.get_users()
print(users)

# Create a user
new_user = {
    "first_name": "Alice",
    "last_name": "Smith",
    "PersonId": "125"
}
unipy.users.create_user(new_user)

# Activate a user
unipy.users.activate_user("user-123")

# Deactivate a user
unipy.users.deactivate_user("user-123")

# Delete a user
unipy.users.delete_user("user-123")

# Update user group
unipy.users.set_user_group("user-123", "group-789")

# Hardware Management
# Get devices
devices = unipy.hardware.get_devices()
print(devices)

# Set device configurations
unipy.hardware.set_access_method("device-123", ["pin", "nfc"])
unipy.hardware.set_display_brightness("device-123", 50)
unipy.hardware.set_status_sound("device-123", "on")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
