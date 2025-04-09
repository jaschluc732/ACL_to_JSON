import pyeapi
import json

def get_acl(node, acl_name):
    """Retrieves an ACL from an Arista device and returns it as a dictionary."""
    try:
        response = node.enable([f"show ip access-lists {acl_name}"])
        acl_data = response[0]['result']
        return acl_data
    except pyeapi.eapilib.CommandError as e:
        print(f"Error retrieving ACL '{acl_name}': {e}")
        return None

def acl_to_json(acl_data, output_file):
    """Converts ACL data to JSON format and writes it to a file."""
    if acl_data:
        with open(output_file, 'w') as f:
            json.dump(acl_data, f, indent=4)
        print(f"ACL data written to '{output_file}'")
    else:
        print("No ACL data to write.")

def main():
    """Main function to prompt user input, connect to the device, retrieve ACL, and convert it to JSON."""
    print("--- Arista ACL Retrieval Tool ---")

    host = input("Enter Arista device IP or hostname: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    acl_name = input("Enter ACL name to retrieve: ").strip()

    output_file = f"{acl_name}.json"

    connection_settings = {
        'transport': 'https',
        'host': host,
        'username': username,
        'password': password,
        'return_output': True
    }

    try:
        node = pyeapi.connect(**connection_settings)
        acl_data = get_acl(node, acl_name)
        acl_to_json(acl_data, output_file)
    except pyeapi.client.ConnectionError as e:
        print(f"Error connecting to Arista device: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
