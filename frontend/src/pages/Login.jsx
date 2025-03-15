import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../static/AuthContext';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

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
            navigate("/", { replace: true });
            window.location.reload();
        }
    }, [loggedIn, navigate]);

    return (
        <div className="container-fluid w-100 vh-100 position-relative">
            <div className="center">
                <h1>Login Page</h1>
                {errorMessage && <div className="alert alert-danger mt-3">{errorMessage}</div>}
                <form onSubmit={handleLogin}>
                    <div className="mb-3 mt-3">
                        <label htmlFor="usernameField" className="form-label bold">Username</label>
                        <input
                            type="text"
                            className="form-control"
                            id="usernameField"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="passwordField" className="form-label bold">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            id="passwordField"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-dark">Submit</button>
                </form>

                {/* Link to the Register page */}
                <div className="mt-3">
                    <p>Don't have an account? <Link to="/register">Register here</Link></p>
                </div>
            </div>
        </div>
    );
}

export default Login;
