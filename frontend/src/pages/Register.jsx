import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';

function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [userRole, setUserRole] = useState("student"); // Default role is 'student'
    const [errorMessage, setErrorMessage] = useState("");
    const [registered, setRegistered] = useState(false);

    const navigate = useNavigate(); // Initialize the navigate function

    const handleRegister = (e) => {
        e.preventDefault();

        // Simulate a successful registration process
        if (username && password) {
            setRegistered(true); // Set the state to indicate that registration is successful
        } else {
            setErrorMessage("Please fill in all fields.");
        }
    };

    // If registration is successful, navigate to another page
    if (registered) {
        navigate("/welcome", { replace: true });
        return null; // Prevents rendering the form after redirection
    }

    return (
        <div className="container-fluid w-100 vh-100 position-relative">
            <div className="center">
                <h1>Register Page</h1>
                {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
                <form onSubmit={handleRegister}>
                    <div className="mb-3">
                        <label htmlFor="usernameField" className="form-label">Username</label>
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
                        <label htmlFor="passwordField" className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            id="passwordField"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="roleField" className="form-label">User Role</label>
                        <select
                            id="roleField"
                            className="form-control"
                            value={userRole}
                            onChange={(e) => setUserRole(e.target.value)}
                        >
                            <option value="student">Student</option>
                            <option value="teacher">Teacher</option>
                        </select>
                    </div>
                    <button type="submit" className="btn btn-primary">Register</button>
                </form>
            </div>
        </div>
    );
}

export default Register;
