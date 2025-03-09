import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom"; // Import useParams to get the assessment ID
import "../styles.css"; // Import global styles
import axios from 'axios';

function AssessmentDetail() {
    const { id } = useParams(); // Get the assessment ID from the URL
    const [assessment, setAssessment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAssessment = async () => {
            try {
                const response = await axios.get(`/assessment/${id}`); // Call the FastAPI endpoint to get the specific assessment
                setAssessment(response.data.data); // Adjust based on the response structure
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAssessment();
    }, [id]);

    if (loading) return <div>Loading assessment...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!assessment) return <div>Assessment not found.</div>;

    return (
        <div className="assessment-detail-container">
            <h1 className="assessment-title">{assessment.name}</h1>
            <p className="assessment-description">This assessment tests your knowledge of {assessment.name}.</p>
            <p className="assessment-meta">Total Marks: {assessment.total_marks}</p>
            <p className="assessment-course">Suitable for course: {assessment.course_id}</p>
            <div className="warning-message">
                <p>Please ensure you are ready before starting the assessment. Good luck!</p>
            </div>
            <button className="take-assessment-btn">Take Assessment</button>
        </div>
    );
}

export default AssessmentDetail; 