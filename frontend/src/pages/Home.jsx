import React from "react";
import { Link } from "react-router-dom";
import "../styles.css"; // Ensure you import the CSS file

function Home() {
    return (
        <div className="container">
            <h1>Welcome to SkillsReadyTalentFutureAdamKhooAcademy!</h1>
            <p>Learn new skills, take assessments, earn certificates, and apply for jobs – all in one place!</p>

            <div className="grid">
                <Link to="/courses" className="card">
                    <h2> Browse Courses</h2>
                    <p>Start your journey now to be next best employee.</p>
                </Link>

                <Link to="/assessments" className="card">
                    <h2> Take an Assessment</h2>
                    <p>Get certified upon successful completion.</p>
                </Link>

                <Link to="/job-portal" className="card">
                    <h2> Apply for Jobs</h2>
                    <p>Use your certificates to apply for jobs.</p>
                </Link>
            </div>
        </div>
    );
}

export default Home;
