# app/__init__.py
from flask import Flask
from app.extensions import db, login_manager, migrate
from dotenv import load_dotenv
load_dotenv()
