import os
from flask import Flask
from dotenv import load_dotenv
from project.init import create_app

load_dotenv()

PORT = int(os.getenv('PORT') or '5000')
DEV = bool(os.getenv('DEV') or True)

app = create_app()

if __name__ == '__main__':
    app.run(port=PORT, debug=DEV)
