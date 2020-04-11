from zakupy_dla_seniora import create_app, db

app = create_app()
port = 80


@app.before_first_request
def manage_db():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
