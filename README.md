see APP!    https://keayoauth-18d96476d084.herokuapp.com/

This Flask application integrates Google OAuth for user authentication and uses SQLAlchemy for database management. Here's a brief summary of the app:

Summary:
Flask Setup: The application is built using the Flask framework.
Database Integration: SQLAlchemy is used to manage the database, with a User model defined to store user information.
User Authentication: Flask-Login is used to handle user sessions and authentication.
Google OAuth: Authlib is used to integrate Google OAuth for user login. The application redirects users to Google's authorization URL, handles the callback, and exchanges the authorization code for an access token.
User Information: After successful authentication, the user's email is fetched from Google and stored in the session and database.
Routes:
/: The home page, accessible only to logged-in users, displays the user's email.
/login: Initiates the OAuth flow by redirecting the user to Google's authorization URL.
/authorize: Handles the OAuth callback, exchanges the authorization code for an access token, fetches user information, and logs in the user.
/logout: Logs out the user and clears the session.
