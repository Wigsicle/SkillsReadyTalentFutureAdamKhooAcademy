import React, { useState, useEffect } from "react";
import { useAuth } from '../static/AuthContext';
import { getUser, updateUser } from "../static/api";

function Profile() {
    const authHandler = useAuth(); 

    // State to hold user data, edit mode, and form field values
    const [userData, setUserData] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [loading, setLoading] = useState(true); // Loading state for API call

    // Fetch user data on component mount
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const token = authHandler.getToken(); // Get token from localStorage
                const response = await getUser(token.token); // Fetch data from API
                if (response.data) {
                    setUserData(response.data); // Set the user data from API
                } else {
                    if(response.error === "Unauthorized"){
                        authHandler.handleTokenExpired();
                    }
                }
            } catch (error) {
                console.error("Failed to fetch user data:", error);
            } finally {
                setLoading(false); // Set loading to false after the data is fetched
            }
        };

        fetchUserData(); // Call the function to fetch data
    }, []); // Empty dependency array to call it only on mount

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
    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Updated user data:", userData);

        // Map the firstname to first_name for submission
        const updatedUserData = {
            ...userData,
            country_id: userData.countryId, // Mapping
            user_type_id: userData.userTypeId, // Mapping
            last_name: userData.lastname, // Mapping 'lastname' to 'last_name'
            first_name: userData.firstname, // Mapping 'firstname' to 'first_name'
         
        };

        // Submit the updated data to the API
        try {
            const token = authHandler.getToken(); 
            const response = await updateUser(updatedUserData, token.token);

            if (response.data) {
                console.log("Profile updated successfully");
                setIsEditing(false); // Disable the fields after successful submission
            } else {
                if(response.error === "Unauthorized"){
                    authHandler.handleTokenExpired();
                }
                console.error("Failed to update profile", response.error);
            }
        } catch (error) {
            console.error("Error updating profile:", error);
        }
    };

    // If data is still loading, show a loading spinner
    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container">
            <h1>Profile Page</h1>
            <form onSubmit={handleSubmit}>
                {/* Fields for profile data */}
                <div className="mb-3">
                    <label htmlFor="firstname" className="form-label">First Name</label>
                    <input
                        type="text"
                        id="firstname"
                        name="firstname"
                        className="form-control"
                        value={userData?.firstname || ""}
                        onChange={handleChange}
                        disabled={!isEditing}
                    />
                </div>

                <div className="mb-3">
                    <label htmlFor="lastname" className="form-label">Last Name</label>
                    <input
                        type="text"
                        id="lastname"
                        name="lastname"
                        className="form-control"
                        value={userData?.lastname || ""}
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
                        value={userData?.email || ""}
                        onChange={handleChange}
                        disabled={!isEditing}
                    />
                </div>

                <div className="mb-3">
                    <label htmlFor="countryId" className="form-label">Country</label>
                    <select
                        id="countryId"
                        name="countryId"
                        className="form-control"
                        value={userData?.countryId || ""}
                        onChange={handleChange}
                        disabled={!isEditing}
                    >
                        <option value="1">Country 1</option>
                        <option value="2">Country 2</option>
                        {/* Add more countries as needed */}
                    </select>
                </div>

                <div className="mb-3">
                    <label htmlFor="address" className="form-label">Address</label>
                    <input
                        type="text"
                        id="address"
                        name="address"
                        className="form-control"
                        value={userData?.address || ""}
                        onChange={handleChange}
                        disabled={!isEditing}
                    />
                </div>

                <div className="mb-3">
                    <label htmlFor="userTypeId" className="form-label">User Type</label>
                    <select
                        id="userTypeId"
                        name="userTypeId"
                        className="form-control"
                        value={userData?.userTypeId || ""}
                        onChange={handleChange}
                        disabled={!isEditing}
                    >
                        <option value="1">Admin</option>
                        <option value="2">User</option>
                        {/* Add more user types as needed */}
                    </select>
                </div>

                {/* Password input, visible but not editable unless necessary */}
                {isEditing && (
                    <div className="mb-3">
                        <label htmlFor="password" className="form-label">Password</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            className="form-control"
                            value={userData?.password || ""}
                            onChange={handleChange}
                        />
                    </div>
                )}

                <button type="button" className="btn btn-secondary" onClick={toggleEdit}>
                    {isEditing ? "Cancel" : "Edit"}
                </button>

                {isEditing && (
                    <button type="submit" className="btn btn-dark ms-2">
                        Save Changes
                    </button>
                )}
            </form>
        </div>
    );
}

export default Profile;
