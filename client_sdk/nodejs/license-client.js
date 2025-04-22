const axios = require('axios');
const os = require('os');
const crypto = require('crypto');

class LicenseClient {
  constructor(apiUrl, apiKey) {
    this.apiUrl = apiUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
  }

  getHardwareId() {
    // Generate a unique hardware ID based on system information
    const systemInfo = {
      platform: process.platform,
      arch: process.arch,
      cpus: os.cpus().length,
      hostname: os.hostname(),
      totalmem: os.totalmem(),
      networkInterfaces: Object.keys(os.networkInterfaces())
    };

    // Create a hash of the system information
    const hardwareHash = crypto
      .createHash('sha256')
      .update(JSON.stringify(systemInfo))
      .digest('hex');

    return hardwareHash;
  }

  async validateLicense(licenseKey) {
    const hardwareId = this.getHardwareId();

    try {
      const response = await axios.post(
        `${this.apiUrl}/api/v1/licenses/validate`,
        {
          license_key: licenseKey,
          hardware_id: hardwareId
        },
        { headers: this.headers }
      );

      return {
        valid: true,
        data: response.data
      };
    } catch (error) {
      return {
        valid: false,
        error: error.response?.data?.detail || error.message
      };
    }
  }

  async activateLicense(licenseKey) {
    const hardwareId = this.getHardwareId();

    try {
      const response = await axios.post(
        `${this.apiUrl}/api/v1/licenses/activate`,
        {
          license_key: licenseKey,
          hardware_id: hardwareId
        },
        { headers: this.headers }
      );

      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message
      };
    }
  }

  async checkLicenseStatus(licenseKey) {
    try {
      const response = await axios.get(
        `${this.apiUrl}/api/v1/licenses/status/${licenseKey}`,
        { headers: this.headers }
      );

      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message
      };
    }
  }
}

module.exports = LicenseClient; 