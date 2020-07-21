from django.shortcuts import render
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont
from datetime import date
from django.core.mail import EmailMessage
from gen_certificate import settings
import os
import tempfile


def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Image generation
        today = date.today()
        # name_list = [name]
        # print(name_list)
        W, H = (2800, 2100)

        im = Image.open("static/image/temp_pic.png")
        d = ImageDraw.Draw(im)

        text_color = (255, 255, 255, 255)
        font = ImageFont.truetype("segoesc.ttf", 150)  # comic
        font_date_sign = ImageFont.truetype("segoesc.ttf", 40)

        w, h = d.textsize(name, font)
        today = date.today()

        d.text(((W - w) / 2, (H - h) / 2), name.title(), fill=text_color, font=font)
        d.text((720, 1560), str(today), fill=text_color, font=font_date_sign)
        d.text((1860, 1560), 'Girisha', fill=text_color, font=font_date_sign)

        # temporary directory to store file

        tmp_dir = tempfile.TemporaryDirectory()
        # predictable_filename = "certificate_" + name
        temp_path = os.path.join(tmp_dir.name, "certificate_" + name)

        im.save(temp_path+'.png')

        # email sending
        sub = 'Certificate'
        body = 'Hey ' + name.title() + ' Congratulations your certificate is ready!!'
        receiver = email
        sender = settings.EMAIL_HOST_USER
        email_mgs = EmailMessage(sub, body, sender, [receiver])

        # file attaching
        email_mgs.attach_file(temp_path+".png")
        email_mgs.send()

        return render(request, 'email_info.html', {'email': email})
    return render(request, 'login.html')


def generate_certificate(request):
    return render(request,'index.html')