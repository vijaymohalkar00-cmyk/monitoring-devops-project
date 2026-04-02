import mysql.connector
import time
from flask import Flask

app = Flask(__name__)

def get_data():
    for i in range(5):  # retry 5 times
        try:
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password="root",
                database="monitoring"
            )
            break
        except:
            print("Waiting for DB...")
            time.sleep(5)

    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255))")

    cursor.execute("INSERT INTO logs (message) VALUES ('App is running')")

    cursor.execute("SELECT * FROM logs")
    data = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return data

@app.route('/')
def home():
    data = get_data()
    output = "<h1>Monitoring Logs:</h1>"
    for row in data:
        output += f"<p>{row}</p>"
    return output

app.run(host='0.0.0.0', port=5000)
