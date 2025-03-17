import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ Import useNavigate
import "../styles.css"; // Import global styles
import BreadCrumb from "../components/Breadcrumb";

function Assessments() {
    const navigate = useNavigate(); // Initialize navigate function

    // Dummy assessment data
    const assessments = [
        {
            id: 1,
            title: "Data Science Fundamentals | Certification Exam",
            description: "Test your knowledge on Python, Machine Learning, and Data Visualization. Includes 100+ questions with detailed explanations.",
            instructor: "Prof. John Doe",
            rating: 4.8,
            reviews: 5234,
            image: "https://tinyurl.com/srtfakateampg", // Placeholder image
            level: "Intermediate",
        },
        {
            id: 2,
            title: "Cybersecurity & Ethical Hacking | Practice Test",
            description: "Assess your skills in penetration testing, network security, and cryptography. Includes real-world scenarios.",
            instructor: "Dr. Alice Smith",
            rating: 4.6,
            reviews: 4120,
            image: "https://tinyurl.com/srtfakateampg",
            level: "Advanced",
        },
        {
            id: 3,
            title: "Cloud Computing & AWS Certification Exam",
            description: "Test your understanding of AWS, Azure, and GCP cloud services. Ideal for those preparing for AWS Certified Solutions Architect.",
            instructor: "Eng. Mark Thompson",
            rating: 4.9,
            reviews: 2890,
            image: "https://tinyurl.com/srtfakateampg",
            level: "Beginner",
        },
    ];

    const [selectedAssessment, setSelectedAssessment] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");

    // Filter assessments based on search term
    const filteredAssessments = assessments.filter((assessment) =>
        assessment.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        assessment.instructor.toLowerCase().includes(searchTerm.toLowerCase()) ||
        assessment.reviews.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="container-fluid">
            <BreadCrumb title={"Assessments"} homeRoute={"/"} />
            <h1>Assess Your Skills & Earn Certifications</h1>
            <p>Prepare for industry-leading certifications with our expert-designed assessment tests.</p>

            {/* Search Input */}
            <div className="mb-3">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Enter assessment title, instructor, or rating"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            {/* Assessment List */}
            <div className="card-list">
                {filteredAssessments.map((assessment) => (
                    <div
                        key={assessment.id}
                        className={`card ${selectedAssessment?.id === assessment.id ? "selected" : ""}`}
                        onClick={() => setSelectedAssessment(assessment)}
                        data-bs-toggle="modal"
                        data-bs-target="#assessmentModal"
                    >
                        <img src={assessment.image} alt={assessment.title} className="card-image-top" />
                        <div className="card-body">
                            <h3 className="card-title">{assessment.title}</h3>
                            <p className="card-text">{assessment.instructor}</p>
                            <p className="card-text">{assessment.rating} ⭐</p>
                            <p className="card-text">{assessment.reviews} reviews</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Modal to show details of the selected assessment */}
            <div className="modal fade" tabindex="-1" id="assessmentModal" aria-labelledby="assessmentModalLabel" aria-hidden="true">
                <div className="modal-dialog modal-lg">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Assessment Details</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div className="modal-body">
                            {selectedAssessment !== null ? (
                                <div>
                                    <img src={selectedAssessment.image} alt={selectedAssessment.title} className="course-detail-image w-100" />
                                    <h2 className="pt-3"><b>{selectedAssessment.title}</b></h2>
                                    <p className="course-instructor">Taught By: {selectedAssessment.instructor}</p>
                                    <p className="course-rating">Rating: {selectedAssessment.rating} ⭐</p>
                                    <p className="course-reviews">Reviews: {selectedAssessment.reviews}</p>
                                    <p className="course-level">Level: {selectedAssessment.level}</p>
                                    <p className="course-description">{selectedAssessment.description}</p>

                                </div>
                            ) : (
                                <p>No selected assessment</p>
                            )}
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-dark" data-bs-dismiss="modal">Begin</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Assessments;
