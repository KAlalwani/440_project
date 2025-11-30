rules = {
    
    # Registration
    r"(how (do|can)? i register|how to register|registration process|steps to register|where .*register)": 
        "You can register through the SIS website.",
    
    r"(when (is|does|will).*registration|registration date|when can i register|registration open|registration period)": 
        "Registration opens on January 5.",

    # Course Credits
    r"(credit|credits|how many credit|credit hours|course hours|ects)": 
        "Each course is worth 3 credit hours.",

    # Add/Drop
    r"(deadline|add.?drop|course change deadline|last day to add|last day to drop)": 
        "The add/drop deadline is January 18.",

    # Advisor
    r"(advisor|academic advisor|meet advisor|advising appointment|advisor meeting)": 
        "You must meet your academic advisor each semester.",

    # Graduation
    r"(graduation|graduate|requirements to graduate|how many credits to graduate|grad application)": 
        "Graduation requires at least 120 credit hours.",

    # Class Schedule
    r"(schedule|class time|where is my schedule|view schedule|timetable)": 
        "You can view your schedule on the SIS website.",

    # Library
    r"(library|books| borrow|library hours|print|printing|study room)": 
        "Library hours are 8AM–10PM every day.",

    # Fees/Payment
    r"(fees|payment|tuition|installments|invoice|balance|financial hold)": 
        "Tuition fees must be paid before Week 2.",

    # Exams
    r"(exam|midterm|final|quiz|exam schedule|test time|assessment)": 
        "Final exams are fixed on SIS; midterms are scheduled by instructors.",

    # Scholarships
    r"(scholarship|financial aid|funding|discount)": 
        "Scholarships require a GPA above 90.",

    # Wi-Fi
    r"(wifi|internet|network password|wifi password|connect wifi)": 
        "Campus Wi-Fi password is your student ID.",

    # Map / Directions
    r"(campus map|map|location|where is.*building|directions)": 
        "You can find the campus map at the main reception.",

    # Parking
    r"(parking|car|vehicle|park|parking pass)": 
        "Student parking spaces are available on campus.",

    # Cafeteria
    r"(cafeteria|food|canteen|lunch|restaurant|menu)": 
        "The cafeteria is open from 9AM–8PM.",

    # Housing
    r"(housing|dorm|accommodation|live on campus|hostel|residence)": 
        "University housing applications open in August.",

    # Student ID
    r"(id card|student card|lost id|replace id|id replacement)": 
        "A replacement student ID costs 10 BHD.",

    # Transcript
    r"(transcript|grades|get transcript|official transcript|record)": 
        "You can request transcripts from the registrar or via SIS.",

    # Portal
    r"(portal|login|student portal|access portal|cant login)": 
        "Use your student ID and password to log into the portal.",

    # Password reset
    r"(password reset|forgot password|reset account|lost password)": 
        "You can reset your password via the IT Helpdesk portal.",

    # Orientation
    r"(orientation|new student|freshman week|student welcome|intro week)": 
        "Orientation week begins September 1.",

    # Office hours
    r"(office hours|faculty hours|teacher hours|professor availability|meet professor)": 
        "Office hours vary by instructor and are posted online.",

    # Class format
    r"(online class|in person|hybrid|class type)": 
        "Most classes are in-person, but some programs offer hybrid formats.",

    # Email access
    r"(email|university email|outlook|student email)": 
        "You can access your student email using Office 365 login credentials.",

    # Printing
    r"(print|printing|scanner|scan|copy)": 
        "Printers and scanners are available in the library.",

    # Attendance
    r"(attendance|absence|miss class)": 
        "Attendance is required; more than 25% absence may result in failure.",

    # Prerequisites
    r"(prerequisite|requirements for course|take this course|course needed)": 
        "Course prerequisites are listed in the course catalog.",

    # Student clubs
    r"(club|clubs|activities|join club|student life)": 
        "You can join student clubs through the Student Affairs office.",

    # Events
    r"(event|events|workshop|seminar|activity calendar)": 
        "Upcoming events are posted on the university website.",

    # Lost & Found
    r"(lost|found|lost item|forgot)": 
        "Lost items can be claimed at the security office.",

    # Medical help
    r"(clinic|medical|health|doctor|nurse|first aid)": 
        "The campus medical clinic is open 9AM–4PM.",

    # Transport
    r"(bus|transport|shuttle|transportation)": 
        "University shuttle service runs between campus and student housing.",

    # Certificates
    r"(certificate|enrollment letter|student verification)": 
        "You can request official letters from the registrar office.",

    # Blackboard / LMS
    r"(blackboard|lms|moodle|canvas|course materials)":
        "You can access course materials through the LMS platform online.",

    # Internship
    r"(internship|training|coop|work placement)": 
        "Internship requirements depend on your major. Contact Career Services.",

    # GPA
    r"(gpa|calculate gpa|grade point average)": 
        "Your GPA is visible in SIS under the academic record section.",

    # Holidays
    r"(holiday|break|vacation|mid break|semester break)": 
        "Academic holidays follow the official university calendar.",

    # Course withdrawal
    r"(withdraw|withdrawal|drop semester|leave university)": 
        "Course withdrawal requires approval and may affect fees/grades.",

    # Complaints
    r"(complaint|report|issue|feedback)": 
        "You can submit complaints or feedback to Student Affairs.",

    # IT support
    r"(it support|technical help|computer help|tech support)": 
        "For technical support, contact IT Helpdesk or email support@university.com."
}
