-- Insert all tables with no FK dependency first
insert into public.user_type (id,value) VALUES (1,'Student'),(2,'Instructor'),(3,'Administrator');

insert into public.employment_type (id, value, short_val) values (1,'Full-Time','FT'),(2,'Part-Time','PT'),(3,'Intern','INT'),(4,'Temporary','TMP');

insert into public.country (id,name,short_name) values (1,'Singapore','SG'),(2,'Malaysia','MY'),(3,'Brunei','BRN'),(4,'Indonesia','IDN'),(5,'India','IND'),(6,'Thailand','TH');

insert into public.industry (name, short_name) values 
('Arts', 'Arts'), -- 1
('Science', 'Sci'), -- 2
('Marketing', 'Mkt'), -- 3
('Computing', 'Comp'), -- 4 
('Math', 'Math'), -- 5
('Environment', 'Env'); -- 6

insert into public.user (password, email, first_name, last_name, address, country_id, user_type_id) values 
('123', 'alice@example.com', 'Alice', 'Johnson', '123 Maple St, New York, SG', 1, 1),
('123', 'bob@example.com', 'Bob', 'Smith', '456 Oak St, London, Malaysia', 2, 1),
('123', 'charlie@example.com', 'Charlie', 'Brown', '789 Pine St, Sydney, Brunei', 3, 1),
('123', 'diana@example.com', 'Diana', 'Evans', '321 Cedar St, Toronto, Indonesia', 4, 1),
('123', 'ethan@example.com', 'Ethan', 'Williams', '654 Birch St, Berlin, India', 5, 1),
('123', 'fiona@example.com', 'Fiona', 'Garcia', '987 Redwood St, Paris, Thailand', 6, 1);

-- Course/Assessment/Cert
insert into public.course (name, details, industry_id, cert_id) values 
('Creative Writing Workshop', 'Learn how to write', 1, 1), 
('Nutrition and Wellness', 'Learn how to eat gooder', 2, 2),
('Digital Marketing Strategies', 'Learn how to sell', 3, 3),
('Data Science', 'Learn how to earth', 4, 4),
('Advanced Calculus', 'Learn how to be a computer', 5, 5),
('History of Art', 'Learn how to become a McDonalds employee.', 1, 6),
('Environmental Science', 'Learn how to earth', 6, 7),
('Environmental Science 2', 'Learn how to earth some MORE', 6, 8);

INSERT INTO public.assessment (name, total_marks, question_paper, course_id) values 
('Creative Writing Workshop', 100, '{"questions": [{"q": "Write a short story about adventure.", "marks": 50}, {"q": "Describe the importance of character development.", "marks": 50}]}', 1),
('Nutrition and Wellness', 100, '{"questions": [{"q": "List five essential nutrients and their benefits.", "marks": 40}, {"q": "Explain the role of hydration in health.", "marks": 30}, {"q": "Create a balanced meal plan for a day.", "marks": 30}]}', 2),
('Digital Marketing Strategies', 100, '{"questions": [{"q": "Define SEO and explain its importance.", "marks": 20}, {"q": "What are three key elements of a successful social media campaign?", "marks": 40}, {"q": "Describe the impact of content marketing.", "marks": 40}]}', 3),
('Data Science', 100, '{"questions": [{"q": "What is the difference between supervised and unsupervised learning?", "marks": 30}, {"q": "Explain how regression analysis is used in data science.", "marks": 40}, {"q": "Discuss a real-world application of data science.", "marks": 30}]}', 4),
('Advanced Calculus', 100, '{"questions": [{"q": "Solve the integral of x^2 dx.", "marks": 25}, {"q": "Prove the limit definition of a derivative.", "marks": 25}, {"q": "Find the Taylor series expansion of sin(x).", "marks": 50}]}', 5),
('History of Art', 100, '{"questions": [{"q": "Analyze the impact of the Renaissance on modern art.", "marks": 40}, {"q": "Compare and contrast Baroque and Impressionist art styles.", "marks": 30}, {"q": "Describe a famous work of art and its historical significance.", "marks": 30}]}', 6),
('Environmental Science', 100, '{"questions": [{"q": "What are the main causes of climate change?", "marks": 35}, {"q": "Explain how deforestation affects ecosystems.", "marks": 35}, {"q": "Discuss three methods to reduce carbon emissions.", "marks": 30}]}', 7),
('Environmental Science 2', 100, '{"questions": [{"q": "Describe the process of carbon sequestration.", "marks": 30}, {"q": "Explain the significance of biodiversity conservation.", "marks": 40}, {"q": "Discuss the role of renewable energy in sustainability.", "marks": 30}]}', 8);

