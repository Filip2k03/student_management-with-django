Steps to Deploy Django on Heroku Using GitHub:
1. Prepare your Django app for deployment:
Make sure your app is ready for deployment by checking:

requirements.txt: List all dependencies.

bash
Copy
pip freeze > requirements.txt
Procfile: This file tells Heroku how to run your app. Create a file called Procfile in your project’s root directory and add:

txt
Copy
web: gunicorn <your_project_name>.wsgi
Replace <your_project_name> with your actual Django project name.

runtime.txt: (Optional) Specify the Python version for Heroku (e.g., python-3.8.10).

Configure Static and Media files: Set up STATIC_ROOT and MEDIA_ROOT in your settings.py and make sure your static files are properly managed for production.

Database Configuration: You’ll likely use PostgreSQL in production, so update your DATABASES setting in settings.py accordingly.

2. Create a Heroku app:
Create a Heroku account if you don't have one already: Heroku Sign-Up

Install the Heroku CLI: Heroku CLI Installation

In your terminal, log in to Heroku:

bash
Copy
heroku login
Create a new Heroku app:

bash
Copy
heroku create <your-app-name>
This will create a new Heroku app and assign a URL (e.g., https://your-app-name.herokuapp.com).

3. Link your GitHub repository to Heroku:
Go to the Heroku Dashboard and open your app.

Under the Deploy tab, select GitHub as your deployment method.

Connect your GitHub account if it’s not already connected.

Select the repository you want to deploy from GitHub.

4. Set up environment variables (config vars) on Heroku:
On the Settings tab of your Heroku app, go to Config Vars and set environment variables like DEBUG, SECRET_KEY, DATABASE_URL, etc.

Example:

DEBUG=False

SECRET_KEY=<your-django-secret-key>

DATABASE_URL=your_database_url

5. Deploy your code:
You can deploy your app automatically by connecting GitHub to Heroku’s deployment method (under the Deploy tab).

Alternatively, you can deploy manually by running:

bash
Copy
git push heroku main
6. Migrate your database:
After your app is deployed, run the migrations on Heroku:

bash
Copy
heroku run python manage.py migrate
7. Collect Static Files:
Collect your static files for production:

bash
Copy
heroku run python manage.py collectstatic
8. Open your app:
Finally, open your app in the browser:

bash
Copy
heroku open
Your Django app should now be deployed and accessible via the Heroku URL.

Key Points:
GitHub is used as a code repository to store your Django app's code.

Heroku is a platform-as-a-service (PaaS) that automates the deployment process, and you can link your GitHub repository directly to it.

Procfile, requirements.txt, and other configurations (like PostgreSQL and static files) are important for production deployment.
