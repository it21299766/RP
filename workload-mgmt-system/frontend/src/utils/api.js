const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

/**
 * Get authentication headers with JWT token
 * @param {boolean} isFormData - If true, don't set Content-Type (let browser set it for FormData)
 */
function getAuthHeaders(isFormData = false) {
  const token = localStorage.getItem('token');
  const headers = {};
  if (!isFormData) {
    headers['Content-Type'] = 'application/json';
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function handleResponse(res) {
  if (!res.ok) {
    let errorMessage = res.statusText;
    try {
      const errorData = await res.json();
      errorMessage = errorData.detail || errorData.message || res.statusText;
    } catch (e) {
      // If response is not JSON, use status text
      const text = await res.text();
      errorMessage = text || res.statusText;
    }
    const error = new Error(errorMessage);
    error.status = res.status;
    throw error;
  }
  // No content
  if (res.status === 204) return null;
  return res.json();
}

export async function get(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: getAuthHeaders(),
  });
  return handleResponse(res);
}

export async function post(path, body, options = {}) {
  // Check if body is FormData (file upload)
  const isFormData = body instanceof FormData;
  const headers = options.headers || getAuthHeaders(isFormData);
  
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: headers,
    body: isFormData ? body : JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function put(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function del(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  return handleResponse(res);
}

export default { get, post, put, del };
