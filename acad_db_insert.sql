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
('test', 'test@example.com', 'test', 'test', '987 Redwood St, Paris, Singapore', 6, 1);

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
('Creative Writing Workshop', 100, '{
  "questions": [
    {
      "q": "Which of the following is NOT a key component of a short story?",
      "marks": 10,
      "options": [
        "Characters",
        "Setting",
        "Conflict",
        "Essay Structure"
      ],
      "answer": "Essay Structure"
    },
    {
      "q": "Which of the following is true about first-person and third-person narrative perspectives?",
      "marks": 15,
      "options": [
        "First-person perspective uses I or we, third-person uses he, she, or they",
        "Both are written using I or we",
        "First-person perspective is used in academic writing only",
        "There is no difference between them"
      ],
      "answer": "First-person perspective uses I or we, third-person uses he, she, or they"
    },
    {
      "q": "What does the theme of a story refer to?",
      "marks": 10,
      "options": [
        "The plot of the story",
        "The central idea or message explored in the story",
        "The setting of the story",
        "The characters names"
      ],
      "answer": "The central idea or message explored in the story"
    },
    {
      "q": "What is the role of conflict in storytelling?",
      "marks": 15,
      "options": [
        "To provide the storys conclusion",
        "To drive the plot and character development by introducing challenges",
        "To make the story longer",
        "To keep the reader bored"
      ],
      "answer": "To drive the plot and character development by introducing challenges"
    },
    {
      "q": "Which is true about showing and telling in writing?",
      "marks": 10,
      "options": [
        "Showing provides sensory details, while telling gives direct information",
        "Showing is always used in academic writing",
        "Telling uses descriptive language to let the reader experience events",
        "There is no difference between the two"
      ],
      "answer": "Showing provides sensory details, while telling gives direct information"
    },
    {
      "q": "What is character development?",
      "marks": 20,
      "options": [
        "The process by which a character evolves over the course of the story",
        "The physical description of a character",
        "The process of creating minor characters",
        "The creation of an imaginary world"
      ],
      "answer": "The process by which a character evolves over the course of the story"
    },
    {
      "q": "What is NOT one of the three main types of plots in storytelling?",
      "marks": 15,
      "options": [
        "Linear",
        "Non-linear",
        "Episodic",
        "Spiral"
      ],
      "answer": "Spiral"
    },
    {
      "q": "What does setting in fiction refer to?",
      "marks": 10,
      "options": [
        "The events that occur in the story",
        "The time, place, and context of the story",
        "The characters motivations",
        "The conflict between the characters"
      ],
      "answer": "The time, place, and context of the story"
    },
    {
      "q": "What is foreshadowing?",
      "marks": 15,
      "options": [
        "Describing events in detail",
        "Giving hints about future events in the story",
        "The conclusion of the story",
        "A method of revealing the characters backstories"
      ],
      "answer": "Giving hints about future events in the story"
    },
    {
      "q": "Which of the following is NOT a primary element of a poem?",
      "marks": 20,
      "options": [
        "Rhyme",
        "Meter",
        "Imagery",
        "Prose Structure"
      ],
      "answer": "Prose Structure"
    }
  ]
}
', 1),
('Nutrition and Wellness', 100, '{
  "questions": [
    {
      "q": "Which of the following are the three macronutrients found in food?",
      "marks": 15,
      "options": [
        "Carbohydrates, Proteins, Fats",
        "Vitamins, Minerals, Water",
        "Sugars, Salts, Fiber",
        "Antioxidants, Minerals, Water"
      ],
      "answer": "Carbohydrates, Proteins, Fats"
    },
    {
      "q": "What is the main role of fiber in the human diet?",
      "marks": 15,
      "options": [
        "To provide energy",
        "To aid in digestion and regulate blood sugar levels",
        "To build muscles",
        "To supply vitamins to the body"
      ],
      "answer": "To aid in digestion and regulate blood sugar levels"
    },
    {
      "q": "Why are vitamins important for the human body?",
      "marks": 15,
      "options": [
        "They provide energy to the body",
        "They help regulate metabolism, immune function, and cell growth",
        "They only aid in bone growth",
        "They help in the digestion of food"
      ],
      "answer": "They help regulate metabolism, immune function, and cell growth"
    },
    {
      "q": "What is the primary source of Omega-3 fatty acids?",
      "marks": 20,
      "options": [
        "Red meat",
        "Fish and flaxseeds",
        "Dairy products",
        "Processed sugars"
      ],
      "answer": "Fish and flaxseeds"
    },
    {
      "q": "Which of the following is a good source of protein?",
      "marks": 15,
      "options": [
        "Apples",
        "Chicken breast",
        "Carrots",
        "White rice"
      ],
      "answer": "Chicken breast"
    },
    {
      "q": "What vitamin is most associated with the absorption of calcium?",
      "marks": 15,
      "options": [
        "Vitamin A",
        "Vitamin B12",
        "Vitamin C",
        "Vitamin D"
      ],
      "answer": "Vitamin D"
    },
    {
      "q": "Which of the following is a function of water in the body?",
      "marks": 10,
      "options": [
        "Transports nutrients and regulates body temperature",
        "Provides calories",
        "Creates proteins in the body",
        "Helps store energy"
      ],
      "answer": "Transports nutrients and regulates body temperature"
    },
    {
      "q": "Which mineral is important for bone health?",
      "marks": 10,
      "options": [
        "Iron",
        "Calcium",
        "Magnesium",
        "Sodium"
      ],
      "answer": "Calcium"
    },
    {
      "q": "Which of the following is NOT a healthy fat?",
      "marks": 20,
      "options": [
        "Avocados",
        "Olive oil",
        "Butter",
        "Nuts"
      ],
      "answer": "Butter"
    },
    {
      "q": "What is the recommended daily intake of water for an average adult?",
      "marks": 10,
      "options": [
        "1-2 cups",
        "3-4 cups",
        "8 cups or about 2 liters",
        "12 cups"
      ],
      "answer": "8 cups or about 2 liters"
    }
  ]
}
', 2),
('Digital Marketing Strategies', 100, '{
  "questions": [
    {
      "q": "Which of the following is the primary goal of digital marketing?",
      "marks": 15,
      "options": [
        "To generate leads and sales online",
        "To increase the number of followers on social media",
        "To create awareness about a brand offline",
        "To promote traditional media campaigns"
      ],
      "answer": "To generate leads and sales online"
    },
    {
      "q": "What is SEO (Search Engine Optimization)?",
      "marks": 20,
      "options": [
        "The process of optimizing a website to rank higher on search engines",
        "The process of creating paid ads for search engines",
        "The process of improving email deliverability",
        "The process of designing websites"
      ],
      "answer": "The process of optimizing a website to rank higher on search engines"
    },
    {
      "q": "What does PPC (Pay-per-click) advertising refer to?",
      "marks": 15,
      "options": [
        "A form of advertising where advertisers pay each time their ad is clicked",
        "A form of SEO strategy",
        "A form of organic social media marketing",
        "A method of creating a websites structure"
      ],
      "answer": "A form of advertising where advertisers pay each time their ad is clicked"
    },
    {
      "q": "What is the primary purpose of content marketing?",
      "marks": 15,
      "options": [
        "To create and distribute valuable content to attract and engage a target audience",
        "To create paid advertisements for social media",
        "To create flashy designs for websites",
        "To measure website traffic"
      ],
      "answer": "To create and distribute valuable content to attract and engage a target audience"
    },
    {
      "q": "Which social media platform is best known for B2B marketing?",
      "marks": 20,
      "options": [
        "Facebook",
        "Instagram",
        "LinkedIn",
        "Twitter"
      ],
      "answer": "LinkedIn"
    },
    {
      "q": "What is an email marketing campaign?",
      "marks": 10,
      "options": [
        "Sending promotional emails to a list of recipients to promote a product or service",
        "Sending invoices to customers",
        "Sending welcome emails only to new customers",
        "Sending newsletters without targeting a specific audience"
      ],
      "answer": "Sending promotional emails to a list of recipients to promote a product or service"
    },
    {
      "q": "What is a call to action (CTA) in digital marketing?",
      "marks": 10,
      "options": [
        "A command that encourages users to take an action, such as Click here or Buy now",
        "A form of content marketing",
        "A type of SEO strategy",
        "A paid ad on social media"
      ],
      "answer": "A command that encourages users to take an action, such as Click here or Buy now"
    },
    {
      "q": "What is the role of analytics in digital marketing?",
      "marks": 15,
      "options": [
        "To track, measure, and analyze data from digital marketing campaigns to improve results",
        "To design websites",
        "To write content for blogs",
        "To create social media posts"
      ],
      "answer": "To track, measure, and analyze data from digital marketing campaigns to improve results"
    },
    {
      "q": "What is social media marketing?",
      "marks": 10,
      "options": [
        "Using social media platforms to promote products or services",
        "Designing social media profiles",
        "Creating content for email marketing",
        "Creating advertisements for television"
      ],
      "answer": "Using social media platforms to promote products or services"
    },
    {
      "q": "Which of the following is NOT a benefit of digital marketing?",
      "marks": 15,
      "options": [
        "It allows for targeting specific audiences with personalized content",
        "It provides real-time metrics and performance tracking",
        "It is always more expensive than traditional marketing",
        "It allows businesses to reach a global audience"
      ],
      "answer": "It is always more expensive than traditional marketing"
    }
  ]
}
', 3),
('Data Science', 100, '{
  "questions": [
    {
      "q": "Which of the following is the main goal of data science?",
      "marks": 15,
      "options": [
        "To analyze and interpret complex data to make informed decisions",
        "To create websites",
        "To design mobile applications",
        "To manage social media campaigns"
      ],
      "answer": "To analyze and interpret complex data to make informed decisions"
    },
    {
      "q": "Which of the following is a popular programming language used in data science?",
      "marks": 10,
      "options": [
        "Java",
        "Python",
        "C++",
        "HTML"
      ],
      "answer": "Python"
    },
    {
      "q": "What does the term big data refer to?",
      "marks": 20,
      "options": [
        "Large volumes of data that cannot be processed by traditional data management tools",
        "A new data visualization tool",
        "Data with no structure or organization",
        "Data stored in cloud servers"
      ],
      "answer": "Large volumes of data that cannot be processed by traditional data management tools"
    },
    {
      "q": "What is machine learning?",
      "marks": 20,
      "options": [
        "A type of artificial intelligence that allows systems to learn from data and improve over time",
        "A method for creating websites",
        "A programming language",
        "A form of data visualization"
      ],
      "answer": "A type of artificial intelligence that allows systems to learn from data and improve over time"
    },
    {
      "q": "Which of the following is an example of unstructured data?",
      "marks": 15,
      "options": [
        "Spreadsheets",
        "Audio recordings",
        "CSV files",
        "Database tables"
      ],
      "answer": "Audio recordings"
    },
    {
      "q": "What is the purpose of data preprocessing?",
      "marks": 15,
      "options": [
        "To clean and organize raw data before analysis",
        "To store data in a database",
        "To design the layout of a website",
        "To create charts and graphs"
      ],
      "answer": "To clean and organize raw data before analysis"
    },
    {
      "q": "Which of the following is used to visualize data patterns?",
      "marks": 10,
      "options": [
        "Data mining",
        "Data visualization tools like charts and graphs",
        "Data warehousing",
        "Programming languages like Python"
      ],
      "answer": "Data visualization tools like charts and graphs"
    },
    {
      "q": "What is the primary purpose of supervised learning in machine learning?",
      "marks": 15,
      "options": [
        "To train a model using labeled data to make predictions",
        "To analyze unstructured data",
        "To create neural networks",
        "To store large datasets"
      ],
      "answer": "To train a model using labeled data to make predictions"
    },
    {
      "q": "What does feature engineering refer to in data science?",
      "marks": 10,
      "options": [
        "The process of selecting, modifying, or creating features (input variables) for a model",
        "The process of writing code for data analysis",
        "The process of designing machine learning algorithms",
        "The process of visualizing data"
      ],
      "answer": "The process of selecting, modifying, or creating features (input variables) for a model"
    },
    {
      "q": "What is the purpose of a confusion matrix in machine learning?",
      "marks": 10,
      "options": [
        "To evaluate the performance of a classification model",
        "To store the raw data",
        "To design the structure of a neural network",
        "To generate random numbers"
      ],
      "answer": "To evaluate the performance of a classification model"
    }
  ]
}
', 4),
('Advanced Calculus', 100, '{
  "questions": [
    {
      "q": "What is the derivative of the function f(x) = x^2?",
      "marks": 15,
      "options": [
        "2x",
        "x",
        "x^2",
        "1"
      ],
      "answer": "2x"
    },
    {
      "q": "Which of the following is the correct integral of f(x) = 3x^2?",
      "marks": 20,
      "options": [
        "x^3 + C",
        "3x^3 + C",
        "x^3 + 3x + C",
        "3x^3"
      ],
      "answer": "x^3 + C"
    },
    {
      "q": "What is the limit of (sin(x)/x) as x approaches 0?",
      "marks": 15,
      "options": [
        "1",
        "0",
        "Infinity",
        "Does not exist"
      ],
      "answer": "1"
    },
    {
      "q": "What is the Taylor series expansion of e^x at x = 0?",
      "marks": 20,
      "options": [
        "1 + x + x^2/2! + x^3/3! + ...",
        "1 + x + x^2 + x^3 + ...",
        "1 + x^2 + x^4 + ...",
        "1 + x^3 + x^5 + ..."
      ],
      "answer": "1 + x + x^2/2! + x^3/3! + ..."
    },
    {
      "q": "What is the integral of cos(x) dx?",
      "marks": 10,
      "options": [
        "sin(x) + C",
        "cos(x) + C",
        "sin(x)",
        "cos(x)"
      ],
      "answer": "sin(x) + C"
    },
    {
      "q": "What does the Fundamental Theorem of Calculus state?",
      "marks": 20,
      "options": [
        "The integral of a functions derivative is the function itself",
        "The derivative of a function is its rate of change",
        "The integral of a function is the area under its curve",
        "The derivative of a function is its slope"
      ],
      "answer": "The integral of a functions derivative is the function itself"
    },
    {
      "q": "What is the second derivative of f(x) = x^3?",
      "marks": 10,
      "options": [
        "6x",
        "3x^2",
        "x^2",
        "3x"
      ],
      "answer": "6x"
    },
    {
      "q": "What is the partial derivative of f(x, y) = x^2 + y^2 with respect to x?",
      "marks": 15,
      "options": [
        "2x",
        "2y",
        "x^2",
        "y^2"
      ],
      "answer": "2x"
    },
    {
      "q": "What is the integral of 1/x dx?",
      "marks": 15,
      "options": [
        "ln(x) + C",
        "x + C",
        "1/x + C",
        "ln(x)"
      ],
      "answer": "ln(x) + C"
    },
    {
      "q": "What is the derivative of sin(x)?",
      "marks": 10,
      "options": [
        "cos(x)",
        "-cos(x)",
        "sin(x)",
        "-sin(x)"
      ],
      "answer": "cos(x)"
    }
  ]
}

       
', 5),
('History of Art', 100, '{
  "questions": [
    {
      "q": "Who painted the Mona Lisa?",
      "marks": 15,
      "options": [
        "Vincent van Gogh",
        "Pablo Picasso",
        "Leonardo da Vinci",
        "Claude Monet"
      ],
      "answer": "Leonardo da Vinci"
    },
    {
      "q": "Which art movement is Pablo Picasso associated with?",
      "marks": 20,
      "options": [
        "Impressionism",
        "Cubism",
        "Surrealism",
        "Baroque"
      ],
      "answer": "Cubism"
    },
    {
      "q": "What is the name of the famous painting by Edvard Munch?",
      "marks": 15,
      "options": [
        "The Persistence of Memory",
        "The Scream",
        "Starry Night",
        "Girl with a Pearl Earring"
      ],
      "answer": "The Scream"
    },
    {
      "q": "What was the main subject matter of Impressionist paintings?",
      "marks": 15,
      "options": [
        "Scenes of daily life and nature",
        "Abstract concepts",
        "Historical events",
        "Religious themes"
      ],
      "answer": "Scenes of daily life and nature"
    },
    {
      "q": "Who is known as the father of modern sculpture?",
      "marks": 20,
      "options": [
        "Auguste Rodin",
        "Michelangelo",
        "Pablo Picasso",
        "Alberto Giacometti"
      ],
      "answer": "Auguste Rodin"
    },
    {
      "q": "Which period is known for its ornate and decorative art style?",
      "marks": 10,
      "options": [
        "Renaissance",
        "Baroque",
        "Romanticism",
        "Art Nouveau"
      ],
      "answer": "Baroque"
    },
    {
      "q": "Which artist is associated with the Surrealist movement?",
      "marks": 15,
      "options": [
        "Salvador Dalí",
        "Vincent van Gogh",
        "Claude Monet",
        "Jackson Pollock"
      ],
      "answer": "Salvador Dalí"
    },
    {
      "q": "What art style did Jackson Pollock help popularize?",
      "marks": 20,
      "options": [
        "Pop Art",
        "Abstract Expressionism",
        "Cubism",
        "Renaissance"
      ],
      "answer": "Abstract Expressionism"
    },
    {
      "q": "What is the primary characteristic of Abstract art?",
      "marks": 10,
      "options": [
        "It focuses on realistic depictions of people and objects",
        "It uses geometric shapes and forms that do not resemble the real world",
        "It incorporates religious symbols",
        "It focuses on depicting historical events"
      ],
      "answer": "It uses geometric shapes and forms that do not resemble the real world"
    },
    {
      "q": "Who is considered the leader of the Renaissance period in Italy?",
      "marks": 10,
      "options": [
        "Leonardo da Vinci",
        "Michelangelo",
        "Raphael",
        "Giotto"
      ],
      "answer": "Leonardo da Vinci"
    }
  ]
}
', 6),
('Environmental Science', 100, '{
  "questions": [
    {
      "q": "What is the greenhouse effect?",
      "marks": 15,
      "options": [
        "The warming of the Earths surface due to the trapping of heat by gases in the atmosphere",
        "The cooling of the Earths surface due to the depletion of ozone",
        "The process of deforestation",
        "The production of renewable energy from solar panels"
      ],
      "answer": "The warming of the Earths surface due to the trapping of heat by gases in the atmosphere"
    },
    {
      "q": "Which of the following is a renewable source of energy?",
      "marks": 10,
      "options": [
        "Coal",
        "Natural gas",
        "Solar power",
        "Oil"
      ],
      "answer": "Solar power"
    },
    {
      "q": "What is the main cause of ocean acidification?",
      "marks": 15,
      "options": [
        "Increased levels of carbon dioxide in the atmosphere",
        "Decreased levels of oxygen in the ocean",
        "Water pollution from plastics",
        "Overfishing"
      ],
      "answer": "Increased levels of carbon dioxide in the atmosphere"
    },
    {
      "q": "Which of the following is a consequence of deforestation?",
      "marks": 20,
      "options": [
        "Loss of biodiversity",
        "Reduction in greenhouse gas emissions",
        "Increased rainfall",
        "Improved air quality"
      ],
      "answer": "Loss of biodiversity"
    },
    {
      "q": "What is the purpose of recycling?",
      "marks": 10,
      "options": [
        "To reduce waste and conserve natural resources",
        "To create more plastic",
        "To generate profit from waste materials",
        "To increase global warming"
      ],
      "answer": "To reduce waste and conserve natural resources"
    },
    {
      "q": "What is biodiversity?",
      "marks": 15,
      "options": [
        "The variety of life in a particular habitat",
        "The process of converting waste into usable energy",
        "The impact of climate change on ecosystems",
        "The study of weather patterns"
      ],
      "answer": "The variety of life in a particular habitat"
    },
    {
      "q": "What is the main contributor to global warming?",
      "marks": 20,
      "options": [
        "Carbon dioxide emissions from burning fossil fuels",
        "Natural volcanic eruptions",
        "Excessive rainfall",
        "Deforestation"
      ],
      "answer": "Carbon dioxide emissions from burning fossil fuels"
    },
    {
      "q": "What is the term for the study of ecosystems?",
      "marks": 10,
      "options": [
        "Ecology",
        "Economics",
        "Geology",
        "Biology"
      ],
      "answer": "Ecology"
    },
    {
      "q": "What is the ozone layer?",
      "marks": 15,
      "options": [
        "A layer of gas that protects Earth from harmful ultraviolet radiation",
        "A layer of water in the atmosphere",
        "A layer of oxygen in the ocean",
        "A layer of nitrogen in the atmosphere"
      ],
      "answer": "A layer of gas that protects Earth from harmful ultraviolet radiation"
    },
    {
      "q": "Which of the following is an example of nonrenewable resources?",
      "marks": 10,
      "options": [
        "Wind",
        "Sunlight",
        "Coal",
        "Water"
      ],
      "answer": "Coal"
    }
  ]
}
', 7),
('Environmental Science 2', 100, '{
  "questions": [
    {
      "q": "What is the main cause of the depletion of the ozone layer?",
      "marks": 15,
      "options": [
        "The use of chlorofluorocarbons (CFCs) in aerosol sprays and refrigerants",
        "Carbon dioxide emissions from vehicles",
        "The burning of fossil fuels",
        "Overfishing"
      ],
      "answer": "The use of chlorofluorocarbons (CFCs) in aerosol sprays and refrigerants"
    },
    {
      "q": "Which of the following is considered a non-renewable resource?",
      "marks": 20,
      "options": [
        "Solar energy",
        "Wind energy",
        "Natural gas",
        "Geothermal energy"
      ],
      "answer": "Natural gas"
    },
    {
      "q": "What is the primary purpose of the Paris Agreement on climate change?",
      "marks": 20,
      "options": [
        "To reduce global greenhouse gas emissions to limit global warming to below 2°C above pre-industrial levels",
        "To promote the use of fossil fuels",
        "To create regulations for nuclear energy",
        "To increase deforestation rates"
      ],
      "answer": "To reduce global greenhouse gas emissions to limit global warming to below 2°C above pre-industrial levels"
    },
    {
      "q": "What does the term sustainability refer to in environmental science?",
      "marks": 15,
      "options": [
        "Using resources in a way that meets present needs without compromising the ability of future generations to meet their own needs",
        "Maximizing resource extraction for economic growth",
        "Destroying natural habitats for urbanization",
        "The reduction of human population"
      ],
      "answer": "Using resources in a way that meets present needs without compromising the ability of future generations to meet their own needs"
    },
    {
      "q": "What is the greenhouse effect?",
      "marks": 15,
      "options": [
        "The trapping of heat in the Earths atmosphere due to increased levels of greenhouse gases",
        "The cooling of the Earths surface due to the depletion of the ozone layer",
        "The natural absorption of solar energy by the Earths surface",
        "The process of turning carbon dioxide into oxygen"
      ],
      "answer": "The trapping of heat in the Earths atmosphere due to increased levels of greenhouse gases"
    },
    {
      "q": "What is the most significant environmental threat caused by deforestation?",
      "marks": 20,
      "options": [
        "Loss of biodiversity and disruption of ecosystems",
        "Increased agricultural productivity",
        "Expansion of urban areas",
        "Reduction in global temperatures"
      ],
      "answer": "Loss of biodiversity and disruption of ecosystems"
    },
    {
      "q": "What is the term for the process by which trees and plants absorb carbon dioxide and release oxygen?",
      "marks": 10,
      "options": [
        "Photosynthesis",
        "Respiration",
        "Transpiration",
        "Evaporation"
      ],
      "answer": "Photosynthesis"
    },
    {
      "q": "Which of the following is a consequence of acid rain?",
      "marks": 15,
      "options": [
        "Soil degradation and damage to aquatic ecosystems",
        "Increase in biodiversity",
        "Reduction in air pollution",
        "Improved plant growth"
      ],
      "answer": "Soil degradation and damage to aquatic ecosystems"
    },
    {
      "q": "What is the concept of carbon footprint?",
      "marks": 10,
      "options": [
        "The total amount of carbon dioxide and other greenhouse gases emitted by human activities",
        "The amount of carbon dioxide absorbed by plants during photosynthesis",
        "The weight of carbon in fossil fuels",
        "The total amount of carbon stored in the oceans"
      ],
      "answer": "The total amount of carbon dioxide and other greenhouse gases emitted by human activities"
    },
    {
      "q": "Which of the following is a renewable energy source?",
      "marks": 10,
      "options": [
        "Coal",
        "Oil",
        "Solar power",
        "Natural gas"
      ],
      "answer": "Solar power"
    }
  ]
}
', 8);

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
