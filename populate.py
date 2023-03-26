import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_check_project.settings')

import django
django.setup()
from campus.models import University, Course, Location, Degree, User, Enrollment

def populate():

        scotland_universities = [
             
    {
    'name': 'University of Oxford',
    'location': {
        'name': 'Oxford',
        'latitude': 51.7542,
        'longitude': -1.2541,
        'university_slug': 'university-of-oxford'
    },
    'degree': {
        'name': 'Computer Science and Mathematics',
        'description': 'This degree focuses on computer programming, algorithms, data structures, and mathematical concepts.'
    },
    'courses': [
        {
            'name': 'Programming and Computation',
            'course_code': 'COMP101',
            'description': 'This course introduces students to the fundamental concepts of computer programming and computational thinking.'
        },
        {
            'name': 'Algorithms and Data Structures II',
            'course_code': 'COMP102',
            'description': 'This course covers the design and analysis of algorithms, data structures and advanced programming concepts.'
        }
    ],
    'logo': 'university_logos/OxfordUniversity.png',
    'description': 'The University of Oxford is a collegiate research university located in Oxford, England. It was founded in the 12th century and is the oldest university in the English-speaking world.',
    'website': 'https://www.ox.ac.uk/',
    'contact_email': 'enquiries@ox.ac.uk'
},
    {
        'name': 'University of Glasgow',
        'location': {
            
            'name': 'Glasgow',
            'latitude': 55.8721,
            'longitude': -4.2882,
            'university_slug': 'university-of-glasgow'
        },
        'degree': {
            'name': 'Computer Science IT+',
            'description': 'This degree focuses on computer programming, algorithms, data structures, and computer systems.'
        },
        'courses': [
            {
                'name': 'Programming in IT',
                'course_code': 'COMP08012',
                'description': 'This course introduces students to the fundamental concepts of computer programming.'
            },
            {
                'name': 'Algorithms and Data Structures I',
                'course_code': 'COMP08020',
                'description': 'This course covers the design and analysis of algorithms and the implementation of data structures.'
            }
        ],
        'logo': 'university_logos/GlasgowUniversity.png',
        'description': 'The University of Glasgow is a public research university located in Glasgow, Scotland. It was founded in 1451 and is the fourth-oldest university in the English-speaking world.',
        'website': 'https://www.gla.ac.uk/',
        'contact_email': 'enquiries@gla.ac.uk'
 },
    {
            'name': 'University of Edinburgh',
            'location': {
                'name': 'Edinburgh',
                'latitude': 55.9533,
                'longitude': -3.1883,
                'university_slug': 'university-of-edinburgh'
            },
            'degree': {
                'name': 'Business Administration',
                'description': 'This degree program focuses on management, marketing, finance, and accounting.'
            },
            'courses': [
                {
                    'name': 'Marketing Principles',
                    'course_code': 'BUSN08011',
                    'description': 'This course introduces students to the fundamental concepts and principles of marketing.'
                },
                {
                    'name': 'Financial Accounting',
                    'course_code': 'BUSN08022',
                    'description': 'This course covers the principles and practices of financial accounting.'
                }
            ],
            'logo': 'university_logos/EdinburghUniversity.png',
            'description': 'The University of Edinburgh is a public research university located in Edinburgh, Scotland. It was founded in 1582 and is the sixth-oldest university in the English-speaking world.',
            'website': 'https://www.ed.ac.uk/',
            'contact_email': 'info@ed.ac.uk'
        },
        {
'name': 'University of Cambridge',
'location': {
'name': 'Cambridge',
'latitude': 52.2053,
'longitude': 0.1218,
'university_slug': 'university-of-cambridge'
},
'degree': {
'name': 'Computer Technology',
'description': 'This degree program focuses on the principles and practices of computer science, including software development, algorithms, data structures, and programming languages.'
},
'courses': [
{
'name': 'AI Systems',
'course_code': 'COMPSCI 50',
'description': 'This course covers the fundamental concepts and techniques of artificial intelligence, including search algorithms, probabilistic reasoning, and machine learning.'
},
{
'name': 'Databases Systems',
'course_code': 'COMPSCI 61',
'description': 'This course covers the design, implementation, and optimization of database systems, including data modeling, query processing, and transaction management.'
}
],
'logo': 'university_logos/CambridgeUniversity.png',
'description': 'The University of Cambridge is a public research university located in Cambridge, England. It was founded in 1209 and is one of the oldest universities in the world.',
'website': 'https://www.cam.ac.uk/',
'contact_email': 'info@admin.cam.ac.uk'
},

{
    'name': 'University of Manchester',
    'location': {
        'name': 'Manchester',
        'latitude': 53.4668,
        'longitude': -2.2339,
        'university_slug': 'university-of-manchester'
    },
    'degree': {
        'name': 'Computer Fundamentals',
        'description': 'This degree program focuses on the study of computer systems, algorithms, programming languages, software engineering, and related topics.'
    },
    'courses': [
        {
            'name': 'Programming Fundamentals I',
            'course_code': 'COMP10120',
            'description': 'This course introduces students to the fundamentals of programming using Python.'
        },
        {
            'name': 'Databases in IT',
            'course_code': 'COMP60332',
            'description': 'This course covers the principles and practices of database systems, including data modeling, query processing, and transaction management.'
        }
    ],
    'logo': 'university_logos/ManchesterUniversity.png',
    'description': 'The University of Manchester is a public research university located in Manchester, England. It was formed in 2004 by the merger of the Victoria University of Manchester and the University of Manchester Institute of Science and Technology (UMIST).',
    'website': 'https://www.manchester.ac.uk/',
    'contact_email': 'enquiries@manchester.ac.uk'
}, 
{
    'name': 'University of Liverpool',
    'location': {
        'name': 'Liverpool',
        'latitude': 53.4084,
        'longitude': -2.9916,
        'university_slug': 'university-of-liverpool'
    },
    'degree': {
        'name': 'Data Science Master',
        'description': 'This degree program focuses on computer programming, software development, and computer systems.'
    },
    'courses': [
        {
            'name': 'Object-Oriented Programming',
            'course_code': 'COMP101',
            'description': 'This course teaches students the principles of object-oriented programming and design patterns.'
        },
        {
            'name': 'Algorithms and Structures',
            'course_code': 'COMP201',
            'description': 'This course covers the principles and implementation of algorithms and data structures.'
        },
        {
            'name': 'IT Systems',
            'course_code': 'COMP301',
            'description': 'This course introduces students to database design and implementation using SQL.'
        }
    ],
    'logo': 'university_logos/LiverpoolUniversity.png',
    'description': 'The University of Liverpool is a public research university located in Liverpool, England. It was founded in 1881 and is a member of the Russell Group of research-led British universities.',
    'website': 'https://www.liverpool.ac.uk/',
    'contact_email': 'enquiries@liverpool.ac.uk'
},
{
    'name': 'University of Newcastle',
    'location': {
        'name': 'Newcastle upon Tyne',
        'latitude': 54.9783,
        'longitude': -1.6178,
        'university_slug': 'university-of-newcastle'
    },
    'degree': {
        'name': 'Data Science',
        'description': 'This degree program focuses on computer programming, algorithms, data structures, and software engineering.'
    },
    'courses': [
        {
            'name': 'Artificial Intelligence',
            'course_code': 'COMP3001',
            'description': 'This course covers the principles and practices of artificial intelligence, including machine learning, computer vision, and natural language processing.'
        },
        {
            'name': 'Web Development',
            'course_code': 'COMP3015',
            'description': 'This course introduces students to the fundamental concepts and technologies used in web development, including HTML, CSS, JavaScript, and web frameworks.'
        }
    ],
    'logo': 'university_logos/NewcastleUniversity.png',
    'description': 'The University of Newcastle is a public research university located in Newcastle upon Tyne, England. It was founded in 1834 and is a member of the Russell Group of leading British research universities.',
    'website': 'https://www.ncl.ac.uk/',
    'contact_email': 'enquiries@ncl.ac.uk'
},
{
    'name': 'University of York',
    'location': {
        'name': 'York',
        'latitude': 53.9450,
        'longitude': -1.0561,
        'university_slug': 'university-of-york'
    },
    'degree': {
        'name': 'Master of Computer Science',
        'description': 'This degree program focuses on the design, development, and analysis of software and computer systems.'
    },
    'courses': [
        {
            'name': 'Data Structures and Algorithms I',
            'course_code': 'COMP1101',
            'description': 'This course covers the fundamentals of data structures and algorithms, including sorting and searching techniques.'
        },
        {
            'name': 'Security and Databases',
            'course_code': 'COMP1201',
            'description': 'This course introduces the principles of database design and management, including SQL and relational algebra.'
        },
        {
            'name': 'IT Networks',
            'course_code': 'COMP1301',
            'description': 'This course covers the basics of computer networks, including network architecture, protocols, and security.'
        }
    ],
    'logo': 'university_logos/YorkUniversity.png',
    'description': 'The University of York is a public research university located in the historic city of York, England. It was founded in 1963 and is known for its research in sciences, social sciences, and humanities.',
    'website': 'https://www.york.ac.uk/',
    'contact_email': 'enquiries@york.ac.uk'
},
{
    'name': 'Lancaster University',
    'location': {
        'name': 'Lancaster',
        'latitude': 54.007,
        'longitude': -2.784,
        'university_slug': 'lancaster-university'
    },
    'degree': {
        'name': 'Computer Science Undergraduate',
        'description': 'This degree program focuses on software development, algorithms, and computer systems.'
    },
    'courses': [
        {
            'name': 'Security Fundamentals',
            'course_code': 'COMP101',
            'description': 'This course teaches basic programming concepts and skills using a high-level programming language.'
        },
        {
            'name': 'Computer Networks',
            'course_code': 'COMP204',
            'description': 'This course covers the principles of computer networks, including network architecture, protocols, and security.'
        }
    ],
    'logo': 'university_logos/LancasterUniversity.png',
    'description': 'Lancaster University is a public research university located in Lancaster, England. It was founded in 1964 and has consistently ranked as one of the top universities in the UK.',
    'website': 'https://www.lancaster.ac.uk/',
    'contact_email': 'admissions@lancaster.ac.uk'
},
{
'name': 'University of Bristol',
'location': {
'name': 'Bristol',
'latitude': 51.4545,
'longitude': -2.5879,
'university_slug': 'university-of-bristol'
},
'degree': {
'name': 'Computer Science Master',
'description': 'This degree program focuses on computer programming, software engineering, and computer systems.'
},
'courses': [
{
'name': 'IT Algorithms and Data Structures',
'course_code': 'COMS10002',
'description': 'This course covers the fundamental algorithms and data structures used in computer science.'
},
{
'name': 'Big Data',
'course_code': 'COMS10004',
'description': 'This course covers the principles and practices of database systems, including data modeling, query languages, and database design.'
}
],
'logo': 'university_logos/BristolUniversity.png',
'description': 'The University of Bristol is a public research university located in Bristol, England. It was founded in 1876 and is one of the red brick universities.',
'website': 'https://www.bristol.ac.uk/',
'contact_email': 'enquiries@bristol.ac.uk'
}

]

        for uni_data in scotland_universities:
                location_data = uni_data['location']
                location = add_location(
                location_data['name'],
                location_data['latitude'],
                location_data['longitude'],
                location_data['university_slug'],
                )
                degree_data = uni_data['degree']
                degree = add_degree(
                degree_data['name'],
                degree_data['description']
                )
                uni = add_university(
                uni_data['name'],
                uni_data['logo'],
                uni_data['description'],
                uni_data['website'],
                uni_data['contact_email'],
                location
                )
                add_uni_location_degree(uni, location, degree)
                for course_data in uni_data['courses']:
                     add_course(
                        uni,
                        course_data['name'],
                        course_data['course_code'],
                        course_data['description']
                )


def add_university(name, logo, description, website, contact_email, location):
    u = University.objects.get_or_create(
        name=name,
        logo=logo,
        description=description,
        website=website,
        contact_email=contact_email,
        location=location
    )[0]
    u.save()
    return u


def add_location(name, latitude, longitude, university_slug):
    l = Location.objects.get_or_create(
        name=name,
        latitude=latitude,
        longitude=longitude,
        university_slug = university_slug
        )[0]
    l.save()
    return l

def add_degree(name, description):
    d = Degree.objects.get_or_create(
        name=name,
        description=description
        )[0]
    d.save()
    return d

def add_course(university, name, course_code, description):
    c = Course.objects.get_or_create(
        university=university,
        name=name,
        course_code=course_code,
        description=description
        )[0]
    c.save()
    return c

def add_uni_location_degree(university, location, degree):
    university.location = location
    university.degree.set([degree])
    university.save()



if __name__ == '__main__':
    print('Starting population script...')
    populate()