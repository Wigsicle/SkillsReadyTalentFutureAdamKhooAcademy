import React, { useEffect, useState } from "react";
import "../styles.css"; // Import global styles

function Assessments() {
    const [assessments, setAssessments] = useState([]); // State to hold assessment data
    const [loading, setLoading] = useState(true); // State to manage loading state
    const [error, setError] = useState(null); // State to manage error messages

    // Function to fetch assessments from the FastAPI backend
    const fetchAssessments = async () => {
        try {
            const response = await fetch("http://localhost:80/assessment"); // Adjust the URL as needed
            const data = await response.json();
            if (response.ok) {
                setAssessments(data.data.assessments); // Set the assessments data
            } else {
                throw new Error(data.detail || "Failed to fetch assessments");
            }
        } catch (err) {
            setError(err.message); // Set error message if fetch fails
        } finally {
            setLoading(false); // Set loading to false after fetch
        }
    };

    // Use useEffect to fetch assessments when the component mounts
    useEffect(() => {
        fetchAssessments();
    }, []);

    // Render loading state or error message
    if (loading) return <div>Loading assessments...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="assessments-container">
            <h1>Assessments</h1>
            <div className="assessments-list">
                {assessments.map((assessment) => (
                    <div key={assessment.assessmentId} className="assessment-card">
                        <div className="card-inner">
                            <div className="card-front">
                                <h2>{assessment.name}</h2>
                                <p>Total Marks: {assessment.totalMarks}</p>
                                <p>Course ID: {assessment.courseId}</p>
                            </div>
                            <div className="card-back">
                                <h3>Ready to take the assessment?</h3>
                                <button className="take-assessment-btn">Take Assessment</button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Back to Home Button */}
            <button className="back-to-home-btn" onClick={() => window.history.back()}>
                Back to Home
            </button>
        </div>
    );
}

export default Assessments;