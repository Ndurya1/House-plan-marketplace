import { apiClient } from './index';

export const getCategories = () => apiClient('/catalogue/categories/');

export const getPlansByCategory = (category) =>
  apiClient(`/catalogue/?category=${encodeURIComponent(category)}`);

export const getPlans = () => apiClient('/catalogue/');

export const getPlanDetails = (id) => apiClient(`/catalogue/${id}/`);

export const createPlan = (planData, token) =>
  apiClient('/catalogue/', {
    method: 'POST',
    body: JSON.stringify(planData),
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const updatePlan = (id, planData, token) =>
  apiClient(`/catalogue/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(planData),
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const patchPlan = (id, planData, token) =>
  apiClient(`/catalogue/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(planData),
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const deletePlan = (id, token) =>
  apiClient(`/catalogue/${id}/`, {
    method: 'DELETE',
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
