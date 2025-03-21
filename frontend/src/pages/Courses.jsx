import React, { useState, useEffect } from "react";
import "../styles.css"; // Import global styles
import BreadCrumb from "../components/Breadcrumb";
import { getUser, getCourses, getCourseById, joinCourse } from "../static/api"; // Ensure these imports exist
import { useAuth } from "../static/AuthContext";

function Courses() {
  const authHandler = useAuth();
  const [userId, setUserId] = useState(0);
  const [courses, setCourses] = useState([]); // Store all courses
  const [selectedCourse, setSelectedCourse] = useState(null); // Store selected course for modal
  const [searchCourseTerm, setSearchCourseTerm] = useState(""); // Store search term for filtering
  const [loading, setLoading] = useState(true);

  // Fetch courses and user information on component mount
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const token = authHandler.getToken(); // Get token from localStorage
        const currentUser = await getUser(token.token); // Fetch current user info
        setUserId(currentUser.data.id);

        // Fetch all courses from the backend
        const response = await getCourses(token.token);
        setCourses(response.data.courses || []);
      } catch (error) {
        console.error("Error fetching courses:", error);
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

  // Filter courses based on the search term
  const filteredCourses = courses.filter((course) =>
    course.title.toLowerCase().includes(searchCourseTerm.toLowerCase()) ||
    course.instructor.toLowerCase().includes(searchCourseTerm.toLowerCase()) ||
    course.reviews.toLowerCase().includes(searchCourseTerm.toLowerCase())
  );

  // Handle joining a course
  const handleJoinCourse = async (courseId) => {
    try {
      const token = authHandler.getToken();
      const response = await joinCourse({ courseId, userId }, token.token);

      if (response.data) {
        alert("Successfully joined the course!");
      } else {
        alert("Error joining course");
      }
    } catch (error) {
      console.error("Error joining course:", error);
    }
  };

  return (
    <div className="container-fluid">
      <BreadCrumb title={"Courses"} homeRoute={"/"} />
      <h1>All the skills you need in one place</h1>
      <p>From critical skills to technical topics, we support your professional development.</p>

      {/* Search Bar */}
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Enter course title, instructor, or rating"
          value={searchCourseTerm}
          onChange={(e) => setSearchCourseTerm(e.target.value)} // Update search term
        />
      </div>

      {/* Course List */}
      <div className="card-list">
        {filteredCourses.map((course) => (
          <div
            key={course.id}
            className={`card ${selectedCourse?.id === course.id ? "selected" : ""}`}
            onClick={() => setSelectedCourse(course)}  // Update selected course for the modal
            data-bs-toggle="modal"
            data-bs-target="#courseModal"
          >
            <img src={course.image} alt={course.title} className="card-image-top" />
            <div className="card-body">
              <h3 className="card-title">{course.title}</h3>
              <p className="card-text">{course.instructor}</p>
              <p className="card-text">{course.rating}</p>
              <p className="card-text">{course.reviews}</p>
              <button
                onClick={(e) => {
                  e.stopPropagation();  // Prevent triggering the parent div's onClick event
                  handleJoinCourse(course.id); // Join course on button click
                }}
                className="btn btn-primary"
              >
                Join Course
              </button>
            </div>
          </div>
        ))}
      </div>
      

      {/* Course Modal for Course Details */}
      <div className="modal fade" tabIndex="-1" id="courseModal" aria-labelledby="courseModalLabel" aria-hidden="true">
        <div className="modal-dialog modal-lg">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Course</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              {selectedCourse ? (
                <div>
                  <img src={selectedCourse.image} alt={selectedCourse.title} className="course-detail-image w-100" />
                  <h2 className="pt-3"><b>{selectedCourse.title}</b></h2>
                  <p className="course-instructor">Taught By: {selectedCourse.instructor}</p>
                  <p className="course-rating">Rating: {selectedCourse.rating}</p>
                  <p className="course-reviews">Reviews: {selectedCourse.reviews}</p>
                </div>
              ) : (
                <p>No selected course</p>
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

export default Courses;
