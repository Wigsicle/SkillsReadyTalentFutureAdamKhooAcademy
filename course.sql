insert into public.user () values ();

insert into public.employment_type (id, value, short_val) values (1,'Full-Time','FT'),(2,'Part-Time','PT'),(3,'Intern','INT'),(4,'Temporary','TMP');

insert into public.user_type (id,value) VALUES (1,'Student'),(2,'Instructor'),(3,'Administrator');

insert into public.country (id,name,short_name) values (1,'Singapore','SG'),(2,'Malaysia','MY'),(3,'Brunei','BRN'),(4,'Indonesia','IDN'),(5,'India','IND'),(6,'Thailand','TH');

insert into public.industry (name, short_name) values ('Arts', 'Arts'),('Science', 'Sci'),('Marketing', 'Mkt'),('Computing', 'Comp'),('Math', 'Math'),('Environment', 'Env');

insert into public.course (name, details, industry_id, cert_id) values ('Creative Writing Workshop', 'Learn how to write', 1, 1), ('Nutrition and Wellness', 'Learn how to eat gooder', 2, 2),('Digital Marketing Strategies', 'Learn how to sell', 3, 3),('Data Science', 'Learn how to earth', 4, 4),('Advanced Calculus', 'Learn how to be a computer', 5, 5),('History of Art', 'Learn how to become a McDonalds employee.', 1, 6),('Environmental Science', 'Learn how to earth', 6, 7),('Environmental Science 2', 'Learn how to earth some MORE', 6, 8);

insert into public.assessment () values ();

INSERT INTO public.certificate(id, name, description, course_id, years_valid)VALUES 
(1, 'Creative Writer', 'This certifies the holder has completed the "Creative Writing Workshop".', 1, 2),
(2, 'Nutrition and Wellness Advocate', 'This person has learned how to eat gooder', 2, 2),
(3, 'Digital Marketing Strategist', 'This person is now great at selling this pen!', 3, 2),
(4, 'Data Science Initiate', 'This person has learned the basics of Data Science.', 4, 2),
(5, 'Certificate of Advanced Calculus (Basic)', 'Maybe they know something, hm...', 5, 2),
(6, 'Art Historian', 'They may not know how to paint, but they know about how people painted. Sounds paint-ful.', 6, 2),
(7, 'Environmental Scientist (Basic)', 'They know about rocks.', 7, 1),
(8, 'Environmental Scientist (Advanced)', 'They know about paper?', 8, 4;

insert into public.user_cert (id, issued_on, expires_on, user_id, cert_id) values 
(1, 2024-10-11, 2026-10-11, 1, );


