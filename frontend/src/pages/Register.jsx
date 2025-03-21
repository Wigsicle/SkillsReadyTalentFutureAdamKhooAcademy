import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import { registerUser } from "../static/api";

function Register() {
    const [firstname, setFirstname] = useState("");
    const [lastname, setLastname] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [countryId, setCountryId] = useState(1); // Default countryId
    const [address, setAddress] = useState("");
    const [userTypeId, setUserTypeId] = useState(1); // Default userTypeId
    const [errorMessage, setErrorMessage] = useState("");
    const [registered, setRegistered] = useState(false);

    const navigate = useNavigate(); // Initialize the navigate function

    const handleRegister = async(e) => {
        e.preventDefault();

        // Simulate a successful registration process
        if (firstname && lastname && email && password && address && countryId && userTypeId) {
            const queryString = new URLSearchParams({
                firstname,
                lastname,
                email,
                password,  
                country_id: countryId, 
                address,
                user_type_id: userTypeId  
            }).toString();
            const newResponse = await registerUser(queryString); // Call the registerUser function from the API
            if (newResponse.error) {
                setErrorMessage(newResponse.error);
                return;
            }
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
        <div className="container-fluid vh-100 position-relative">
            <div className="container p-5 w-25">
                <h1>Register Page</h1>
                {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
                <form onSubmit={handleRegister}>
                    <div className="mb-3">
                        <label htmlFor="firstnameField" className="form-label"><strong>First Name</strong></label>
                        <input
                            type="text"
                            className="form-control"
                            id="firstnameField"
                            value={firstname}
                            onChange={(e) => setFirstname(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="lastnameField" className="form-label"><strong>Last Name</strong></label>
                        <input
                            type="text"
                            className="form-control"
                            id="lastnameField"
                            value={lastname}
                            onChange={(e) => setLastname(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="emailField" className="form-label"><strong>Email (username)</strong></label>
                        <input
                            type="email"
                            className="form-control"
                            id="emailField"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="passwordField" className="form-label"><strong>Password</strong></label>
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
                        <label htmlFor="countryField" className="form-label"><strong>Country</strong></label>
                        <select
                            id="countryField"
                            className="form-control"
                            value={countryId}
                            onChange={(e) => setCountryId(Number(e.target.value))}
                        >
                            <option value="1">Country 1</option>
                            <option value="2">Country 2</option>
                            {/* Add more countries as needed */}
                        </select>
                    </div>
                    <div className="mb-3">
                        <label htmlFor="addressField" className="form-label"><strong>Address</strong></label>
                        <input
                            type="text"
                            className="form-control"
                            id="addressField"
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="userTypeField" className="form-label"><strong>User Type</strong></label>
                        <select
                            id="userTypeField"
                            className="form-control"
                            value={userTypeId}
                            onChange={(e) => setUserTypeId(Number(e.target.value))}
                        >
                            <option value="1">Job Seeker</option>
                            <option value="2">Company</option>
                            {/* Add more user types as needed */}
                        </select>
                    </div>
                    <button type="submit" className="btn btn-dark">Register</button>
                </form>

                <div className="mt-3">
                    <p>Have an account? <Link to="/login">Login here</Link></p>
                </div>

            </div>
        </div>
    );
}

export default Register;
