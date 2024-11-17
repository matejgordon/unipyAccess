import logging

class UserManager:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_users(self):
        endpoint = "/proxy/access/api/v2/users"
        return self.api_client.get(endpoint)["data"]

    def create_user(self, user):
        endpoint = "/proxy/access/api/v2/user"
        payload = {
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "employee_number": str(user.get("PersonId", "")),
            "group_ids": user.get("group_ids", [])
        }
        response = self.api_client.post(endpoint, payload)
        logging.info(f'Created user {user["first_name"]} {user["last_name"]}: {response}')
        return response

    def deactivate_user(self, user_id):
        endpoint = f'/proxy/access/ulp-go/api/v2/user/{user_id}/deactivate?isULP=1'
        response = self.api_client.put(endpoint)
        logging.info(f'Deactivated user {user_id}: {response}')
        return response

    def activate_user(self, user_id):
        endpoint = f'/proxy/access/ulp-go/api/v2/user/{user_id}/active?isULP=1'
        response = self.api_client.put(endpoint)
        logging.info(f'Activated user {user_id}: {response}')
        return response

    def delete_user(self, user_id):
        endpoint = f'/proxy/access/ulp-go/api/v2/user/{user_id}?isULP=1'
        response = self.api_client.delete(endpoint)
        logging.info(f'Deleted user {user_id}: {response}')
        return response

    def set_user_group(self, user_id, group_id):
        endpoint = f"/proxy/access/api/v2/user/{user_id}"
        payload = {"group_ids": [group_id]}
        response = self.api_client.put(endpoint, payload)
        logging.info(f"Updated user group for {user_id}")
        return response
