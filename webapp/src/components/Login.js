import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:80'; // Adjust based on your API Gateway

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`${API_BASE_URL}/token`, { username, password });
            console.log('Login successful:', response.data);
            setSuccessMessage('Account successfully logged in!'); // Success message for login
            // Redirect to account page or dashboard
        } catch (err) {
            setError('Login failed. Please check your credentials.');
            console.error(err);
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Login</button>
            </form>
            {error && <p>{error}</p>}
            {successMessage && <p>{successMessage}</p>}
            <p>
                No account? <span style={{ textDecoration: 'underline', cursor: 'pointer' }} onClick={() => navigate('/create-account')}>Click here to create account</span>
            </p>
        </div>
    );
};

export default Login; 