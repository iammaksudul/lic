// API endpoints
const API_BASE_URL = '/api/v1';

// Utility functions
const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
};

// API calls
const api = {
    async get(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    },

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    },

    async put(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    },

    async delete(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    }
};

// License management
const licenseManager = {
    async activateLicense(licenseKey, hardwareId) {
        try {
            const response = await api.post('/licenses/activate', {
                license_key: licenseKey,
                hardware_id: hardwareId
            });
            showAlert('success', 'License activated successfully!');
            return response;
        } catch (error) {
            showAlert('danger', 'Failed to activate license: ' + error.message);
            throw error;
        }
    },

    async checkLicense(licenseKey, hardwareId) {
        try {
            const response = await api.post('/licenses/check', {
                license_key: licenseKey,
                hardware_id: hardwareId
            });
            return response;
        } catch (error) {
            showAlert('danger', 'Failed to check license: ' + error.message);
            throw error;
        }
    },

    async deactivateLicense(licenseKey, hardwareId) {
        try {
            const response = await api.post('/licenses/deactivate', {
                license_key: licenseKey,
                hardware_id: hardwareId
            });
            showAlert('success', 'License deactivated successfully!');
            return response;
        } catch (error) {
            showAlert('danger', 'Failed to deactivate license: ' + error.message);
            throw error;
        }
    }
};

// UI helpers
const showAlert = (type, message) => {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
    setTimeout(() => alertDiv.remove(), 5000);
};

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // License activation form
    const activateForm = document.getElementById('activateLicenseForm');
    if (activateForm) {
        activateForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const licenseKey = document.getElementById('license_key').value;
            const hardwareId = document.getElementById('hardware_id').value;
            try {
                await licenseManager.activateLicense(licenseKey, hardwareId);
                activateForm.reset();
            } catch (error) {
                console.error('Activation error:', error);
            }
        });
    }

    // License check form
    const checkForm = document.getElementById('checkLicenseForm');
    if (checkForm) {
        checkForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const licenseKey = document.getElementById('check_license_key').value;
            const hardwareId = document.getElementById('check_hardware_id').value;
            try {
                const result = await licenseManager.checkLicense(licenseKey, hardwareId);
                const statusDiv = document.getElementById('licenseStatus');
                statusDiv.classList.remove('d-none', 'alert-success', 'alert-danger');
                statusDiv.classList.add('alert-info');
                statusDiv.innerHTML = `
                    <strong>License Status:</strong><br>
                    Status: ${result.status}<br>
                    Expires: ${formatDate(result.expires_at)}<br>
                    Activations: ${result.current_activations}/${result.max_activations}
                `;
            } catch (error) {
                console.error('Check error:', error);
            }
        });
    }

    // License deactivation form
    const deactivateForm = document.getElementById('deactivateLicenseForm');
    if (deactivateForm) {
        deactivateForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const licenseKey = document.getElementById('deactivate_license_key').value;
            const hardwareId = document.getElementById('deactivate_hardware_id').value;
            try {
                await licenseManager.deactivateLicense(licenseKey, hardwareId);
                deactivateForm.reset();
            } catch (error) {
                console.error('Deactivation error:', error);
            }
        });
    }
}); 