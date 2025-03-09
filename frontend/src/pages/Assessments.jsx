import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom
import "../styles.css"; // Import global styles
import axios from 'axios'; // Import axios for making HTTP requests

function Assessments() {
    const [assessments, setAssessments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAssessments = async () => {
            try {
                const response = await axios.get('/assessment'); // Call the FastAPI endpoint to get assessments
                console.log(response.data); // Log the entire response
                // Check if response.data.data is an array
                if (Array.isArray(response.data.data)) {
                    setAssessments(response.data.data); // Adjust based on the response structure
                } else {
                    setError("Unexpected response structure");
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAssessments();
    }, []);

    if (loading) return <div>Loading assessments...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="assessments-container">
            <h1>Assess Your Skills & Earn Certifications</h1>
            <p>Prepare for industry-leading certifications with our expert-designed assessment tests.</p>

            {/* Assessment List */}
            <div className="assessment-list">
                {assessments.length > 0 ? (
                    assessments.map((assessment) => (
                        <Link to={`/assessments/${assessment.id}`} className="assessment-card" key={assessment.id}>
                            <img src="https://via.placeholder.com/300x200" alt={assessment.name} className="assessment-image" />
                            <div className="assessment-details">
                                <h3 className="assessment-title">{assessment.name}</h3>
                                <p className="assessment-course">Suitable for course: {assessment.course_id}</p>
                            </div>
                        </Link>
                    ))
                ) : (
                    <div>No assessments available.</div>
                )}
            </div>

            {/* Back to Home Button */}
            <button className="back-to-home-btn" onClick={() => window.history.back()}>
                Back to Home
            </button>
        </div>
    );
}

export default Assessments;
