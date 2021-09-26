import requests
from flask import redirect, url_for, flash, request
from flask_login import current_user
from functools import wraps
from .models import Favourite


def liked_movie_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.favs:
            flash("Nie dodales zadnego filmu do ulubionych")
            return redirect(url_for("home"))
        else:
            return func(*args, **kwargs)

    return wrapper


def not_log_in(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if current_user:
            flash('Jesteś już zalogowany')
            return redirect(url_for("home"))
        else:
            return func(*args,**kwargs)
    return wrapper

