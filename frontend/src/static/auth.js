// Simulate auth flow. Settle later

import { makeRequest } from "./api";

class AuthHandler{
    constructor(){
    }
    async login(username, password) {
        var newFormData = new FormData();
        newFormData.append("username", username);
        newFormData.append("password", password);

        try {
            const newResponse = await makeRequest(`/token`, "POST", newFormData, null);
            console.log(newResponse);
            if (newResponse.error) {
                return false;
            }
            if (newResponse.access_token) {
                const newToken = this.createToken(username, newResponse.access_token);
                localStorage.setItem("token", JSON.stringify(newToken));
                return true;
            }
            return false;
        } catch (error) {
            console.error("Error during login:", error);
            return false;
        }
    }
    logout(){
        localStorage.removeItem("token");
        window.location.reload();
    }
    handleTokenExpired(){
        alert("Session Expired. Please login again.");
        this.logout();
    }
    createToken(username, token){
        const newToken = {username: username, token: token};
        return newToken;
    }
    checkAuth(){
        return this.getToken() != null;
    }
    getToken(){
        try {
            const token = localStorage.getItem("token");
            return JSON.parse(token);
        } catch (error) {
            return null;
        }

    }
}

export default AuthHandler;
