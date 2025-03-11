import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Courses from "./pages/Courses";
import Assessments from "./pages/Assessments";
import Certificates from "./pages/Certificates";
import JobPortal from "./pages/JobPortal";
import Navbar from "./components/Navbar";
import { AuthProvider, useAuth } from './static/AuthContext'; // Import AuthProvider

function MainApp(){
    const newAuthHandler = useAuth();
    const loggedIn = newAuthHandler.checkAuth();
    return(
        <main className="w-100 container-fluid h-100">
            
        {loggedIn ? 
        <div className="row h-100">
            <div className="col-3 vh-100">
                <Navbar/>
            </div>
            <div className="col-9 p-5 contentContainer">
                    <Routes>
                        <Route path="/" element={<Home/>} />
                        <Route path="/profile" element={<Profile/>} />
                        <Route path="/courses" element={<Courses/>} />
                        <Route path="/assessments" element={<Assessments/>} />
                        <Route path="/certificates" element={<Certificates />} />
                        <Route path="/job-portal" element={<JobPortal/>} />
                        <Route path="*" element={<Profile />} />
                    </Routes>
            </div>
        </div>
        :   <div>
                <Routes>
                    <Route path="/login" element={<Login/>} />
                    <Route path="/register" element={<Register/>} />
                    <Route path="*" element={<Login />} />
                </Routes>
            </div>}

        
    </main>
    );
}
function App() {
    return (
        <AuthProvider>
        <Router>
            <MainApp/>
        </Router>
        </AuthProvider>
    );
}

export default App;
