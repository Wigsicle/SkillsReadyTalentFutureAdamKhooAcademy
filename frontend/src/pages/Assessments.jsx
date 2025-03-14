import React from "react";
import "../styles.css"; // Import global styles

function Assessments() {
    // Fake assessment data
    const fakeAssessments = [
        {
            assessmentId: "1",
            name: "Computer Science Fundamentals",
            total_marks: 100,
            course_id: "CS101",
        },
        {
            assessmentId: "2",
            name: "Data Structures and Algorithms",
            total_marks: 80,
            course_id: "CS102",
        },
        {
            assessmentId: "3",
            name: "Web Development Basics",
            total_marks: 90,
            course_id: "CS103",
        },
    ];

    return (
        <div className="assessments-container">
            <h1>Assess Your Skills & Earn Certifications</h1>
            <p>Prepare for industry-leading certifications with our expert-designed assessment tests.</p>

            {/* Assessment List */}
            <div className="assessment-list">
                {fakeAssessments.map((assessment) => (
                    <div className="assessment-card" key={assessment.assessmentId}>
                        <div className="card-inner">
                            <div className="card-front">
                                <h3 className="assessment-title">{assessment.name}</h3>
                                <p>Total Marks: {assessment.total_marks}</p>
                                <p>Course ID: {assessment.course_id}</p>
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