import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ Import useNavigate
import "../styles.css"; // Import global styles
import catImage from '../assets/cat.jpg';  // Import the image

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
            image: "https://media.istockphoto.com/id/1361394182/photo/funny-british-shorthair-cat-portrait-looking-shocked-or-surprised.jpg?s=612x612&w=0&k=20&c=6yvVxdufrNvkmc50nCLCd8OFGhoJd6vPTNotl90L-vo=", // Placeholder image
        },
        {
            id: 2,
            title: "The Complete Crypto Trading Course",
            instructor: "Ing. Tomas Moravek",
            rating: 4.2,
            reviews: "1,773",
            image: "https://media.istockphoto.com/id/1361394182/photo/funny-british-shorthair-cat-portrait-looking-shocked-or-surprised.jpg?s=612x612&w=0&k=20&c=6yvVxdufrNvkmc50nCLCd8OFGhoJd6vPTNotl90L-vo=",
        },
        {
            id: 3,
            title: "How to get rich 101",
            instructor: "Anton Voroniuk",
            rating: 4.5,
            reviews: "508",
            image: "https://media.istockphoto.com/id/1361394182/photo/funny-british-shorthair-cat-portrait-looking-shocked-or-surprised.jpg?s=612x612&w=0&k=20&c=6yvVxdufrNvkmc50nCLCd8OFGhoJd6vPTNotl90L-vo=",
        },
        {
            id: 4,
            title: "Mastering SEO With ChatGPT: Ultimate Beginner's Guide",
            instructor: "Anton Voroniuk",
            rating: 4.5,
            reviews: "260",
            image: "https://media.istockphoto.com/id/1361394182/photo/funny-british-shorthair-cat-portrait-looking-shocked-or-surprised.jpg?s=612x612&w=0&k=20&c=6yvVxdufrNvkmc50nCLCd8OFGhoJd6vPTNotl90L-vo=",
        },
    ];


    return (
        <div className="container-fluid">
            <h1>All the skills you need in one place</h1>
            <p>From critical skills to technical topics, we support your professional development.</p>


            {/* Course List */}
            <div className="card-list">
                {courses.map((course) => (
                    <div className="card" key={course.id}>
                        <img src={course.image} alt={course.title} className="card-img-top" />
                        <div className="card-body">
                            <h3 className="card-title">{course.title}</h3>
                            <p className="card-text">{course.instructor}</p>
                            <div className="course-rating">
                                ⭐ {course.rating} ({course.reviews} reviews)
                            </div>
                        </div>
                    </div>
                ))}
            </div>


            
        </div>
    );
}

export default Courses;
