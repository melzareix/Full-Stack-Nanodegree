### Configuring Linux Webservers
This project is a part of Udacity's nanodegree program.

Deploying a Flask app to Amazon AWS on an Ubuntu 14.04 server,
   configuring the server and securing it.
   
### How to Use

- The project can be accessed from : http://ec2-50-112-217-103.us-west-2.compute.amazonaws.com/

- To access through ssh, the RSA file contents is provided in the instruction notes.

    `ssh grader@50.112.217.103 -i ~/.ssh/grader -p 2200`

- **Configurations**
    - Pass-phrase : `grader`.
    - DB Username : catalog_user - With full privileges -
    another user with restricted privileges named `catalog`.
   
    - DB Password : `FMLJsXCjuq7QZveCxx4Y`.
    
    - DB Name :   `itemcatalogue`.
    
- **Configuration changed**
    - Created new user `grader` with `sudo privileges`.
    - Changed Timezone to `UTC`.
    - Installed and updated the required software.
    - Changed SSH port to `2200`.
    - Configured UFW to allow connections only on SSH (port 2200),      HTTP (port 80), and NTP (port 123).
    - Secured PostgreSQL.
    - Deployed The ItemCatalogue developed in the previous course.
    - Although not applicaple to current git structure, Prevented
    access to `.git` through a custom `.htaccess` rules.
    
- **Software Installed**
    - Ubuntu 14.04 Trusty
    - Apache2
    - mod_wsgi
    - python
    - pip
    - Flask
    - PostgreSQL
    - Flask-SQLAlchemy
    - SQLAlchemy
    - Jinja2
    - oauth2client
    - httplib2
    - psycopg2