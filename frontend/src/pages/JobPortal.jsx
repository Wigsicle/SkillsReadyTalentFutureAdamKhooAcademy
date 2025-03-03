import React, { useState } from "react";
import "../styles.css"; // Import global styles

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
            image: "https://via.placeholder.com/300x200",
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
            image: "https://via.placeholder.com/300x200",
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
            image: "https://via.placeholder.com/300x200",
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
            {/* Search Bar */}
            <div className="job-search-bar">
                <input
                    type="text"
                    placeholder="Enter job title, company, or location"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button className="search-btn">Search</button>
            </div>

            <div className="job-portal-container">
                {/* Job List */}
                <div className="job-list">
                    <h2>Available Jobs</h2>
                    {filteredJobs.map((job) => (
                        <div key={job.id} className={`job-card ${selectedJob?.id === job.id ? "selected" : ""}`} onClick={() => setSelectedJob(job)}>
                            <img src={job.image} alt={job.title} className="job-image" />
                            <div className="job-info">
                                <h3 className="job-title">{job.title}</h3>
                                <p className="job-company">{job.company}</p>
                                <p className="job-location">{job.location}</p>
                                <p className="job-posted">{job.posted}</p>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Job Details */}
                <div className="job-details">
                    {selectedJob ? (
                        <>
                            <img src={selectedJob.image} alt={selectedJob.title} className="job-detail-image" />
                            <h2>{selectedJob.title}</h2>
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
                            <div className="job-actions">
                                <button className="apply-btn">Quick Apply</button>
                                <button className="save-btn">Save</button>
                            </div>
                        </>
                    ) : (
                        <div className="job-placeholder">
                            <h2>Select a job</h2>
                            <p>Display details here</p>
                            <img src="https://via.placeholder.com/200x150" alt="Placeholder" />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default JobPortal;
