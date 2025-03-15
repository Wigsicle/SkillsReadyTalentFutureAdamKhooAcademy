import React, { useState } from "react";
import "../styles.css"; // Import global styles
import BreadCrumb from "../components/Breadcrumb";

function JobPortal() {
    // Job list (dummy data)
    const jobs = [
        {
            id: 1,
            title: "Software Engineer",
            company: "Tech Innovators Inc.",
            location: "Remote",
            category: "Software Development",
            description: "We are looking for a skilled software engineer to develop and maintain web applications.",
            requirements: [
                "Experience in JavaScript, React, and Node.js",
                "Strong problem-solving skills",
                "Knowledge of RESTful APIs and cloud services",
            ],
            posted: "2 days ago",
            image: "https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png?w=1000&h=563&crop=1",
            type: "Full-time",
            rating: 4.7,
            reviews: 320,
        },
        {
            id: 2,
            title: "Cybersecurity Analyst",
            company: "SecureIT Solutions",
            location: "Singapore",
            category: "Cybersecurity",
            description: "Join our team to enhance security infrastructure and prevent cyber threats.",
            requirements: [
                "Understanding of penetration testing & security protocols",
                "Experience with network monitoring tools",
                "Familiarity with SIEM solutions",
            ],
            posted: "5 days ago",
            image: "https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png?w=1000&h=563&crop=1",
            type: "Contract",
            rating: 4.5,
            reviews: 215,
        },
        {
            id: 3,
            title: "Data Scientist",
            company: "AI Insights Ltd.",
            location: "New York, USA",
            category: "Data Science",
            description: "Analyze data trends and create machine learning models to improve decision-making.",
            requirements: [
                "Proficiency in Python, TensorFlow, and Pandas",
                "Strong statistical and mathematical skills",
                "Experience in AI and ML model deployment",
            ],
            posted: "1 week ago",
            image: "https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png?w=1000&h=563&crop=1",
            type: "Full-time",
            rating: 4.9,
            reviews: 410,
        },
    ];

    // State for job selection and search
    const [selectedJob, setSelectedJob] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");

    // Filter jobs based on search term
    const filteredJobs = jobs.filter((job) =>
        job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.location.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="job-portal">
            <BreadCrumb title={"Jobs"} homeRoute={"/"}/>

            {/* Search Bar */}

            <div className="job-portal-container">
                <h1>Available Jobs</h1>
                <p>A sea of opportunites awaits.</p>

                <div class="mb-3">
                <input
                        type="text"
                        className="form-control"
                        placeholder="Enter job title, company, or location"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />  
                </div>

                {/* Job List */}
                <div className="card-list">
                    {filteredJobs.map((job) => (
                        <div key={job.id} className={`card ${selectedJob?.id === job.id ? "selected" : ""}`} onClick={() => setSelectedJob(job)} data-bs-toggle="modal" data-bs-target="#jobModal">
                            <img src={job.image} alt={job.title} className="card-image-top" />
                            <div className="card-body">
                                <h3 className="card-title">{job.title}</h3>
                                <p className="card-text">{job.company}</p>
                                <p className="card-text">{job.location}</p>
                                <p className="card-text">{job.posted}</p>
                            </div>
                        </div>
                    ))}
                </div>

           
            </div>
 
        <div class="modal fade" tabindex="-1" id="jobModal" aria-labelledby="jobModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Job </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    
                        {selectedJob !== null ? (
                            <div>
                                <img src={selectedJob.image} alt={selectedJob.title} className="job-detail-image w-100" />
                                <h2 className="pt-3">{selectedJob.title}</h2>
                                <p className="job-company">{selectedJob.company}</p>
                                <p className="job-location">{selectedJob.location} | {selectedJob.type}</p>
                                <p className="job-category">Category: {selectedJob.category}</p>
                                <p className="job-description">{selectedJob.description}</p>
                                <h3>Requirements:</h3>
                                <ul className="job-requirements">
                                {selectedJob.requirements.map((req, index) => (
                                    <li key={index}>{req}</li>
                                ))}
                                </ul>
                            </div>
                        ) : (
                            <p>No selected job</p>
                        )}   
                        
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Apply</button>
                </div>
                </div>
            </div>
            </div>

        </div>
    );
}

export default JobPortal;
