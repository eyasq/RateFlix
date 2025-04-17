# 🎬 RateFlix

**RateFlix** is a Django-based web application that simulates a movie database and discussion forum. It allows users to browse movies, write reviews, and engage in discussions, providing a platform for movie enthusiasts to share their thoughts and opinions.

## 🚀 Features

- **User Authentication**: Secure registration and login system.
- **Movie Database**: Browse and search for movies with detailed information.
- **Reviews & Ratings**: Users can write reviews and rate movies.
- **Discussion Forums**: Engage in discussions about movies with other users.
- **Personalized Recommendations**: Receive movie suggestions based on user preferences.

## 🛠️ Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default), can be configured to use PostgreSQL or MySQL
- **Templates**: Django Templates
- **Version Control**: Git & GitHub

## 📂 Project Structure
C:.
│   .env
│   .gitignore
│   db.sqlite3
│   manage.py
│   README.md
│
├───RateFlix
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│   │
│   └───__pycache__
│
│
└───rateflix_app
    │   admin.py
    │   apps.py
    │   forms.py
    │   models.py
    │   tests.py
    │   tmdb_utils.py
    │   urls.py
    │   views.py
    │   __init__.py
    ├───migrations
    │   │   __init__.py
    │   │
    │   └───__pycache__
    │
    ├───static
    │   ├───assets
    │   ├───css
    │   │       starability.css
    │   │       style.css
    │   │
    │   └───js
    │           comments.js
    │           favorites.js
    │           genre.js
    │           loadMore.js
    │           reviews.js
    │
    ├───templates
    │       about.html
    │       actorsmovies.html
    │       base.html
    │       contact.html
    │       login.html
    │       movies.html
    │       movie_page.html
    │       other_profile.html
    │       profile.html
    │       register.html
    │       search_results.html
    │       slider.html
    │       test.html
    │
    └───__pycache__

# 🔧 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/eyasq/RateFlix.git
   cd RateFlix
   
2. **Create Virtual Environment**:
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

3. **Install Dependencies**:
    pip install -r requirements.txt

4. **Apply Migrations**:
    python manage.py migrate

5. **Run The Development Server**
    python manage.py runserver

6. **Run The Development Server**
    Access the application: Open your browser and navigate to http://127.0.0.1:8000/

🧪 Running Tests
    To run the test suite:
    python manage.py test

🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

📫 Contact
For any inquiries or feedback, please contact rateflixproject@gmail.com