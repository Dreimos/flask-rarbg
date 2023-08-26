from website import create_app, DEBUG

app = create_app()

if __name__ == "__main__":
    app.run(debug=DEBUG, port=8080)
