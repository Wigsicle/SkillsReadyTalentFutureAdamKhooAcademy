import axios from "axios";

const API_BASE_URL = "http://localhost:8000/accounts";  // FastAPI API Gateway

// Fetch the logged-in user's account
export const getAccount = async () => {
    return { name: "John Doe", username: "johndoe", accountStatus: true };  // Mock user data
};

export const createAccount = async (userData) => {
    console.log("Mock Register:", userData);
    return { message: "Account created successfully!" };
};

export const updateAccount = async (userData) => {
    console.log("Mock Update:", userData);
    return { message: "Account updated successfully!" };
};

export const deleteAccount = async () => {
    console.log("Mock Delete");
    return { message: "Account deleted successfully!" };
};
