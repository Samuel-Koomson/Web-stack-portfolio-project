from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import pyperclip
import json

app = Flask(__name__)

# ... Your existing code ...

@app.route('/')
def index():
    return render_template('index.html')  # Create a new HTML file for your main page

@app.route('/generate_password', methods=['POST'])
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
               'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
               'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pass_letters = [random.choice(letters) for item in range(nr_letters)]
    pass_symbols = [random.choice(symbols) for i in range(nr_symbols)]

    pass_numbers = [random.choice(numbers) for n in range(nr_numbers)]

    password_list = pass_letters + pass_symbols + pass_numbers
    random.shuffle(password_list)
    password = "".join(password_list)

    password_text.insert(0, password)
    pyperclip.copy(password)

    password = "".join(password_list)
    pyperclip.copy(password)
    return jsonify({'password': password})

@app.route('/save_data', methods=['POST'])
def save_data():
    website = request.form.get('website')
    user_id = request.form.get('email')
    password = request.form.get('password')

    if len(website) == 0 or len(password) == 0 or len(user_id) == 0:
        return jsonify({'error': 'Fields cannot be empty'})

    with open("password_data.json", 'r') as pass_data:
        data = json.load(pass_data)
        data[website] = {'user_id': user_id, 'password': password}

    with open("password_data.json", 'w') as pass_data:
        json.dump(data, pass_data, indent=4)

    return jsonify({'message': 'Data saved successfully'})

@app.route('/view_passwords', methods=['GET'])
def view_passwords():
    with open("password_data.json", 'r') as pass_data:
        data = json.load(pass_data)
        passwords = []
        for website, info in data.items():
            passwords.append({
                'website': website,
                'user_id': info['user_id'],
                'password': info['password']
            })
        return jsonify(passwords)

@app.route('/search_password', methods=['POST'])
def search_password():
    website = request.form.get('website')
    with open("password_data.json", 'r') as pass_data:
        data = json.load(pass_data)
        if website in data:
            info = data[website]
            return jsonify({
                'website': website,
                'user_id': info['user_id'],
                'password': info['password']
            })
        else:
            return jsonify({'error': f'No password found for {website}'})

@app.route('/delete_password', methods=['POST'])
def delete_password():
    website = request.form.get('website')
    with open("password_data.json", 'r') as pass_data:
        data = json.load(pass_data)
        if website in data:
            del data[website]
            with open("password_data.json", 'w') as pass_data:
                json.dump(data, pass_data, indent=4)
            return jsonify({'message': f'Password for {website} deleted successfully'})
        else:
            return jsonify({'error': f'No password found for {website}'})

@app.route('/delete_all_passwords', methods=['POST'])
def delete_all_passwords():
    with open("password_data.json", 'w') as pass_data:
        json.dump({}, pass_data)
    return jsonify({'message': 'All passwords deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)