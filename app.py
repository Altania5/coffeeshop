from flask import Flask, render_template, jsonify, g  # Import 'g'
import sqlite3

app = Flask(__name__)
DATABASE = 'coffeeshop.db'

def get_db():
    """Opens a new database connection for each request."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def close_db(exception=None):
    """Closes the database connection after the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_app():
    app = Flask(__name__)
    # ... other app configurations ...

    with app.app_context():
        db = get_db()
        with db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS drinks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL
                )
            ''')

    return app

app = create_app()

@app.teardown_appcontext
def teardown_db(exception=None):
    """Ensures the database connection is closed when the app shuts down."""
    close_db()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM drinks")
    menu = cursor.fetchall()
    close_db()
    return render_template('index.html', menu=menu)

@app.route('/menu')
def get_menu():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM drinks")
    menu = cursor.fetchall()
    close_db()
    return jsonify(menu)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
