from django.shortcuts import render
import googletrans
import gtts
import sys
import os
from convert import *
import summarize
from home.models import Files
from django.core.mail import EmailMessage

reload(sys)
# noinspection PyUnresolvedReferences
sys.setdefaultencoding("utf-8")


# noinspection PyUnresolvedReferences
def index(request):
    if request.method == "POST":
        if request.FILES['pdf']:
            temp_file = Files()
            temp_file.file_field = request.FILES.get('pdf')
            temp_file.save()

            text = convert(temp_file.file_field.path).decode('utf-8', 'ignore')
            text = sanitize_input(text)
            input_file = open('input_file.txt', 'w')
            input_file.write(text.encode('utf-8'))
            input_file = open('input_file.txt', 'r')
            section(input_file)
            input_file = open('input_file.txt', 'r')
            temp_input = ""
            for line in input_file.readlines():
                if len(line) <= 15:
                    continue
                else:
                    temp_input += line
            input_file = open('input_file.txt', 'w')
            input_file.write(temp_input.encode('utf-8'))
            temp = ""
            temp2 = None
            input_file = open('input_file.txt', 'r')
            translator = googletrans.Translator()
            for line in input_file.readlines():
                try:
                    temp2 = translator.translate(line, dest='hi')
                    print(temp2.text)
                except ValueError:
                    for character in line:
                        print('loop')
                        try:
                            temp2 = translator.translate(character, dest='hi')
                            print(temp2.text)
                        except ValueError:
                            line.replace(character, '')

                temp += temp2.text

            # temp = translator.translate(text, dest='mr')
            gtts_object = gtts.gTTS(text=temp, lang="hi", slow=False)
            gtts_object.save('voice.mp3')

            doc = Document('summary')
            doc.documentclass = Command(
                'documentclass',
                options=['conference'],
                arguments=['IEEEtran'],
            )
            text = sanitize_input(temp_input)
            with doc.create(Section('Summary:')):
                doc.append(text.decode('utf-8'))

            doc.generate_pdf()

            mail_subject = 'TEST'
            message = "Test body"
            email_message = EmailMessage(
                mail_subject, message, to=['rj203171@gmail.com']
            )
            email_message.attach_file('summary.pdf')
            email_message.attach_file('voice.mp3')
            email_message.send()
    return render(request, 'home/index.html', {'languages': gtts.lang.tts_langs()})