INSERT INTO public.certificate(id, name, description, course_id, years_valid) VALUES 
(1, 'Creative Writer', 'This certifies the holder has completed the "Creative Writing Workshop".', 1, 2),
(2, 'Nutrition and Wellness Advocate', 'This person has learned how to eat gooder', 2, 2),
(3, 'Digital Marketing Strategist', 'This person is now great at selling this pen!', 3, 2),
(4, 'Data Science Initiate', 'This person has learned the basics of Data Science.', 4, 2),
(5, 'Certificate of Advanced Calculus (Basic)', 'Maybe they know something, hm...', 5, 2),
(6, 'Art Historian', 'They may not know how to paint, but they know about how people painted. Sounds paint-ful.', 6, 2),
(7, 'Environmental Scientist (Basic)', 'They know about rocks.', 7, 1),
(8, 'Environmental Scientist (Advanced)', 'They know about paper?', 8, 4);

-- User 1:M relation to Course/Assessment/Cert
insert into public.course_progress (cleared, student_id, course_id) VALUES
(TRUE, 1, 1),
(TRUE, 2, 2),
(TRUE, 3, 3),
(TRUE, 4, 4),
(TRUE, 5, 5),
(TRUE, 6, 6),
(TRUE, 1, 7),
(TRUE, 2, 8),
(TRUE, 3, 4),
(FALSE, 1, 4);

insert into public.assessment_attempt (earned_marks, attempted_on, remarks, student_id, assessment_id) values
(85, '20250310 10:30:00 AM', 'Well-structured story with good character development.', 1, 1),
(70, '20250311 02:15:00 PM', 'Missed one key nutrient, but good explanation.', 2, 2),
(90, '20250312 09:45:00 AM', 'Excellent understanding of SEO and content marketing.', 3, 3),
(65, '20250313 04:30:00 PM', 'Basic understanding, but needs more depth in analysis.', 4, 4),
(95, '20250314 12:00:00 PM', 'Accurate calculus solutions with clear explanations.', 5, 5),
(80, '20250315 11:25:00 AM', 'Good insights into art history, but could expand more.', 6, 6),
(75, '20250316 02:50:00 PM', 'Identified major causes of climate change well.', 1, 7),
(88, '20250317 09:35:00 AM', 'Strong understanding of biodiversity conservation.', 2, 8),
(60, '20250318 03:10:00 PM', 'Some answers lacked detail, but core concepts were correct.', 3, 4),
(92, '20250319 10:45:00 AM', 'Excellent discussion on renewable energy sustainability.', 4, 8);

insert into public.user_cert (issued_on, expires_on, user_id, cert_id) values 
('20241011', '20261011', 1, 1),
('20241011', '20261011', 2, 2),
('20241011', '20261011', 3, 3),
('20241011', '20261011', 4, 4),
('20241011', '20261011', 5, 5),
('20241011', '20261011', 6, 6),
('20241011', '20261011', 1, 7),
('20241011', '20261011', 2, 8);

-- Job Service Tables: Company, Job_Listing, Application (Employment Type is above)
INSERT INTO public.company(name, address, industry_id, country_id) VALUES
('Tech Innovators Inc.', '123 Tampines St, SG', 1, 1),
('Global Marketing Solutions', '456 Business St, Kuala Lumpur, MY', 4, 2),
('Data Insights Ltd.', '789 Analytics Ave, Brunei Darussalam, Brunei', 2, 3);

