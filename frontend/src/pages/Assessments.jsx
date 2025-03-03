import React from "react";
import "../styles.css"; // Import global styles

function Assessments() {
    // Dummy assessment data
    const assessments = [
        {
            id: 1,
            title: "Data Science Fundamentals | Certification Exam",
            description: "Test your knowledge on Python, Machine Learning, and Data Visualization. Includes 100+ questions with detailed explanations.",
            instructor: "Prof. John Doe",
            rating: 4.8,
            reviews: 5234,
            questions: 100,
            level: "Intermediate",
            image: "https://via.placeholder.com/300x200", // Placeholder image
        },
        {
            id: 2,
            title: "Cybersecurity & Ethical Hacking | Practice Test",
            description: "Assess your skills in penetration testing, network security, and cryptography. Includes real-world scenarios.",
            instructor: "Dr. Alice Smith",
            rating: 4.6,
            reviews: 4120,
            questions: 150,
            level: "Advanced",
            image: "https://via.placeholder.com/300x200",
        },
        {
            id: 3,
            title: "Cloud Computing & AWS Certification Exam",
            description: "Test your understanding of AWS, Azure, and GCP cloud services. Ideal for those preparing for AWS Certified Solutions Architect.",
            instructor: "Eng. Mark Thompson",
            rating: 4.9,
            reviews: 2890,
            questions: 120,
            level: "Beginner",
            image: "https://via.placeholder.com/300x200",
        },
    ];

    return (
        <div className="assessments-container">
            <h1>Assess Your Skills & Earn Certifications</h1>
            <p>Prepare for industry-leading certifications with our expert-designed assessment tests.</p>

            {/* Assessment List */}
            <div className="assessment-list">
                {assessments.map((assessment) => (
                    <div className="assessment-card" key={assessment.id}>
                        <img src={assessment.image} alt={assessment.title} className="assessment-image" />
                        <div className="assessment-details">
                            <h3 className="assessment-title">{assessment.title}</h3>
                            <p className="assessment-description">{assessment.description}</p>
                            <p className="assessment-instructor">{assessment.instructor}</p>
                            <div className="assessment-rating">
                                ⭐ {assessment.rating} ({assessment.reviews} reviews)
                            </div>
                            <div className="assessment-meta">
                                {assessment.questions} questions • {assessment.level}
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
