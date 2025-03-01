import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:80'; // Adjust based on your API Gateway

const CreateAccount = () => {
    const [name, setName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();

    const handleCreateAccount = async (e) => {
        e.preventDefault();
        try {
            const formData = new FormData();
            formData.append('name', name);
            formData.append('username', username);
            formData.append('password', password);

            const response = await axios.post(`${API_BASE_URL}/accounts/create`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log('Account created:', response.data);
            setSuccessMessage('Account successfully created!'); // Success message for account creation
            setTimeout(() => {
                navigate('/'); // Redirect to login after 2 seconds
            }, 2000);
        } catch (err) {
            setError('Account creation failed. Please try again.');
            console.error(err);
        }
    };

    return (
        <div>
            <h1>Create Account</h1>
            <form onSubmit={handleCreateAccount}>
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
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
                <button type="submit">Create Account</button>
            </form>
            {error && <p>{error}</p>}
            {successMessage && <p>{successMessage}</p>}
        </div>
    );
};

export default CreateAccount; 