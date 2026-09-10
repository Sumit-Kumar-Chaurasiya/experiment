from flask import Flask, request, render_template_string
from selenium import webdriver
import threading
import time


app = Flask(__name__)

# --------------------------------------------------
# HTML for our local command page
# --------------------------------------------------

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Selenium Assistant</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 50px;
        }

        .container {
            max-width: 700px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        h1 {
            margin-bottom: 25px;
        }

        input {
            width: 70%;
            padding: 14px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }

        button {
            padding: 14px 20px;
            font-size: 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        .message {
            margin-top: 20px;
            padding: 12px;
            background: #eee;
            border-radius: 6px;
        }

        .examples {
            margin-top: 30px;
            color: #555;
        }

        code {
            display: block;
            margin: 8px 0;
            padding: 8px;
            background: #f1f1f1;
            border-radius: 4px;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🤖 Selenium Assistant</h1>

    <form method="POST">

        <input
            type="text"
            name="command"
            placeholder="Enter command..."
            autofocus
            autocomplete="off"
        >

        <button type="submit">
            Run
        </button>

    </form>

    {% if message %}
        <div class="message">
            {{ message }}
        </div>
    {% endif %}

    <div class="examples">
        <h3>Commands</h3>

        <code>open youtube</code>
        <code>open google</code>
        <code>open github</code>

    </div>

</div>

</body>
</html>
"""


# --------------------------------------------------
# Selenium browser
# --------------------------------------------------

driver = None


def start_browser():
    global driver

    # Start ONE Chrome window
    driver = webdriver.Chrome()

    # Open our Flask command page
    driver.get("http://127.0.0.1:5000")


# --------------------------------------------------
# Open website in a NEW TAB
# --------------------------------------------------

def open_new_tab(url):

    # Create a new tab in the SAME Chrome window
    driver.switch_to.new_window("tab")

    # Open the requested website
    driver.get(url)


# --------------------------------------------------
# Command processor
# --------------------------------------------------

def process_command(command):

    command = command.lower().strip()

    if command == "open youtube":

        open_new_tab("https://www.youtube.com")

        return "YouTube opened in a new tab."

    elif command == "open google":

        open_new_tab("https://www.google.com")

        return "Google opened in a new tab."

    elif command == "open github":

        open_new_tab("https://github.com")

        return "GitHub opened in a new tab."

    else:

        return f"Unknown command: {command}"


# --------------------------------------------------
# Flask route
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        command = request.form.get("command", "")

        if command.strip():

            message = process_command(command)

        else:

            message = "Please enter a command."

    return render_template_string(
        HTML,
        message=message
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    # Start Flask in a background thread
    flask_thread = threading.Thread(
        target=lambda: app.run(
            host="127.0.0.1",
            port=5000,
            debug=False,
            use_reloader=False
        )
    )

    flask_thread.daemon = True
    flask_thread.start()

    # Give Flask a moment to start
    time.sleep(1)

    # Start Selenium Chrome
    start_browser()

    # Keep Python running
    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("Closing browser...")

        if driver:
            driver.quit()
