import React, { useEffect, useState } from "react";
import BreadCrumb from "../components/Breadcrumb";
import { getCertificates, getUser } from "../static/api";  // Assuming getCertificates is the API function
import { useAuth } from '../static/AuthContext';

function Certificates() {
    const authHandler = useAuth();
    
    const [certificates, setCertificates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCertificates = async () => {
            try {
                const token = authHandler.getToken(); // Get token from localStorage
                const currentUser = await getUser(token.token);
                if (currentUser.data) {
                    const response = await getCertificates(currentUser.data.userId, token.token); // Fetch certificates from the API
                    if(response.data && currentUser.data){
                        setCertificates(response.data); // Assuming the API returns a 'certificates' field
                        setLoading(false); // Set loading to false once the fetch is complete
                    }
                    else{
                        throw new Error(response.error || "Failed to fetch certificates");
                    }
                } else {
                    if (currentUser.error === "Unauthorized") {
                        authHandler.handleTokenExpired(); // Handle token expiration
                    }
                }
            } catch (err) {
                setError(err.message); // Set error message if fetch fails
                setLoading(false); // Set loading to false on error
            }
        };

        fetchCertificates();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="container-fluid">
            <BreadCrumb title={"Your Certificates"} homeRoute={"/"} />
            <h1>Your Certificates</h1>
            <p>All your achievements in one place.</p>

            <div className="accordion" id="accordionExample">
                {certificates.map((certificate) => (
                    <div className="accordion-item" key={certificate.certificateId}>
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target={`#collapse${certificate.certificateId}`}
                                aria-expanded="true"
                                aria-controls={`collapse${certificate.certificateId}`}
                            >
                                {certificate.name}
                            </button>
                        </h2>
                        <div
                            id={`collapse${certificate.certificateId}`}
                            className="accordion-collapse collapse"
                            data-bs-parent="#accordionExample"
                        >
                            <div className="accordion-body">
                                <strong>{certificate.description || "No description available."}</strong>
                                <div>
                                    <strong>Course ID:</strong> {certificate.courseId || "N/A"}
                                </div>
                                <div>
                                    <strong>Years Valid:</strong> {certificate.yearsValid || "N/A"}
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Certificates;
