import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${BASE_URL}//api`,
  withCredentials: true, // send session cookie on every request
  headers: {
    'Content-Type': 'application/json',
  },
})

// Fetch and attach CSRF token before any mutating request
let csrfToken = null

async function ensureCsrf() {
  if (!csrfToken) {
    const response = await axios.get(`${BASE_URL}/api/auth/csrf/`, {
      withCredentials: true,
    })
    csrfToken = response.data.csrfToken
  }
}

api.interceptors.request.use(async (config) => {
  const mutating = ['post', 'put', 'patch', 'delete']
  if (mutating.includes(config.method)) {
    await ensureCsrf()
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 403) {
      // CSRF token may be stale — reset so it's fetched fresh on next request
      csrfToken = null
    }
    return Promise.reject(error)
  }
)

export default api
