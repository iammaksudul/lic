#!/bin/bash

# License Client for Bash
# Usage: ./license-client.sh <api_url> <api_key> <action> <license_key>

API_URL=$1
API_KEY=$2
ACTION=$3
LICENSE_KEY=$4

# Remove trailing slash from API URL
API_URL=${API_URL%/}

# Function to get hardware ID
get_hardware_id() {
    # Collect system information
    OS=$(uname -s)
    ARCH=$(uname -m)
    HOSTNAME=$(hostname)
    CPU_INFO=$(cat /proc/cpuinfo | grep "model name" | head -n 1 | cut -d ':' -f 2)
    MEM_INFO=$(free -m | grep Mem | awk '{print $2}')
    
    # Create a string with all the information
    HARDWARE_INFO="${OS}|${ARCH}|${HOSTNAME}|${CPU_INFO}|${MEM_INFO}"
    
    # Create a hash of the hardware information
    HARDWARE_ID=$(echo -n "$HARDWARE_INFO" | sha256sum | cut -d ' ' -f 1)
    
    echo "$HARDWARE_ID"
}

# Function to make API requests
make_request() {
    local METHOD=$1
    local ENDPOINT=$2
    local DATA=$3
    
    if [ -z "$DATA" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" -X "$METHOD" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            "${API_URL}${ENDPOINT}")
    else
        RESPONSE=$(curl -s -w "\n%{http_code}" -X "$METHOD" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d "$DATA" \
            "${API_URL}${ENDPOINT}")
    fi
    
    # Extract status code and response body
    STATUS_CODE=$(echo "$RESPONSE" | tail -n 1)
    RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')
    
    echo "$STATUS_CODE|$RESPONSE_BODY"
}

# Main function
main() {
    if [ "$ACTION" = "validate" ]; then
        HARDWARE_ID=$(get_hardware_id)
        DATA="{\"license_key\":\"$LICENSE_KEY\",\"hardware_id\":\"$HARDWARE_ID\"}"
        RESULT=$(make_request "POST" "/api/v1/licenses/validate" "$DATA")
        
        STATUS_CODE=$(echo "$RESULT" | cut -d '|' -f 1)
        RESPONSE_BODY=$(echo "$RESULT" | cut -d '|' -f 2-)
        
        if [ "$STATUS_CODE" = "200" ]; then
            echo "License is valid"
            echo "$RESPONSE_BODY"
        else
            echo "License is invalid"
            echo "$RESPONSE_BODY"
            exit 1
        fi
    elif [ "$ACTION" = "activate" ]; then
        HARDWARE_ID=$(get_hardware_id)
        DATA="{\"license_key\":\"$LICENSE_KEY\",\"hardware_id\":\"$HARDWARE_ID\"}"
        RESULT=$(make_request "POST" "/api/v1/licenses/activate" "$DATA")
        
        STATUS_CODE=$(echo "$RESULT" | cut -d '|' -f 1)
        RESPONSE_BODY=$(echo "$RESULT" | cut -d '|' -f 2-)
        
        if [ "$STATUS_CODE" = "200" ]; then
            echo "License activated successfully"
            echo "$RESPONSE_BODY"
        else
            echo "Failed to activate license"
            echo "$RESPONSE_BODY"
            exit 1
        fi
    elif [ "$ACTION" = "status" ]; then
        RESULT=$(make_request "GET" "/api/v1/licenses/status/$LICENSE_KEY")
        
        STATUS_CODE=$(echo "$RESULT" | cut -d '|' -f 1)
        RESPONSE_BODY=$(echo "$RESULT" | cut -d '|' -f 2-)
        
        if [ "$STATUS_CODE" = "200" ]; then
            echo "License status:"
            echo "$RESPONSE_BODY"
        else
            echo "Failed to get license status"
            echo "$RESPONSE_BODY"
            exit 1
        fi
    else
        echo "Invalid action. Use 'validate', 'activate', or 'status'"
        exit 1
    fi
}

# Check if all required parameters are provided
if [ -z "$API_URL" ] || [ -z "$API_KEY" ] || [ -z "$ACTION" ] || [ -z "$LICENSE_KEY" ]; then
    echo "Usage: $0 <api_url> <api_key> <action> <license_key>"
    echo "Actions: validate, activate, status"
    exit 1
fi

# Run the main function
main 