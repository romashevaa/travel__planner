import os


class Config:
    SECRET_KEY = 'dev-key'  # замінити пізніше
    SQLALCHEMY_DATABASE_URI = 'sqlite:///travel_planner.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
