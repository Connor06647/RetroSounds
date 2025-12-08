# RetroSounds 🎵

A vintage-inspired vinyl record shop web application built with Flask and Tailwind CSS.

## Features

- **Home Page**: Browse featured vinyl records with beautiful card layouts
- **Products Page**: Explore the full catalog of classic albums
- **Login System**: User authentication with SQLite database backend
- **Theme Customization**: Multiple visual themes including:
  - Minimalist Dark
  - Vintage Warm
  - Modern Professional
  - Neon Retro
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS
- **Settings Sidebar**: Easy theme switching on the fly

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Tailwind CSS
- **Fonts**: Google Fonts (Inter)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Connor06647/RetroSounds.git
cd RetroSounds
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
- Windows: `.venv\Scripts\activate`
- Mac/Linux: `source .venv/bin/activate`

4. Install dependencies:
```bash
pip install flask
```

## Running the Application

1. Start the Flask server:
```bash
python Contact.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Project Structure

- `Contact.py` - Flask backend server
- `index.html` - Home page
- `products.html` - Products catalog page
- `Contact.html` - Login page
- `theme-browser.html` - Theme customization page
- `Contact.css` - Custom styles
- `view_database.py` - Database viewer utility
- `users.db` - SQLite database (created on first run)

## Pages

- **/** - Home page with featured albums
- **/products** - Full product catalog
- **/login** - User login page
- **/themes** - Theme browser and customization

## Development

This project uses Flask's development server. For production deployment, use a production WSGI server like Gunicorn or uWSGI.

## License

This project is open source and available for educational purposes.

## Author

Connor06647
