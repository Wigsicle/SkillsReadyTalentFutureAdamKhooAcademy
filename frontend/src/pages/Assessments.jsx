import React, { useEffect, useState } from "react";
import "../styles.css"; // Import global styles
import BreadCrumb from "../components/Breadcrumb";
import { getUser, getAsssessment, getAttempts, submitAssessmentResults, getCourses } from "../static/api"; // Assuming getCourses is the API call to fetch courses
import { useAuth } from '../static/AuthContext';

function Assessments() {
    const authHandler = useAuth();
    const [assessments, setAssessments] = useState([]); // State to hold assessment data
    const [attempts, setAttempts] = useState([]); // State to hold assessment attempts
    const [courses, setCourses] = useState([]); // State to hold courses data
    const [loading, setLoading] = useState(true); // State to manage loading state
    const [error, setError] = useState(null); // State to manage error messages
    const [searchTerm, setSearchTerm] = useState(""); // State for search term
    const [view, setView] = useState("available"); // View toggle for available/completed assessments
    const [selectedAssessment, setSelectedAssessment] = useState(null); // Store selected assessment for modal
    const [userAnswers, setUserAnswers] = useState({}); // Store user's answers for each question
    const [score, setScore] = useState(0); // Store total score
    const [submitted, setSubmitted] = useState(false); // Flag to check if assessment has been submitted
    const [userId, setUserId] = useState(null); // Store the user ID
    const [selectedCertId, setSelectedCertId] = useState(null); // State to store the certId for selected assessment

    // Function to fetch assessments from the backend
    const fetchAssessments = async () => {
        try {
            const token = authHandler.getToken(); // Get token from localStorage

            const response = await getAsssessment(token.token);
            if (response.data) {
                setAssessments(response.data.assessments); // Set the assessments data
            } else {
                if (response.error === "Unauthorized") {
                    authHandler.handleTokenExpired();
                }
                throw new Error(response.error || "Failed to fetch assessments");
            }
        } catch (err) {
            setError(err.message); // Set error message if fetch fails
        }
    };

    // Function to fetch assessment attempts from the backend
    const fetchAssessmentAttempts = async () => {
        try {
            const token = authHandler.getToken(); // Get token from localStorage

            const response = await getAttempts(token.token);
            if (response.data && response.data.attempts.length > 0) {
                setAttempts(response.data.attempts); // Set the attempts data
            } else {
                throw new Error("No attempts found.");
            }
        } catch (err) {
            setError(err.message); // Set error message if fetch fails
        }
    };

    // Function to fetch courses from the backend
    const fetchCourses = async () => {
        try {
            const token = authHandler.getToken(); // Get token from localStorage

            const response = await getCourses(token.token); // Assuming getCourses is the API call to fetch courses
            if (response.data) {
                setCourses(response.data.courses); // Set the courses data
            } else {
                if (response.error === "Unauthorized") {
                    authHandler.handleTokenExpired();
                }
                throw new Error(response.error || "Failed to fetch courses");
            }
        } catch (err) {
            setError(err.message); // Set error message if fetch fails
        }
    };

    // Fetch the user ID and assess their attempts on mount
    const fetchUserData = async () => {
        try {
            const token = authHandler.getToken();
            const userResponse = await getUser(token.token);
            if (userResponse.data) {
                setUserId(userResponse.data.userId); // Save the userId
            } else {
                throw new Error("Failed to fetch user data");
            }
        } catch (err) {
            setError(err.message);
        }
    };

    // Use useEffect to fetch assessments, attempts, courses, and user data when the component mounts
    useEffect(() => {
        fetchAssessments();
        fetchAssessmentAttempts();
        fetchUserData(); // Fetch user ID
        fetchCourses(); // Fetch courses data
    }, []);

    // Check if the user has attempted the assessment (based on both userId and assessmentId)
    const hasUserAttemptedAssessment = (assessmentId) => {
        if (!attempts || attempts.length === 0) {
            return false;
        }

        return attempts.some((attempt) => attempt.assessmentId == assessmentId && attempt.studentId == userId);
    };

    // Filter assessments based on search term and view state
    const filteredAssessments = assessments.filter((assessment) => {
        if (view === "available") {
            return !hasUserAttemptedAssessment(assessment.assessmentId) && assessment.name.toLowerCase().includes(searchTerm.toLowerCase());
        } else if (view === "completed") {
            return hasUserAttemptedAssessment(assessment.assessmentId) && assessment.name.toLowerCase().includes(searchTerm.toLowerCase());
        }
        return false;
    });

    // Handle view toggle between available and completed assessments
    const handleViewToggle = (viewType) => {
        setView(viewType);
    };

    // Get the result (score) of the completed assessment
    const getUserAssessmentResult = (assessmentId) => {
        const attempt = attempts.find(attempt => attempt.assessmentId == assessmentId && attempt.studentId == userId);
        return attempt ? attempt.earnedMarks : null; // Return the marks earned by the user, or null if not completed
    };

    // Handle assessment click to open modal and set the certId based on the selected assessment's course
    const handleAssessmentClick = (assessment) => {
        setSelectedAssessment(assessment);
        setSelectedCertId(courses.find(course => course.id === assessment.courseId)?.certId || null); // Set certId based on course
        setUserAnswers({}); // Reset user answers when new assessment is selected
        setScore(0); // Reset score
        setSubmitted(false); // Reset submit flag
    };

    // Handle user answer change
    const handleAnswerChange = (questionIndex, selectedOption) => {
        setUserAnswers(prevAnswers => {
            const updatedAnswers = {
                ...prevAnswers,
                [questionIndex]: selectedOption
            };

            // Recalculate score each time an answer changes
            calculateScore(updatedAnswers);

            return updatedAnswers;
        });
    };

    // Calculate total score
    const calculateScore = (updatedAnswers = userAnswers) => {
        if (!selectedAssessment) return;

        let totalScore = 0;
        selectedAssessment.questionAnswer.forEach((question, index) => {
            const userAnswer = updatedAnswers[index];
            if (userAnswer === question.answer) {
                totalScore += question.marks;
            }
        });
        setScore(totalScore);
    };

    // Handle assessment submission
    const handleSubmit = async () => {
        // Make sure score is up-to-date before submitting
        calculateScore(); 
        console.log("Total Score:", score);

        try {
            const token = authHandler.getToken();
            const currentUser = await getUser(token.token);
            const submissionData = {
                attemptId: 0, 
                earnedMarks: score, 
                attemptedOn: new Date().toISOString(), 
                remarks: "Submitted by student", 
                studentId: currentUser.data.userId, 
                assessmentId: selectedAssessment.assessmentId,
                certId: selectedCertId,
                userId: currentUser.data.userId
            };
            const response = await submitAssessmentResults(submissionData, token.token);
            if (currentUser.data && response.data) {
                alert("Assessment submitted successfully");
                setSubmitted(true); // Mark assessment as submitted
                window.location.reload(); 
            }
            else{
                if (response.error === "Unauthorized") {
                    authHandler.handleTokenExpired();
                }
                throw new Error(response.data.detail || "Failed to submit assessment");
            }
        } catch (err) {
            console.error("Error submitting assessment:", err);
            setError(err.message); 
        }
    };

    return (
        <div className="assessments-container">
            <BreadCrumb title={"Assessments"} homeRoute={"/"} />
            <h1>Assessments</h1>
            <p>Test yourself, be better.</p>

            {/* View Toggle */}
            <div className="btn-group mb-3">
                <button
                    className={`btn ${view === 'available' ? 'btn-light' : 'btn-light'}`}
                    onClick={() => handleViewToggle("available")}
                >
                    Available Assessments
                </button>
                <button
                    className={`btn ${view === 'completed' ? 'btn-dark' : 'btn-dark'}`}
                    onClick={() => handleViewToggle("completed")}
                >
                    Completed Assessments
                </button>
            </div>

            {/* Search Bar */}
            <div className="mb-3">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Enter assessment name"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            {/* Assessment Cards */}
            <div className="card-list">
                {filteredAssessments.map((assessment) => (
                    <div
                        key={assessment.assessmentId}
                        className="card"
                        onClick={() => handleAssessmentClick(assessment)}
                        data-bs-toggle="modal"
                        data-bs-target="#assessmentModal"
                    >
                        <div className="card-body">
                            <h3 className="card-title">{assessment.name}</h3>
                            <p className="card-text">Total Marks: {assessment.totalMarks}</p>
                            
                            {/* Display Course and CertId */}
                            <p className="card-text">
                                Course: {courses.find(course => course.id === assessment.courseId)?.name || "Unknown"} 
                                <br />
                            </p>
                        </div>
                        <div className="card-footer">
                            <button 
                                className="btn btn-dark"
                                disabled={hasUserAttemptedAssessment(assessment.assessmentId)}
                            >
                                {view === "available" 
                                    ? hasUserAttemptedAssessment(assessment.assessmentId) 
                                        ? "Assessment Completed"
                                        : "View Assessment" 
                                    : getUserAssessmentResult(assessment.assessmentId) !== null
                                        ? `Score: ${getUserAssessmentResult(assessment.assessmentId)}`
                                        : "View Results"
                                }
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Modal for Assessment Details */}
            <div className="modal fade" id="assessmentModal" tabIndex="-1" aria-labelledby="assessmentModalLabel" aria-hidden="true">
                <div className="modal-dialog modal-lg">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title" id="assessmentModalLabel">Assessment Details</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div className="modal-body">
                            {selectedAssessment ? (
                                <div>
                                    <h2>{selectedAssessment.name}</h2>
                                    <p>Total Marks: {selectedAssessment.totalMarks}</p>
                                    
                                    {/* Display Course and CertId */}
                                    <p>
                                        Course: {courses.find(course => course.id === selectedAssessment.courseId)?.name || "Unknown"} 
                                        <br />
                                        Cert ID: {selectedCertId || "N/A"} {/* Display selectedCertId */}
                                    </p>

                                    {/* Show results if the assessment is completed */}
                                    {hasUserAttemptedAssessment(selectedAssessment.assessmentId) ? (
                                        <div>
                                            <p>Your score: {getUserAssessmentResult(selectedAssessment.assessmentId)}</p>
                                        </div>
                                    ) : (
                                        <div>
                                            {selectedAssessment.questionAnswer.map((question, index) => (
                                                <div className="container-fluid mt-3" key={index}>
                                                    <h5>{question.question}</h5>
                                                    {question.options.map((option, i) => (
                                                        <div className="container-fluid" key={i}>
                                                            <label>
                                                                <input
                                                                    type="radio"
                                                                    name={`question-${index}`}
                                                                    value={option}
                                                                    checked={userAnswers[index] === option}
                                                                    onChange={() => handleAnswerChange(index, option)}
                                                                />
                                                                {option}
                                                            </label>
                                                        </div>
                                                    ))}
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <p>Loading...</p>
                            )}
                        </div>
                        <div className="modal-footer">
                            {hasUserAttemptedAssessment(selectedAssessment?.assessmentId) ? (
                                <p>Assessment already completed</p>
                            ) : (
                                <button className="btn btn-primary" onClick={handleSubmit}>
                                    Submit Assessment
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Assessments;
