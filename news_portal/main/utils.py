import os
import os.path as op
import secrets
from PIL import Image
from news_portal import app
from datetime import datetime, date

# Current date and Time
def current_datetime(dt):
    if dt == 1:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%p")
        return current_time
    elif dt == 2:
        today = date.today()
        current_date = today.strftime("%A, %b-%d-%Y")
        return current_date
    else:
        pass

# save picture
def save_image(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    img = random_hex + f_ext
    img_path = os.path.join(app.root_path, 'static/upload_pic', img)
    output_size = (150, 150) #125x125px
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(img_path)
    return img