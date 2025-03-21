import React from "react";
import { Link } from "react-router-dom";
import "../styles.css"; // Ensure you import the CSS file

function Home() {
    return (
        <div className="container-fluid">
            <h1>Welcome to SRTFAKA!</h1>
            <p>Learn new skills, take assessments, earn certificates, and apply for jobs – all in one place!</p>

            <div className="container-fluid w-100 mt-5">

            <div class="p-3 mb-4 bg-body-tertiary rounded-3">
                <div class="container-fluid py-5">
                    <Link to="/courses" className="text-dark">
                        <h2 class="display-6 fw-bold">Browse Courses</h2>
                    </Link>
                <p class="col-md-8 fs-4">Start your journey now to be next best employee.</p>
                </div>
            </div>

            <div class="p-3 mb-4 bg-body-tertiary rounded-3">
                <div class="container-fluid py-5">
                <Link to="/assessments" className="text-dark">
                    <h2 class="display-6 fw-bold">Take an Assessment</h2>
                </Link>
                <p class="col-md-8 fs-4">Get certified upon successful completion.</p>
                </div>
            </div>
               
            <div class="p-3 mb-4 bg-body-tertiary rounded-3">
                <div class="container-fluid py-5">
                <Link to="/job-portal" className="text-dark">
                    <h2 class="display-6 fw-bold">Apply for Jobs</h2>
                </Link>
                <p class="col-md-8 fs-4">Use your certificates to apply for jobs.</p>
                </div>
            </div>
               
            
            </div>
        </div>
    );
}

export default Home;
