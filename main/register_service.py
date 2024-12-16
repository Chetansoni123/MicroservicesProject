import os
import requests
import socket

def register_service():
    # Get the container's private IP dynamically
    service_address = socket.gethostbyname(socket.gethostname())
    
    # Set the service-specific details
    service_name = os.getenv("SERVICE_NAME")
    service_port = int(os.getenv("SERVICE_PORT"))
    
    # Consul registration payload
    registration_payload = {
        "Name": service_name,
        "Address": service_address,
        "Port": service_port,
        "Check": {
            "HTTP": f"http://{service_address}:{service_port}/health",
            "Interval": "10s",  # Health check interval
            "Timeout": "1s"     # Health check timeout
        }
    }
    
    # Send registration request to Consul
    consul_url = os.getenv("CONSUL_URL")
    response = requests.put(consul_url, json=registration_payload)
    
    if response.status_code == 200:
        print(f"Successfully registered {service_name} with Consul.")
    else:
        print(f"Failed to register service: {response.text}")

if __name__ == "__main__":
    register_service()
