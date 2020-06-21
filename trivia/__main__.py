from trivia.create_app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=False)
