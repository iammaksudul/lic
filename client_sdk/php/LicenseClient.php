<?php

class LicenseClient {
    private $apiUrl;
    private $apiKey;
    private $headers;

    public function __construct(string $apiUrl, string $apiKey) {
        $this->apiUrl = rtrim($apiUrl, '/');
        $this->apiKey = $apiKey;
        $this->headers = [
            "Authorization: Bearer " . $apiKey,
            "Content-Type: application/json"
        ];
    }

    public function getHardwareId(): string {
        // Generate a unique hardware ID based on system information
        $systemInfo = [
            "os" => PHP_OS,
            "php_version" => PHP_VERSION,
            "server_software" => $_SERVER['SERVER_SOFTWARE'] ?? '',
            "server_name" => $_SERVER['SERVER_NAME'] ?? '',
            "server_addr" => $_SERVER['SERVER_ADDR'] ?? '',
            "server_port" => $_SERVER['SERVER_PORT'] ?? '',
            "document_root" => $_SERVER['DOCUMENT_ROOT'] ?? '',
            "http_host" => $_SERVER['HTTP_HOST'] ?? '',
            "http_user_agent" => $_SERVER['HTTP_USER_AGENT'] ?? ''
        ];

        // Create a hash of the system information
        return hash('sha256', json_encode($systemInfo));
    }

    public function validateLicense(string $licenseKey): array {
        $hardwareId = $this->getHardwareId();
        
        $data = [
            "license_key" => $licenseKey,
            "hardware_id" => $hardwareId
        ];

        $response = $this->makeRequest('POST', '/api/v1/licenses/validate', $data);
        
        if ($response['status_code'] === 200) {
            return [
                "valid" => true,
                "data" => $response['data']
            ];
        } else {
            return [
                "valid" => false,
                "error" => $response['data']['detail'] ?? "Unknown error"
            ];
        }
    }

    public function activateLicense(string $licenseKey): array {
        $hardwareId = $this->getHardwareId();
        
        $data = [
            "license_key" => $licenseKey,
            "hardware_id" => $hardwareId
        ];

        $response = $this->makeRequest('POST', '/api/v1/licenses/activate', $data);
        
        if ($response['status_code'] === 200) {
            return [
                "success" => true,
                "data" => $response['data']
            ];
        } else {
            return [
                "success" => false,
                "error" => $response['data']['detail'] ?? "Unknown error"
            ];
        }
    }

    public function checkLicenseStatus(string $licenseKey): array {
        $response = $this->makeRequest('GET', "/api/v1/licenses/status/{$licenseKey}");
        
        if ($response['status_code'] === 200) {
            return [
                "success" => true,
                "data" => $response['data']
            ];
        } else {
            return [
                "success" => false,
                "error" => $response['data']['detail'] ?? "Unknown error"
            ];
        }
    }

    private function makeRequest(string $method, string $endpoint, array $data = null): array {
        $url = $this->apiUrl . $endpoint;
        
        $ch = curl_init();
        
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->headers);
        
        if ($method === 'POST') {
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
        
        $response = curl_exec($ch);
        $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        
        curl_close($ch);
        
        return [
            "status_code" => $statusCode,
            "data" => json_decode($response, true) ?? []
        ];
    }
} 