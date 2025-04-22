import requests
import uuid
import platform
import hashlib
import json
from typing import Dict, Optional, Any

class LicenseClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_hardware_id(self) -> str:
        """Generate a unique hardware ID based on system information"""
        system_info = {
            "platform": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "node": platform.node()
        }
        # Create a hash of the system information
        hardware_hash = hashlib.sha256(json.dumps(system_info, sort_keys=True).encode()).hexdigest()
        return hardware_hash
    
    def validate_license(self, license_key: str) -> Dict[str, Any]:
        """Validate a license key"""
        hardware_id = self.get_hardware_id()
        
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/licenses/validate",
                headers=self.headers,
                json={
                    "license_key": license_key,
                    "hardware_id": hardware_id
                }
            )
            
            if response.status_code == 200:
                return {
                    "valid": True,
                    "data": response.json()
                }
            else:
                return {
                    "valid": False,
                    "error": response.json().get("detail", "Unknown error")
                }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    def activate_license(self, license_key: str) -> Dict[str, Any]:
        """Activate a license on the current hardware"""
        hardware_id = self.get_hardware_id()
        
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/licenses/activate",
                headers=self.headers,
                json={
                    "license_key": license_key,
                    "hardware_id": hardware_id
                }
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": response.json().get("detail", "Unknown error")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_license_status(self, license_key: str) -> Dict[str, Any]:
        """Check the status of a license"""
        try:
            response = requests.get(
                f"{self.api_url}/api/v1/licenses/status/{license_key}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": response.json().get("detail", "Unknown error")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 