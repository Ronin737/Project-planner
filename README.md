Django framework has been used for the project.
The out-of-the-box sqlite3 database has been used for the data.

The project has 2 apps running- Users and Projects.

Users contain the data about users and teams.
Projects contain the data about projectboards and individual tasks.

The datatable relations are defined as such:-
User-Team(Many to One)
Projectboard-Team(One to One)
Task-Projectboard(Many to One)
Task-Team(One to One)

For building out the API endpoints, rest-framework's generic views have been used.
The views are designed to inherit from the generic views as well as the abstract classes, and then have their functions extended and overridden for performing various operations like creating, adding and listing.

All the available endpoints are specified in the urls file of both apps. It can also be viewed by the show_urls command in django terminal.

All required dependencies are specified in requirements file.
