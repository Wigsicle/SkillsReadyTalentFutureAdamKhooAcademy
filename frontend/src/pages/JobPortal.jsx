import React, { useState, useEffect } from "react";
import "../styles.css"; // Import global styles
import BreadCrumb from "../components/Breadcrumb";
import { getJob } from "../static/api"; // Assuming getJob is already defined for fetching jobs

function JobPortal() {
    // State for jobs and selected job
    const [jobs, setJobs] = useState([]);
    const [selectedJob, setSelectedJob] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");

    // Fetch jobs when the component is mounted
    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const response = await getJob(); // Make the API call to get jobs
                const jobData = response.data.jobs; // Assuming the response is structured as in the provided example
                setJobs(jobData);
            } catch (error) {
                console.error("Error fetching jobs:", error);
            }
        };
        fetchJobs();
    }, []);

    // Filter jobs based on search term
    const filteredJobs = jobs.filter((job) =>
        job.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.companyName.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="job-portal">
            <BreadCrumb title={"Jobs"} homeRoute={"/"} />

            {/* Search Bar */}
            <div className="job-portal-container">
                <h1>Available Jobs</h1>
                <p>A sea of opportunities awaits.</p>

                <div className="mb-3">
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
                        <div
                            key={job.jobId}
                            className={`card ${selectedJob?.jobId === job.jobId ? "selected" : ""}`}
                            onClick={() => setSelectedJob(job)}
                            data-bs-toggle="modal"
                            data-bs-target="#jobModal"
                        >
                            <div className="card-body">
                                <h3 className="card-title">{job.name}</h3>
                                <p className="card-text">{job.companyName}</p>
                                <p className="card-text">{job.employmentValue}</p>
                                <p className="card-text">{job.startDate}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Modal for Job Details */}
            <div className="modal fade" tabindex="-1" id="jobModal" aria-labelledby="jobModalLabel" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Job Details</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div className="modal-body">
                            {selectedJob !== null ? (
                                <div>
                                    <h2 className="pt-3">{selectedJob.name}</h2>
                                    <p className="job-company">{selectedJob.companyName}</p>
                                    <p className="job-location">{selectedJob.employmentValue} | {selectedJob.startDate} - {selectedJob.endDate}</p>
                                    <p className="job-description">{selectedJob.description}</p>
                                    <h3>Requirements:</h3>
                                    <ul className="job-requirements">
                                        <li>Monthly Salary: ${selectedJob.monthlySalary}</li>
                                        <li>Available Spot Count: {selectedJob.availableSpotCount}</li>
                                    </ul>
                                </div>
                            ) : (
                                <p>No selected job</p>
                            )}
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" className="btn btn-primary">Apply</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default JobPortal;
