from flask import Blueprint, render_template, request
from news_portal.main.utils import current_datetime
from news_portal.models import News 

main = Blueprint('main', __name__)

@main.route('/')
def home():
    business = News.query.filter_by(category='Business', status='approved').order_by(News.date.desc()).first()
    travel = News.query.filter_by(category='Travel', status='approved').order_by(News.date.desc()).first()
    sport = News.query.filter_by(category='Sports', status='approved').order_by(News.date.desc()).first()
    politics = News.query.filter_by(category='Politics', status='approved').order_by(News.date.desc()).first()
    page = request.args.get('page', 1, type=int)
    tech = News.query.filter_by(category='Technology', status='approved').order_by(News.date.desc()).paginate(page=page, per_page=5)
    page2 = request.args.get('page', 1, type=int)
    entertainment = News.query.filter_by(category='Entertainment', status='approved').order_by(News.date.desc()).paginate(page=page2, per_page=4)
    page3 = request.args.get('page', 1, type=int)
    news = News.query.filter_by(status='approved').paginate(page=page3, per_page=6)
    today = News.query.filter_by(status='approved').first()
    page4 = request.args.get('page', 1, type=int)
    latest = News.query.filter_by(status='approved').order_by(News.date.desc()).paginate(page=page2, per_page=2)
    return render_template('index.html', time=current_datetime(1), date=current_datetime(2), 
                            business=business, travel=travel, sport=sport, politics=politics, tech=tech,
                             entertainment=entertainment, news=news, today=today, latest=latest)
