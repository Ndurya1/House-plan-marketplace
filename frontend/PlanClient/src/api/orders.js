import { apiClient } from './index';

export const getOrders = (token) =>
  apiClient('/orders/', {
    method: 'GET',
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const getOrderDetails = (id, token) =>
  apiClient(`/orders/${id}/`, {
    method: 'GET',
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const createOrder = (orderData, token) =>
  apiClient('/orders/', {
    method: 'POST',
    body: JSON.stringify(orderData),
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const updateOrder = (id, orderData, token) =>
  apiClient(`/orders/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(orderData),
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const patchOrder = (id, orderData, token) =>
  apiClient(`/orders/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(orderData),
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const deleteOrder = (id, token) =>
  apiClient(`/orders/${id}/`, {
    method: 'DELETE',
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const getOrderPaymentMethods = (id, token) =>
  apiClient(`/orders/${id}/payment-methods/`, {
    method: 'GET',
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });

export const triggerMpesaPayment = (paymentData, token) =>
  apiClient('/payments/', {
    method: 'POST',
    body: JSON.stringify(paymentData),
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
