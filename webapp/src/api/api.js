// src/api/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:80'; // Adjust based on your API Gateway

export const getAccounts = async () => {
    const response = await axios.get(`${API_BASE_URL}/account`);
    return response.data;
};

export const createAccount = async (accountData) => {
    const response = await axios.post(`${API_BASE_URL}/account/create`, accountData);
    return response.data;
};

// Add more functions for other services as needed