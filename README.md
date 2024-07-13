# JobTrackr - Job Listing and Application Management System
JobTrackr is a comprehensive web application designed to streamline the job listing and application process. It offers functionalities for companies to post job listings and for applicants to search and apply for jobs. The platform includes features for profile management, application tracking, and status updates, all integrated with a responsive design using Tailwind CSS.

Table of Contents
Features
Installation
Usage
Models
Views
Templates
Forms
Static Files
CSS and JavaScript
Routing
License
Features
User Authentication: Secure login and registration for both companies and applicants.
Profile Management: Companies and applicants can manage their profiles, including personal and professional information.
Job Listings: Companies can create, edit, and delete job listings with detailed descriptions and requirements.
Job Applications: Applicants can apply to jobs and track the status of their applications.
Application Status: Companies can update the status of job applications (e.g., pending, reviewed, accepted, rejected).
Responsive Design: Implemented using Tailwind CSS for a modern and responsive user interface.
Error Handling: Comprehensive error handling and messaging system to guide users.
Dynamic Content: Use of Django's template system to dynamically render content based on user roles and actions.
Installation
Clone the Repository

bash
Copy code
git clone https://github.com/yourusername/jobtrackr.git
cd jobtrackr
Set up the Virtual Environment

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Run Migrations

bash
Copy code
python manage.py migrate
Create Superuser

bash
Copy code
python manage.py createsuperuser
Run the Server

bash
Copy code
python manage.py runserver
Usage
Register: New users can register as either a company or an applicant.
Login: Users can log in with their credentials.
Profile Management: After logging in, users can manage their profile information.
Job Listings: Companies can create job listings, which will be visible to all applicants.
Job Applications: Applicants can search for jobs and apply by submitting a cover letter. Their resume must be uploaded in their profile.
Application Management: Companies can view the list of applicants for each job and update the application status.
Models
User: Custom user model extending Django's AbstractUser.
Company: Model for storing company-specific information.
Applicant: Model for storing applicant-specific information.
Job: Model for job listings.
Application: Model for job applications, including status tracking.
Views
User Views:

register_user: Handles user registration.
login_user: Handles user login.
logout_user: Handles user logout.
profile: Displays the profile page for the logged-in user.
edit_profile: Allows users to edit their profile.
Company Views:

company_profile: Displays the company profile along with job listings.
edit_company_profile: Allows companies to edit their profile information.
delete_job: Allows companies to delete a job listing.
view_applications: Allows companies to view and manage applications for their job listings.
Job Views:

create_job: Allows companies to create job listings.
edit_job: Allows companies to edit job listings.
job_details: Displays the details of a job listing.
apply_to_job: Allows applicants to apply to job listings.
Templates
Base Templates: Common structure for all pages.
User Templates: Specific templates for user-related views.
Company Templates: Specific templates for company-related views.
Job Templates: Specific templates for job-related views.
Forms
User Forms:

UserRegistrationForm
UserLoginForm
UserProfileForm
Company Forms:

CompanyRegistrationForm
CompanyProfileForm
JobForm
Applicant Forms:

ApplicantRegistrationForm
ApplicantProfileForm
JobApplicationForm
Static Files
CSS: Tailwind CSS for responsive design.
JavaScript: Custom scripts for enhanced interactivity.
Images: Placeholder and company logos.
CSS and JavaScript
Tailwind CSS: Integrated for styling.
Custom JS: For handling dynamic interactions like form submissions, AJAX requests, and more.
Routing
URL Configuration: All URLs are configured in urls.py within respective apps and included in the project-level urls.py.
