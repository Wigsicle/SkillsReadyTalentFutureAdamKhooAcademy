import axios from "axios";
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = "http://localhost";  // Base API URL

// Utility function to make a generic API request
export const makeRequest = async (endpoint, method, data = null, token = null) => {
    try {
        const config = {
            method: method,  // GET, POST, PUT, DELETE, etc.
            url: `${API_BASE_URL}${endpoint}`,
            data: data,  // If there’s data (for POST/PUT requests)
        };

        // If a token is provided, add it to the Authorization header
        if (token) {
            config.headers = {
                Authorization: `Bearer ${token}`,
            };
        }

        const response = await axios(config);
        return response.data;  // Return the response data
    } catch (error) {
        if(error.response.status === 401){
            return { error: "Unauthorized" };
        }
        console.error("API Request Error:", error);
        return { error: "An error occurred while processing the request." };
    }
};

// Jobs APIs
export const getJob = async (token) => {
    return await makeRequest("/job", "GET", null, token);
};
export const createJob = async (userData, token) => {
    return await makeRequest("/job/create", "POST", userData, null);
};

export const updateJob = async (userData, token) => {
    return await makeRequest("/job/update", "PUT", userData, null);
};
export const deleteJob = async (token) => {
    return await makeRequest("/job", "DELETE", null, null);
};
export const applyJob = async (userData, token) => {
    return await makeRequest("/job/apply", "POST", userData, token);
};
export const getApplications = async (userId, token) => {
    return await makeRequest(`/job/applications/${userId}`, "GET", userId, token);
};


// User APIs
export const registerUser = async (userData, token) => {
    console.log(userData);
    return await makeRequest(`/accounts/create?${userData}`, "POST", null, null);
};

export const getUser = async (token) => {
    return await makeRequest(`/accounts/`, "GET", null, token);
};
export const updateUser = async (userData, token) => {
    console.log(userData);
    return await makeRequest(`/accounts/`, "PUT", userData, token);
};

// Course APISSSS, no need CRUD for now
export const getCourses = async (token) => {
    return await makeRequest("/api/courses", "GET", null, token); 
};

export const getCourseById = async (courseId, token) => {
    return await makeRequest(`/api/courses/${courseId}`, "GET", null, token); //filter by course id
};

export const updateCourse = async (courseId, courseData, token) => {
    return await makeRequest(`/api/courses/${courseId}`, "PUT", courseData, token);
};

// Course-Progress APISSSSS
export const joinCourse = async (courseProgressData, token) => {
    return await makeRequest("/api/course-progress", "POST", courseProgressData, token); //once joined, the course will be added to the user's course list
};

export const updateCourseProgress = async (progressId, courseProgressData, token) => {
    return await makeRequest(`/api/course-progress/${progressId}`, "PUT", courseProgressData, token);
};

