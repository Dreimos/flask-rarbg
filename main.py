from website import create_app
from website.config import DEBUG
app = create_app()

if __name__ == "__main__":
    app.run(debug=DEBUG, port=8080)
