import api from './axios'

export const collectionsApi = {
  list: (params = {}) => api.get('/collections/', { params }),
  get: (id) => api.get(`/collections/${id}/`),
  create: (data) => api.post('/collections/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  update: (id, data) => api.patch(`/collections/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  delete: (id) => api.delete(`/collections/${id}/`),
  stats: (id) => api.get(`/collections/${id}/stats/`),
}
