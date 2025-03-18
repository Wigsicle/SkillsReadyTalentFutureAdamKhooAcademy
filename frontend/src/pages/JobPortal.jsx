import React, { useState, useEffect } from "react";
import "../styles.css"; // Import global styles
import BreadCrumb from "../components/Breadcrumb";
import { getUser, getJob, applyJob } from "../static/api"; // Assuming you have an applyForJob API function for submitting job applications
import { useAuth } from '../static/AuthContext';

function JobPortal() {

    const authHandler = useAuth(); 
    const [userId, setUserId] = useState(0)
    // State for jobs and selected job
    const [jobs, setJobs] = useState([]);
    const [selectedJob, setSelectedJob] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");

    // State for job application form
    const [applicationData, setApplicationData] = useState({
        applicantId: 0,
        jobId: 0,
        resumeLink: "",
        additionalInfo: "",
        industryId: 0
    });

    const [loading, setLoading] = useState(true); // Loading state for API call

    // Fetch jobs when the component is mounted
    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const token = authHandler.getToken(); // Get token from localStorage
                const currentUser = await getUser(token.token);
                setUserId(currentUser.data.userId);
                const response = await getJob(token.token); // Make the API call to get jobs
                if (currentUser.data && response.data) {
                    const jobData = response.data.jobs; // Assuming the response is structured as in the provided example
                    setJobs(jobData);
                } else {
                    if(response.error === "Unauthorized"){
                        authHandler.handleTokenExpired();
                    }
                }
  
            } catch (error) {
                console.error("Error fetching jobs:", error);
            } finally {
                setLoading(false); // Set loading to false after the data is fetched
            }
        };
        fetchJobs();
    }, []);

    // Filter jobs based on search term
    const filteredJobs = jobs.filter((job) =>
        job.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.companyName.toLowerCase().includes(searchTerm.toLowerCase())
    );

    // Handle input changes for job application form
    const handleApplicationChange = (e) => {
        const { name, value } = e.target;
        setApplicationData((prevData) => ({
            ...prevData,
            [name]: value,
            jobId: selectedJob ? selectedJob.jobId : prevData.jobId, // Ensure jobId is set from selectedJob
        }));
    };

    // Handle form submission for applying to a job
    const handleApplySubmit = async (e) => {
        e.preventDefault();
        try {
            // Make the API call to apply for the job
            const token = authHandler.getToken(); // Get token from localStorage
            applicationData.applicantId = userId;
            const response = await applyJob(applicationData, token.token);
            if (response.data) {
                alert("Successfully applied for the job");
                window.location.reload();
            } else {
                if(response.error === "Unauthorized"){
                    authHandler.handleTokenExpired();
                }
                console.error("Error applying for job:", response.error);
            }
        } catch (error) {
            console.error("Error submitting job application:", error);
        }
    };

    // If data is still loading, show a loading spinner
    if (loading) {
        return <div>Loading...</div>;
    }

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

            {/* Modal for Job Details and Application Form */}
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

                                    {/* Application Form */}
                                    <form onSubmit={handleApplySubmit}>
                                        <div className="mb-3">
                                            <label htmlFor="resumeLink" className="form-label">Resume Link</label>
                                            <input
                                                type="url"
                                                id="resumeLink"
                                                name="resumeLink"
                                                className="form-control"
                                                value={applicationData.resumeLink}
                                                onChange={handleApplicationChange}
                                                required
                                            />
                                        </div>

                                        <div className="mb-3">
                                            <label htmlFor="additionalInfo" className="form-label">Additional Information</label>
                                            <textarea
                                                id="additionalInfo"
                                                name="additionalInfo"
                                                className="form-control"
                                                value={applicationData.additionalInfo}
                                                onChange={handleApplicationChange}
                                            />
                                        </div>

                                        {/* Submit Button */}
                                        <button type="submit" className="btn btn-primary">Apply for Job</button>
                                    </form>
                                </div>
                            ) : (
                                <p>No selected job</p>
                            )}
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default JobPortal;
