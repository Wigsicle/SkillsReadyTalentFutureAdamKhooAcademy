import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ Import useNavigate
import "../styles.css"; // Import global styles

function Courses() {
    const navigate = useNavigate(); // ✅ Initialize navigate function

    // Dummy categories
    const categories = ["Data Science", "IT Certifications", "Leadership", "Web Development", "Communication", "Business Analytics"];
    const [selectedCategory, setSelectedCategory] = useState("Data Science");

    // Dummy course data
    const courses = [
        {
            id: 1,
            title: "Invest like Adam Khoo",
            instructor: "Julian Melanson",
            rating: 4.5,
            reviews: "44,829",
            image: "https://via.placeholder.com/300x200", // Placeholder image
        },
        {
            id: 2,
            title: "The Complete Crypto Trading Course",
            instructor: "Ing. Tomas Moravek",
            rating: 4.2,
            reviews: "1,773",
            image: "https://via.placeholder.com/300x200",
        },
        {
            id: 3,
            title: "How to get rich 101",
            instructor: "Anton Voroniuk",
            rating: 4.5,
            reviews: "508",
            image: "https://via.placeholder.com/300x200",
        },
        {
            id: 4,
            title: "Mastering SEO With ChatGPT: Ultimate Beginner's Guide",
            instructor: "Anton Voroniuk",
            rating: 4.5,
            reviews: "260",
            image: "https://via.placeholder.com/300x200",
        },
    ];

    return (
        <div className="courses-container">
            <h1>All the skills you need in one place</h1>
            <p>From critical skills to technical topics, we support your professional development.</p>

            {/* Category Navigation */}
            <div className="category-tabs">
                {categories.map((category, index) => (
                    <button
                        key={index}
                        className={`category-btn ${selectedCategory === category ? "active" : ""}`}
                        onClick={() => setSelectedCategory(category)}
                    >
                        {category}
                    </button>
                ))}
            </div>

            {/* Course List */}
            <div className="course-list">
                {courses.map((course) => (
                    <div className="course-card" key={course.id}>
                        <img src={course.image} alt={course.title} className="course-image" />
                        <div className="course-details">
                            <h3 className="course-title">{course.title}</h3>
                            <p className="course-instructor">{course.instructor}</p>
                            <div className="course-rating">
                                ⭐ {course.rating} ({course.reviews} reviews)
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* View More Button */}
            <button className="view-more-btn">Show all {selectedCategory} courses</button>

            {/* Back to Home Button with Navigation */}
            <button className="back-to-home-btn" onClick={() => navigate("/")}>
                Back to Home
            </button>
        </div>
    );
}

export default Courses;
