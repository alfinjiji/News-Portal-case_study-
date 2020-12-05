from flask import Blueprint, render_template
from news_portal.main.utils import current_datetime 

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', time=current_datetime(1), date=current_datetime(2))
