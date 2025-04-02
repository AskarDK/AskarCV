from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from flask import request
import json


app = Flask(__name__)


app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_SUPPORTED_LOCALES'] = ['ru', 'en']


TELEGRAM_TOKEN = '7918334441:AAEaN5vs-seHHeB4DUu_zQhU7Fw2CXMhGc0'
TELEGRAM_CHAT_ID = '964240622'




# Путь к SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'certificates.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(300))
    image_path = db.Column(db.String(300))

    def __repr__(self):
        return f'<Certificate {self.title}>'

@app.route('/certificates')
def certificates():
    certs = Certificate.query.all()
    return render_template('certificates.html', certificates=certs)

@app.route('/')
def home():
    lang = request.args.get('lang', 'ru')
    translations = load_translations(lang)
    certs = Certificate.query.all()
    return render_template('index.html', t=translations, lang=lang, certificates=certs)

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    company = request.form.get('company')
    message = request.form.get('message')

    print(f'Сообщение от {name} ({email}, {phone}, {company}): {message}')

    text = f"<b>📩 Новое сообщение с сайта</b>\n\n" \
           f"<b>Имя:</b> {name}\n" \
           f"<b>Email:</b> {email}\n" \
           f"<b>Телефон:</b> {phone or 'Не указан'}\n" \
           f"<b>Компания:</b> {company or 'Не указана'}\n" \
           f"<b>Сообщение:</b>\n{message}"

    send_telegram_message(text)

    return jsonify({'message': 'Спасибо! Я скоро свяжусь с тобой.'})

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response.ok

def load_translations(lang='ru'):
    try:
        with open(f'translations/{lang}.json', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        with open(f'translations/ru.json', encoding='utf-8') as f:
            return json.load(f)

# ✅ Автоматическое создание базы, если её нет
if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(db_path):
            print("Создаю базу данных...")
        db.create_all()
    app.run(debug=True)
