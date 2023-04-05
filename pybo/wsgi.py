import os
from flask import Flask
from pybo import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