INSERT INTO public.job_listing(name, description, start_date, end_date, available_spot_count, company_id, employment_type_id, monthly_salary) VALUES
('Software Engineer', 'Develop and maintain web applications.', '2025-04-01 09:00:00', '2025-12-31 18:00:00', 5, 1, 1, 6000),
('Marketing Specialist', 'Plan and execute marketing campaigns.', '2025-04-15 09:00:00', '2025-10-15 18:00:00', 3, 2, 2, 4500),
('Data Analyst', 'Analyze business data for insights.', '2025-05-01 09:00:00', '2025-11-30 18:00:00', 4, 3, 1, 5500),
('HR Manager', 'Manage recruitment and employee relations.', '2025-04-10 09:00:00', '2025-10-10 18:00:00', 2, 1, 3, 5000),
('Project Manager', 'Oversee project execution and delivery.', '2025-06-01 09:00:00', '2025-12-01 18:00:00', 2, 2, 1, 7000),
('Customer Support Representative', 'Handle customer queries and issues.', '2025-03-20 09:00:00', '2025-09-20 18:00:00', 6, 3, 4, 3500),
('Network Engineer', 'Maintain and improve company networks.', '2025-05-15 09:00:00', '2025-11-15 18:00:00', 3, 1, 2, 6200),
('Graphic Designer', 'Create visual designs for branding.', '2025-04-05 09:00:00', '2025-10-05 18:00:00', 4, 2, 3, 4800),
('Cybersecurity Specialist', 'Ensure company security protocols.', '2025-07-01 09:00:00', '2025-12-31 18:00:00', 2, 3, 1, 7500),
('Content Writer', 'Write and edit content for various platforms.', '2025-03-25 09:00:00', '2025-09-25 18:00:00', 5, 1, 4, 4000);

INSERT INTO public.application(applied_on, edited_on, resume_link, additional_info, status, applicant_id, listing_id, industry_id) VALUES
('2025-03-10 14:30:00', NULL, 'https://example.com/resumes/resume1.pdf', 'Looking forward to this opportunity.', 'Pending', 1, 3, 2),
('2025-03-12 09:15:00', '2025-03-13 10:00:00', 'https://example.com/resumes/resume2.pdf', 'Available for immediate start.', 'Reviewed', 2, 5, 1),
('2025-03-14 16:45:00', NULL, 'https://example.com/resumes/resume3.pdf', 'Excited to join your team.', 'Pending', 3, 7, 3),
('2025-03-15 11:00:00', '2025-03-16 12:30:00', 'https://example.com/resumes/resume4.pdf', 'Have prior experience in this role.', 'Interview Scheduled', 4, 2, 4),
('2025-03-16 08:50:00', NULL, 'https://example.com/resumes/resume5.pdf', 'Willing to relocate.', 'Pending', 5, 9, 5),
('2025-03-17 10:20:00', '2025-03-18 14:15:00', 'https://example.com/resumes/resume6.pdf', 'I can start within two weeks.', 'Reviewed', 6, 1, 6),
('2025-03-18 14:10:00', NULL, 'https://example.com/resumes/resume7.pdf', 'Passionate about cybersecurity.', 'Pending', 1, 8, 3),
('2025-03-19 13:35:00', '2025-03-20 09:50:00', 'https://example.com/resumes/resume8.pdf', 'Strong background in networking.', 'Interview Scheduled', 2, 4, 1),
('2025-03-20 15:25:00', NULL, 'https://example.com/resumes/resume9.pdf', 'Available for remote work.', 'Pending', 3, 10, 2),
('2025-03-21 09:05:00', '2025-03-22 11:45:00', 'https://example.com/resumes/resume10.pdf', 'Excited to contribute to your team.', 'Reviewed', 4, 6, 4),
('2025-03-22 17:40:00', NULL, 'https://example.com/resumes/resume11.pdf', 'Proficient in multiple programming languages.', 'Pending', 5, 1, 5),
('2025-03-23 12:30:00', '2025-03-24 14:20:00', 'https://example.com/resumes/resume12.pdf', 'I have worked in this industry for 5 years.', 'Interview Scheduled', 6, 3, 6),
('2025-03-24 14:50:00', NULL, 'https://example.com/resumes/resume13.pdf', 'Would love to discuss this opportunity further.', 'Pending', 1, 7, 2),
('2025-03-25 10:30:00', '2025-03-26 13:10:00', 'https://example.com/resumes/resume14.pdf', 'Available for both full-time and contract roles.', 'Reviewed', 2, 5, 1),
('2025-03-26 09:45:00', NULL, 'https://example.com/resumes/resume15.pdf', 'Looking for a long-term position.', 'Pending', 3, 9, 3);
