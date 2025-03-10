import React, { useState } from "react";

function Profile() {
    // Sample user data to populate the form
    const sampleUserData = {
        username: "sampleUser",
        email: "sampleuser@example.com",
        phone: "123-456-7890",
    };

    // State to hold user data, edit mode, and form field values
    const [userData, setUserData] = useState(sampleUserData);
    const [isEditing, setIsEditing] = useState(false);

    // Handle input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    // Toggle edit mode
    const toggleEdit = () => {
        setIsEditing(!isEditing);
    };

    // Handle form submission (e.g., save the updated user data)
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Updated user data:", userData);
        // Here you could send the updated data to the server or save it as necessary
        setIsEditing(false); // Disable the fields after submission
    };

    return (
        <div className="container">
            <h1>Profile Page</h1>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        className="form-control"
                        value={userData.username}
                        onChange={handleChange}
                        disabled={!isEditing}
                    />
                </div>

                <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        className="form-control"
                        value={userData.email}
                        onChange={handleChange}
                        disabled={!isEditing}
                    />
                </div>

                <div className="mb-3">
                    <label htmlFor="phone" className="form-label">Phone</label>
                    <input
                        type="text"
                        id="phone"
                        name="phone"
                        className="form-control"
                        value={userData.phone}
                        onChange={handleChange}
                        disabled={!isEditing}
                    />
                </div>

                <button type="button" className="btn btn-secondary" onClick={toggleEdit}>
                    {isEditing ? "Cancel" : "Edit"}
                </button>

                {isEditing && (
                    <button type="submit" className="btn btn-primary ms-2">
                        Save Changes
                    </button>
                )}
            </form>
        </div>
    );
}

export default Profile;
