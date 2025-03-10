from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from authentication import User
from database import init_db, add_user, get_user_by_username
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State  # Ensure these are imported
import dash_bootstrap_components as dbc

# Initialize Flask app
server = Flask(__name__)
server.secret_key = 'supersecretkey'

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'

# Initialize database
init_db()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Flask routes for login, signup, and logout
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user['password'] == password:
            user_obj = User(id=user['id'], username=user['username'], password=user['password'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password", 401
    return render_template('login.html')

@server.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_user(username, password)
        return redirect(url_for('login'))
    return render_template('signup.html')

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@server.route('/dashboard')
@login_required
def dashboard():
    return "Welcome to the dashboard!"

# Initialize Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),  # Ensure Output is imported
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/dashboard':
        return html.Div([
            html.H1("Dashboard"),
            dbc.Button("Logout", id="logout-button", color="danger", className="mr-1"),
            dcc.Link('Go to Trading Analysis', href='/trading-analysis'),
            dcc.Link('Go to Parameter Optimization', href='/parameter-optimization')
        ])
    elif pathname == '/trading-analysis':
        return trading_analysis_layout
    elif pathname == '/parameter-optimization':
        return optimization_layout
    else:
        return html.Div([
            html.H1("Welcome to the Stock Analysis App"),
            dcc.Link('Login', href='/login'),
            html.Br(),
            dcc.Link('Signup', href='/signup')
        ])

if __name__ == '__main__':
    server.run(debug=True)
