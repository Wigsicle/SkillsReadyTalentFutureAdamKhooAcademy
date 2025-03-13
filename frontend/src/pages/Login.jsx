import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../static/AuthContext';

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [loggedIn, setLoggedIn] = useState(false);

    const navigate = useNavigate(); // Initialize the navigate function
    const authHandler = useAuth();  // Use the useAuth hook to get authHandler

    const handleLogin = (e) => {
        e.preventDefault();
        const isValid = authHandler.login(username, password) // Call the login method from AuthHandler
        if (isValid) {
            setLoggedIn(true);
        } else {
            setErrorMessage("Invalid username or password");
        }
    };

    useEffect(() => {
        if (loggedIn) {
            navigate("/profile", { replace: true });
            window.location.reload();
        }
    }, [loggedIn, navigate]);

    return (
        <div className="container-fluid w-100 vh-100 position-relative">
            <div className="center">
                <h1>Login Page</h1>
                {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
                <form onSubmit={handleLogin}>
                    <div class="mb-3">
                        <label for="usernameField" class="form-label">Username</label>
                        <input
                            type="text"
                            className="form-control"
                            id="usernameField"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />                    
                    </div>
                    <div class="mb-3">
                        <label for="passwordField" class="form-label">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            id="passwordField"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>

            </div>
        </div>
    );

}

export default Login;