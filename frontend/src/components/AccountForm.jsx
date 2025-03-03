import React, { useState, useEffect } from "react";
import { getAccount, createAccount, updateAccount, deleteAccount } from "../assets/api";

function Account() {
    const [account, setAccount] = useState(null);
    const [token, setToken] = useState(localStorage.getItem("token") || "");  // Store JWT if needed
    const [formData, setFormData] = useState({ name: "", username: "", password: "" });
    const [message, setMessage] = useState("");

    // Fetch user account on page load
    useEffect(() => {
        if (token) {
            getAccount(token).then((data) => {
                if (data) setAccount(data.data);
            });
        }
    }, [token]);

    // Handle form input changes
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // Create a new account
    const handleCreate = async (e) => {
        e.preventDefault();
        const response = await createAccount(formData);
        if (response) {
            setMessage("Account created successfully!");
        } else {
            setMessage("Registration failed. Try again.");
        }
    };

    // Update the account
    const handleUpdate = async () => {
        const response = await updateAccount(formData, token);
        if (response) {
            setMessage("Account updated successfully!");
            setAccount(response.data);
        } else {
            setMessage("Update failed. Try again.");
        }
    };

    // Delete the account
    const handleDelete = async () => {
        const response = await deleteAccount(token);
        if (response) {
            setMessage("Account deleted successfully!");
            setAccount(null);
        } else {
            setMessage("Failed to delete account.");
        }
    };

    return (
        <div>
            <h1>Account Management</h1>

            {/* Show account details */}
            {account ? (
                <div>
                    <h2>Account Details</h2>
                    <p><strong>Name:</strong> {account.name}</p>
                    <p><strong>Username:</strong> {account.username}</p>
                    <button onClick={handleDelete}>Delete Account</button>
                </div>
            ) : (
                <p>No account found.</p>
            )}

            {/* Registration Form */}
            <div>
                <h2>Create Account</h2>
                <form onSubmit={handleCreate}>
                    <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
                    <input type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required />
                    <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
                    <button type="submit">Register</button>
                </form>
            </div>

            {/* Update Form */}
            {account && (
                <div>
                    <h2>Update Account</h2>
                    <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} />
                    <input type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} />
                    <input type="password" name="password" placeholder="New Password" value={formData.password} onChange={handleChange} />
                    <button onClick={handleUpdate}>Update</button>
                </div>
            )}

            {message && <p>{message}</p>}
        </div>
    );
}

export default Account;
