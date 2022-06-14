from project import create_app
import settings

app = create_app()

if __name__ == '__main__':
    app.run(port=settings.FLASK_PORT, debug=settings.DEV)
