import axios from "axios";

const API_BASE_URL = "http://localhost";  // Base API URL

// Utility function to make a generic API request
export const makeRequest = async (endpoint, method, data = null) => {
    try {
        const config = {
            method: method,  // GET, POST, PUT, DELETE, etc.
            url: `${API_BASE_URL}${endpoint}`,
            data: data,  // If there’s data (for POST/PUT requests)
        };

        const response = await axios(config);
        return response.data;  // Return the response data
    } catch (error) {
        console.error("API Request Error:", error);
        return { error: "An error occurred while processing the request." };
    }
};

export const getJob = async () => {
    return await makeRequest("/job", "GET");
};

// Create a new job (POST request)
export const createJob = async (userData) => {
    return await makeRequest("/job/create", "POST", userData);
};

// Update an existing job (PUT request)
export const updateJob = async (userData) => {
    return await makeRequest("/job/update", "PUT", userData);
};

// Delete an job (DELETE request)
export const deleteJob = async () => {
    return await makeRequest("/job", "DELETE");
};