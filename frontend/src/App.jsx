import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Courses from "./pages/Courses";
import Assessments from "./pages/Assessments";
import Certificates from "./pages/Certificates";
import JobPortal from "./pages/JobPortal";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/courses" element={<Courses />} />
                <Route path="/assessments" element={<Assessments />} />
                <Route path="/certificates" element={<Certificates />} />
                <Route path="/job-portal" element={<JobPortal />} />
            </Routes>
        </Router>
    );
}

export default App;
