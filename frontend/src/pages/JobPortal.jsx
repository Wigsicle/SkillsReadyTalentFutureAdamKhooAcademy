import React, { useState, useEffect } from "react";
import "../styles.css"; // Import global styles
import BreadCrumb from "../components/Breadcrumb";
import { getUser, getJob, applyJob, getApplications } from "../static/api"; // Assuming you have an applyForJob API function for submitting job applications
import { useAuth } from '../static/AuthContext';

function JobPortal() {
    const authHandler = useAuth();
    const [userId, setUserId] = useState(0);
    const [jobs, setJobs] = useState([]);
    const [selectedJob, setSelectedJob] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");
    const [appliedJobs, setAppliedJobs] = useState([]); // Now stores jobId along with application data
    const [view, setView] = useState('available'); // Toggle between 'available' and 'applied' jobs
    const [loading, setLoading] = useState(true); // Loading state for API call
    const [applicationData, setApplicationData] = useState(null); // Store the user's application data for a selected job

    // Fetch jobs and user's applications when the component is mounted
    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const token = authHandler.getToken(); // Get token from localStorage
                const currentUser = await getUser(token.token);
                const response = await getJob(token.token); // Get jobs data
                if (currentUser.data && response.data) {
                    setUserId(currentUser.data.userId);
                    const jobData = response.data.jobs;
                    setJobs(jobData);

                    // Fetch the user's job applications
                    const applications = await getApplications(currentUser.data.userId, token.token);
                    if (applications.data) {
                        // Store applied jobs with full application data (including resumeLink, additionalInfo)
                        setAppliedJobs(applications.data.applications);
                    }
                } else {
                    if (response.error === "Unauthorized") {
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
    }, [authHandler]);

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
            industryId: selectedJob ? selectedJob.industryId : prevData.industryId, // Include industryId from selectedJob
        }));
    };

    // Handle form submission for applying to a job
    const handleApplySubmit = async (e) => {
        e.preventDefault();
        try {
            const token = authHandler.getToken(); // Get token from localStorage
            applicationData.applicantId = userId;
            const response = await applyJob(applicationData, token.token);
            if (response.data) {
                alert("Successfully applied for the job");
                window.location.reload();
            } else {
                if (response.error === "Unauthorized") {
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

    // Handle job selection for the modal
    const handleJobClick = (job) => {
        setSelectedJob(job);

        // If the job has been applied for, fetch the application data
        const appliedJobData = appliedJobs.find((app) => app.jobId === job.jobId);
        if (appliedJobData) {
            setApplicationData({
                resumeLink: appliedJobData.resumeLink || "",
                additionalInfo: appliedJobData.additionalInfo || "",
                jobId: job.jobId,
                industryId: job.industryId || "", // Set industryId when job is selected
            });
        } else {
            setApplicationData(null); // Reset application data if the job hasn't been applied for
        }
    };

    return (
        <div className="job-portal">
            <BreadCrumb title={"Jobs"} homeRoute={"/"} />

            {/* Search Bar */}
            <div className="job-portal-container">
                <h1>{view === 'available' ? 'Available Jobs' : 'Applied Jobs'}</h1>
                <p>A sea of opportunities awaits.</p>


                <div class="btn-group mb-3">
                    <button
                        className={`btn ${view === 'available' ? 'btn-light' : 'btn-light'}`}
                        onClick={() => setView('available')}
                    >
                        Available Jobs
                    </button>
                    <button
                        className={`btn ${view === 'applied' ? 'btn-dark' : 'btn-dark'}`}
                        onClick={() => setView('applied')}
                    >
                        Applied Jobs
                    </button>
                </div>
         
            
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
                    {view === 'available'
                        ? filteredJobs.map((job) => (
                            <div
                                key={job.jobId}
                                className={`card ${selectedJob?.jobId === job.jobId ? "selected" : ""}`}
                                onClick={() => handleJobClick(job)}
                                data-bs-toggle="modal"
                                data-bs-target="#jobModal"
                            >
                                <div className="card-body">
                                    <h3 className="card-title">{job.name}</h3>
                                    <p className="card-text">{job.companyName}</p>
                                    <p className="card-text">{job.employmentValue}</p>
                                    <p className="card-text">{job.startDate}</p>

                                </div>
                                <div class="card-footer text-body-light">
                                    {/* Apply Button */}
                                    <button
                                    className="btn btn-dark"
                                    disabled={appliedJobs.some(app => app.jobId === job.jobId)} // Disable if the jobId is in appliedJobs
                                    >
                                        {appliedJobs.some(app => app.jobId === job.jobId) ? "Already Applied" : "Apply"}
                                    </button>
                                </div>
                            </div>
                        ))
                        : jobs
                            .filter((job) => appliedJobs.some(app => app.jobId === job.jobId)) // Show only jobs the user has applied for
                            .map((job) => (
                                <div key={job.jobId} className="card" onClick={() => handleJobClick(job)} data-bs-toggle="modal" data-bs-target="#jobModal">
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
                                    {view === 'available' && (
                                        <form onSubmit={handleApplySubmit}>
                                            <div className="mb-3">
                                                <label htmlFor="resumeLink" className="form-label">Resume Link</label>
                                                <input
                                                    type="url"
                                                    id="resumeLink"
                                                    name="resumeLink"
                                                    className="form-control"
                                                    value={applicationData ? applicationData.resumeLink : ''}
                                                    onChange={handleApplicationChange}
                                                    disabled={appliedJobs.some(app => app.jobId === selectedJob.jobId)}
                                                    required
                                                />
                                            </div>

                                            <div className="mb-3">
                                                <label htmlFor="additionalInfo" className="form-label">Additional Information</label>
                                                <textarea
                                                    id="additionalInfo"
                                                    name="additionalInfo"
                                                    className="form-control"
                                                    value={applicationData ? applicationData.additionalInfo : ''}
                                                    onChange={handleApplicationChange}
                                                    disabled={appliedJobs.some(app => app.jobId === selectedJob.jobId)}
                                                />
                                            </div>

                                            <button type="submit" className="btn btn-dark" disabled={appliedJobs.some(app => app.jobId === selectedJob.jobId)}>
                                                {appliedJobs.some(app => app.jobId === selectedJob.jobId) ? "Already Applied" : "Apply"}
                                            </button>
                                        </form>
                                    )}

                                    {view === 'applied' && applicationData && (
                                        <div>
                                            <p><strong>Resume Link:</strong> {applicationData.resumeLink}</p>
                                            <p><strong>Additional Info:</strong> {applicationData.additionalInfo}</p>
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <p>No selected job</p>
                            )}
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-light" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default JobPortal;
