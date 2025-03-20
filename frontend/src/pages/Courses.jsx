import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // ✅ Import useNavigate
import "../styles.css"; // Import global styles
import BreadCrumb from "../components/Breadcrumb";
import {getUser, getCourses, getCourseById, updateCourse, joinCourse, updateCourseProgress} from "../static/api";
import {useAuth} from "../static/AuthContext";


function Courses() {
    const authHandler = useAuth(); 
    const [userId, setUserId] = useState(0);
    const [course, setCourse] = useState([]);
    const [selectedCourse, setSelectedCourse] = useState(null);
    const [searchCourseTerm, setSearchCourseTerm] = useState("");
    const [appliedCourse, setAppliedCourse] = useState([]);
    const [progressId, setProgressId] = useState(0);
    const [viewCourse, setViewCourse] = useState('available');
    const [loading, setLoading] = useState(true);
    const [courseData, setCourseData] = useState(null);



    // Dummy course data
    // const courses = [
    //     {
    //         id: 1,
    //         title: "Invest like Adam Khoo",
    //         instructor: "Julian Melanson",
    //         rating: 4.5,
    //         reviews: "44,829",
    //         image: "https://media.istockphoto.com/id/1361394182/photo/funny-british-shorthair-cat-portrait-looking-shocked-or-surprised.jpg?s=612x612&w=0&k=20&c=6yvVxdufrNvkmc50nCLCd8OFGhoJd6vPTNotl90L-vo=", // Placeholder image
    //     },
    //     {
    //         id: 2,
    //         title: "The Complete Crypto Trading Course",
    //         instructor: "Ing. Tomas Moravek",
    //         rating: 4.2,
    //         reviews: "1,773",
    //         image: "https://media.istockphoto.com/id/1361394182/photo/funny-british-shorthair-cat-portrait-looking-shocked-or-surprised.jpg?s=612x612&w=0&k=20&c=6yvVxdufrNvkmc50nCLCd8OFGhoJd6vPTNotl90L-vo=",
    //     },
    //     {
    //         id: 3,
    //         title: "How to get rich 101",
    //         instructor: "Anton Voroniuk",
    //         rating: 4.5,
    //         reviews: "508",
    //         image: "https://media.istockphoto.com/id/1361394182/photo/funny-british-shorthair-cat-portrait-looking-shocked-or-surprised.jpg?s=612x612&w=0&k=20&c=6yvVxdufrNvkmc50nCLCd8OFGhoJd6vPTNotl90L-vo=",
    //     },
    //     {
    //         id: 4,
    //         title: "Mastering SEO With ChatGPT: Ultimate Beginner's Guide",
    //         instructor: "Anton Voroniuk",
    //         rating: 4.5,
    //         reviews: "260",
    //         image: "https://media.istockphoto.com/id/1361394182/photo/funny-british-shorthair-cat-portrait-looking-shocked-or-surprised.jpg?s=612x612&w=0&k=20&c=6yvVxdufrNvkmc50nCLCd8OFGhoJd6vPTNotl90L-vo=",
    //     },
    // ];

    // fetch courses and users application
    useEffect(() => {
        const fetchCourses = async () => {
          try {
            const token = authHandler.getToken(); // Get token from local storage
            const currentUser = await getUser(token.token); // Fetch user info
            const response = await getCourses(token.token); // Fetch courses data
            if (currentUser.data && response.data) {
              setUserId(currentUser.data.id);
              setCourses(response.data.courses);
    
              // Here you can also fetch the courses the user has already applied to
              // Assume appliedCourses API exists that fetches applied courses
              const appliedCoursesResponse = await getAppliedCourses(currentUser.data.id, token.token);
              setAppliedCourses(appliedCoursesResponse.data.courses || []);
            } else {
              if (response.error === "Unauthorized") {
                authHandler.handleTokenExpired();
              }
            }
          } catch (error) {
            console.error("Courses Fetch Error:", error);
          } finally {
            setLoading(false);
          }
        };
        fetchCourses();
      }, [authHandler]);
    

    // If data is still loading, show a loading spinner
    if (loading) {
        return <div>Loading...</div>;
    }
    
    // Filter courses based on search term
    const filteredCourses = courses.filter((course) =>
        course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        course.instructor.toLowerCase().includes(searchTerm.toLowerCase()) ||
        course.reviews.toLowerCase().includes(searchTerm.toLowerCase())
    );

  // Handle Join Course
  const handleJoinCourse = async (courseId) => {
    try {
      const token = authHandler.getToken();
      const response = await joinCourse({ courseId, userId }, token.token);

      if (response.data) {
        // If the user successfully joined the course, update the appliedCourses state
        setAppliedCourses((prev) => [...prev, response.data]);
        alert("Successfully joined the course!");
      } else {
        alert("Error joining course");
      }
    } catch (error) {
      console.error("Error joining course:", error);
    }
  };
//   const handleJobClick = (job) => {
//     setSelectedJob(job);

//     // If the job has been applied for, fetch the application data
//     const appliedJobData = appliedJobs.find((app) => app.jobId === job.jobId);
//     if (appliedJobData) {
//         setApplicationData({
//             resumeLink: appliedJobData.resumeLink || "",
//             additionalInfo: appliedJobData.additionalInfo || "",
//             jobId: job.jobId,
//             industryId: job.industryId || "", // Set industryId when job is selected
//         });
//     } else {
//         setApplicationData(null); // Reset application data if the job hasn't been applied for
//     }
// };


    return (
        <div className="container-fluid">
            <BreadCrumb title={"Courses"} homeRoute={"/"}/>
            <h1>All the skills you need in one place</h1>
            <p>From critical skills to technical topics, we support your professional development.</p>

            <div class="mb-3">
            <input
                    type="text"
                    className="form-control"
                    placeholder="Enter course title, instructor, or rating"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            {/* Course List */}
            <div className="card-list">
                    {filteredCourses.map((course) => (
                        <div key={course.id} className={`card ${selectedCourse?.id === course.id ? "selected" : ""}`} onClick={() => setSelectedCourse(course)} data-bs-toggle="modal" data-bs-target="#courseModal">
                            <img src={course.image} alt={course.title} className="card-image-top" />
                            <div className="card-body">
                                <h3 className="card-title">{course.title}</h3>
                                <p className="card-text">{course.instructor}</p>
                                <p className="card-text">{course.rating}</p>
                                <p className="card-text">{course.reviews}</p>
                            </div>
                        </div>
                    ))}
            </div>

            <div class="modal fade" tabindex="-1" id="courseModal" aria-labelledby="courseModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Course</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    
                        {selectedCourse !== null ? (
                            <div>
                                <img src={selectedCourse.image} alt={selectedCourse.title} className="course-detail-image w-100" />
                                <h2 className="pt-3"><b>{selectedCourse.title}</b></h2>
                                <p className="course-instructor">Taught By: {selectedCourse.instructor}</p>
                                <p className="course-rating">Rating: {selectedCourse.rating}</p>
                                <p className="course-reviews">Reviews: {selectedCourse.reviews}</p>
                                
                                Accordion
                                <div class="accordion" id="accordionExample">
                                    <div class="accordion-item">
                                        <h2 class="accordion-header">
                                        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                            PDF
                                        </button>
                                        </h2>
                                        <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
                                        <div class="accordion-body">
                                            <strong>This is the first item's accordion body.</strong> It is shown by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
                                        </div>
                                        </div>
                                    </div>
                                    <div class="accordion-item">
                                        <h2 class="accordion-header">
                                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                            Video
                                        </button>
                                        </h2>
                                        <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                        <div class="accordion-body">
                                            <strong>This is the second item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
                                        </div>
                                        </div>
                                    </div>
                    
                                </div>
                                {/*  */}
                            </div>
                        ) : (
                            <p>No selected course</p>
                        )}   
                        
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
                </div>
            </div>
            </div>
            
        </div>
    );
}

export default Courses;
