// Simulate auth flow. Settle later
class AuthHandler{
    constructor(){
        this.mockUser = {username: "test", password: "test", userRole: "student"}
    }
    login(username, password){
        if(username == this.mockUser.username && password == this.mockUser.password){
            const newToken = this.createToken(this.mockUser.username, this.mockUser.userRole);
            localStorage.setItem("token", JSON.stringify(newToken));
            return true;
        }
        return false;
    }
    logout(){
        localStorage.removeItem("token");
    }
    createToken(username, userRole){
        const newToken = {username: username, userRole: userRole};
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
