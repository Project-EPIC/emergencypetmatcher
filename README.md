# emergencypetmatcher

EPM is a Python web application built in Django for reuniting lost and found pets as a collaborative effort during mass emergency events. EPM is designed to help spread lost/found pet postings, as users can easily sign up using Facebook/Twitter and share them easily. With the power of the crowd, people can log in, report lost/found pets, propose matches using a simple matching interface, and vote up/down on those matches to increase likelihood of successful matches. When enough votes have been cast on a pet match, emails are sent out to original lost/found pet contacts encouraging them to speak with each other to determine whether the match is successful.  

##Requirements
1. Python 2.7
2. VirtualEnv

##Setup

1. First, clone this repo locally.
2. Run `virtualenv .` in the `project` folder.
3. Run `pip install -r requirements.txt` and ensure that all modules are properly installed.
4. Run `python manage.py migrate` to run migrations for the database.
5. To create test pet data, just run `python fixture.py setup` to see pet reports, matches, and user profiles generated at random.
6. In order to properly run EPM, you must fill out email account settings and social auth settings in order for your EPM instance to properly send emails and to authenticate Facebook/Twitter accounts, respectively. Fill out the `social_auth_settings.py` and `email_settings.py` under `project/project`.
7. Finally, run `python manage.py runserver` to start the development server and go to `localhost:8000` to see the front page of EPM.

