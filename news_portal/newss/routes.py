import os
import os.path as op
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from news_portal import app, db 
from news_portal.models import News
from news_portal.newss.forms import NewsForm, EditNewsForm
from news_portal.main.utils import save_image
from news_portal.main.utils import current_datetime 

newss = Blueprint('newss', __name__)

# addnews route
@newss.route('/addnews', methods=['GET', 'POST'])
@login_required
def addnews():
    form = NewsForm()
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(uid=current_user.id).order_by(News.date.desc()).paginate(page=page, per_page=4)
    n = News.query.filter_by(uid=current_user.id).all()
    if n:
        msg=""
    else:
        msg="No news Added"
    if form.validate_on_submit():
        if form.news_img.data:
            img_file = save_image(form.news_img.data)
            img = img_file
        news = News(heading=form.heading.data, description=form.description.data, district=form.district.data, place=form.place.data, category=form.category.data, news_img=img, uid=current_user.id)
        db.session.add(news)
        db.session.commit()
        flash('Your News Uploaded Successfully!','addnews')
        return redirect(url_for('newss.addnews'))
    return render_template('addnews.html', title='Add_News', form=form, news=news, msg=msg, time=current_datetime(1), date=current_datetime(2))

# edit news route
@newss.route('/editnews/<int:news_id>', methods=['GET', 'POST'])
@login_required
def editnews(news_id):
    form2 = EditNewsForm()
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(uid=current_user.id).order_by(News.date.desc()).paginate(page=page, per_page=4)
    if news:
        msg=""
    else:
        msg="No news Added"
    current_news = News.query.filter_by(id=news_id).first()
    if form2.validate_on_submit():
        if form2.news_img.data:
            try:
                os.unlink(os.path.join(app.root_path, 'static/upload_pic', current_news.news_img))
                img_file = save_image(form2.news_img.data)
                current_news.news_img = img_file
            except:
                img_file = save_image(form2.news_img.data)
                current_news.news_img = img_file
        current_news.heading = form2.heading.data
        current_news.description = form2.description.data
        current_news.district = form2.district.data
        current_news.place = form2.place.data
        current_news.category = form2.category.data
        db.session.commit()
        flash('Your News has been updated!','editnews')
        return redirect(url_for('newss.editnews', news_id=current_news.id))
    elif request.method == 'GET':
        form2.heading.data = current_news.heading
        form2.description.data = current_news.description
        form2.district.data = current_news.district
        form2.place.data = current_news.place
        form2.category.data = current_news.category
        news_id = news_id
    return render_template('editnews.html', title='Edit News', form2=form2, news=news, msg=msg, news_id=news_id, time=current_datetime(1), date=current_datetime(2))

# Delete News
@newss.route('/deletenews/<int:news_id>', methods=['POST'])
@login_required
def deletenews(news_id):
    news =News.query.get_or_404(news_id)
    if news.uid != current_user.id:
        abort(403)
    os.unlink(os.path.join(app.root_path, 'static/upload_pic', news.news_img))
    db.session.delete(news)
    db.session.commit()
    flash('Your News has been deleted!', 'deletenews')
    return redirect(url_for('newss.addnews'))

# News categories
@newss.route('/<string:category>', methods=['GET'])
def categories(category):
    n = News.query.filter_by(category=category).all()
    if n:
        msg=""
    else:
        msg="No news Added"
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(category=category).order_by(News.date.desc()).paginate(page=page, per_page=5)
    return render_template('categories.html', title=category, news=news, msg=msg, time=current_datetime(1), date=current_datetime(2))

# Single News
@newss.route('/<string:category>/<int:id>', methods=['GET'])
def single(category,id):
    news = News.query.filter_by(id=id).first()
    return render_template('single_post.html', title=category, news=news, time=current_datetime(1), date=current_datetime(2))
