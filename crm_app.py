from flask import Flask, request, jsonify, render_template
import sqlite3

# Initialize Flask application
app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        phone TEXT,
                        company TEXT,
                        company_size TEXT,
                        budget TEXT,
                        industry TEXT,
                        compliance_needs TEXT,
                        status TEXT,
                        initial_outreach_date TEXT,
                        last_contact_date TEXT,
                        sale_closing_date TEXT
                    )''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Add new client
@app.route('/api/clients', methods=['POST'])
def add_client():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    company = data.get('company')
    company_size = data.get('company_size')
    budget = data.get('budget')
    industry = data.get('industry')
    compliance_needs = data.get('compliance_needs')
    status = data.get('status', 'Prospective')
    initial_outreach_date = data.get('initial_outreach_date')
    last_contact_date = data.get('last_contact_date')
    sale_closing_date = data.get('sale_closing_date')

    try:
        conn = sqlite3.connect('crm.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO clients (name, email, phone, company, company_size, budget, industry, compliance_needs, status, initial_outreach_date, last_contact_date, sale_closing_date) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (name, email, phone, company, company_size, budget, industry, compliance_needs, status, initial_outreach_date, last_contact_date, sale_closing_date))
        conn.commit()
        client_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'Client added successfully', 'client_id': client_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409

# Get all clients
@app.route('/api/clients', methods=['GET'])
def get_clients():
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = [dict(id=row[0], name=row[1], email=row[2], phone=row[3], company=row[4], company_size=row[5], budget=row[6], industry=row[7], compliance_needs=row[8], status=row[9], initial_outreach_date=row[10], last_contact_date=row[11], sale_closing_date=row[12])
               for row in cursor.fetchall()]
    conn.close()
    return jsonify(clients)

# Update client information
@app.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    company = data.get('company')
    company_size = data.get('company_size')
    budget = data.get('budget')
    industry = data.get('industry')
    compliance_needs = data.get('compliance_needs')
    status = data.get('status')
    initial_outreach_date = data.get('initial_outreach_date')
    last_contact_date = data.get('last_contact_date')
    sale_closing_date = data.get('sale_closing_date')

    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE clients SET name = ?, email = ?, phone = ?, company = ?, company_size = ?, budget = ?, industry = ?, compliance_needs = ?, status = ?, initial_outreach_date = ?, last_contact_date = ?, sale_closing_date = ? 
                      WHERE id = ?''', 
                      (name, email, phone, company, company_size, budget, industry, compliance_needs, status, initial_outreach_date, last_contact_date, sale_closing_date, client_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Client information updated successfully'})

# Delete client
@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Client deleted successfully'})

# Main entry point
if __name__ == '__main__':
    init_db()
    app.run(debug=True)