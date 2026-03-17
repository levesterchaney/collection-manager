import api from './axios'

export const itemsApi = {
  list: (collectionId, params = {}) =>
    api.get(`/collections/${collectionId}/items/`, { params }),
  get: (collectionId, itemId) =>
    api.get(`/collections/${collectionId}/items/${itemId}/`),
  create: (collectionId, data) =>
    api.post(`/collections/${collectionId}/items/`, data, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  update: (collectionId, itemId, data) =>
    api.patch(`/collections/${collectionId}/items/${itemId}/`, data, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  delete: (collectionId, itemId) =>
    api.delete(`/collections/${collectionId}/items/${itemId}/`),
}
