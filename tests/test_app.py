from app import db, User, Food

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'ZeroWaste' in response.data

def test_register_and_login(client):
    # Register
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'donor'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data or b'Login successful!' in response.data or b'Welcome Back' in response.data

    # Login
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login successful!' in response.data or b'Dashboard' in response.data

def test_add_food(client):
    # Register and login a donor
    client.post('/register', data={
        'name': 'Donor',
        'email': 'donor@example.com',
        'password': 'password',
        'confirm_password': 'password',
        'role': 'donor'
    }, follow_redirects=True)
    client.post('/login', data={'email': 'donor@example.com', 'password': 'password'}, follow_redirects=True)
    
    # Add food
    response = client.post('/add_food', data={
        'title': 'Test Food',
        'description': 'This is a test food item for testing.',
        'location': '123 Test St',
        'expiry_date': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test Food' in response.data
