import React, { useState, useEffect } from "react";
import axios from 'axios';
import { useNavigate } from "react-router-dom";

function CreateAssessment() {
    const [name, setName] = useState("");
    const [courseId, setCourseId] = useState("");
    const [questions, setQuestions] = useState([]);
    const [selectedQuestionId, setSelectedQuestionId] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const response = await axios.get('/questions'); // Adjust this endpoint as needed
                console.log(response.data); // Log the entire response
                setQuestions(response.data.data); // Adjust based on the response structure
            } catch (err) {
                console.error(err);
            }
        };

        fetchQuestions();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/assessment/create', {
                name,
                courseId,
                questionId: selectedQuestionId,
            });
            navigate('/assessments'); // Redirect to assessments page after creation
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div>
            <h1>Create Assessment</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Assessment Name:</label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div>
                    <label>Course ID:</label>
                    <input type="text" value={courseId} onChange={(e) => setCourseId(e.target.value)} required />
                </div>
                <div>
                    <label>Select Question:</label>
                    <select value={selectedQuestionId} onChange={(e) => setSelectedQuestionId(e.target.value)} required>
                        <option value="">Select a question</option>
                        {questions.map((question) => (
                            <option key={question.id} value={question.id}>{question.name}</option>
                        ))}
                    </select>
                </div>
                <button type="submit">Create Assessment</button>
            </form>
        </div>
    );
}

export default CreateAssessment; 