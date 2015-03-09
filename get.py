# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import datetime
import os
import json
import requests

doc = '''
    #paste html

    '''

def convertsub(html, name):
    try:
        print name
        a_list = html.find_all('a')
        what = []
        a_list_len = a_list.__len__()
        for i in range(1, a_list_len + 1):
            if i < a_list_len:
                s = '{}\n'.format(i)
                sub = a_list[i - 1].getText().encode('utf-8') + '\n\n'
                sub_time = time_sub(a_list[i - 1], a_list[i])
                s = s + sub_time + sub
                what.append(s)
            else:
                s = '{}\n'.format(i)
                sub = a_list[i - 1].getText().encode('utf-8') + '\n\n'

                x = a_list[i - 1].get('href').split(',')[1].strip()
                y = a_list[i - 1].get('href').split(',')[1].strip()
                if not RepresentsInt(x):
                    x = float(x)
                    x = datetime.timedelta(seconds=round(x, 3))
                    x = str(x)[:-3]
                else:
                    x = datetime.timedelta(seconds= int(x))
                    x = str(x)

                if not RepresentsInt(y):
                    y = float(y) + 7
                    y = datetime.timedelta(seconds=round(y, 3))
                    y = str(y)[:-3]
                else:
                    y = datetime.timedelta(seconds= int(y) +7)
                    y = str(y)



                sub_time = '{0} --> {1}\n'.format(x.replace('.', ','), y.replace('.',','))
                s = s + sub_time + sub
                what.append(s)

        f = open(name + '.srt', 'w')
        for u in what:
            f.write(u)
        f.close()
    except IOError:
        print name
        print what
    except Exception as mess:
        print mess


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def time_sub(x, y):
    x = x.get('href').split(',')[1].strip()
    y = y.get('href').split(',')[1].strip()

    if not RepresentsInt(x):
        x = float(x)
        x = datetime.timedelta(seconds = round(x, 3))
        x = str(x)[:-3]
    else:
        x = datetime.timedelta(seconds = int(x))
        x = str(x)
    if not RepresentsInt(y):
        y = float(y)
        y = datetime.timedelta(seconds = round(y, 3))
        y = str(y)[:-3]
    else:
        y = datetime.timedelta(seconds = int(y))
        y = str(y)

    return '{0} --> {1}\n'.format(x.replace('.', ','), y.replace('.',','))


def main():
    global doc
    main_directory = os.getcwd()

    html = bs(doc)
    part_list = html.find_all('div', {"ng-show": "transcripts.userIsAuthorizedForCourseTranscripts"})
    stt_part = 1
    for part in part_list:
        sub_folder_name = part.h4.get_text()
        os.mkdir(str(sub_folder_name))
        os.chdir(sub_folder_name)
        chapter_list = part.find_all('div')
        stt_chapter = 1
        for chapter in chapter_list:
            name = chapter.h6.get_text().encode('utf-8')
            if name.find(':'):
                name = name.replace(':', '')
            a = chapter.find_all('p',{"class":"ng-isolate-scope"})[0]
            if stt_chapter < 10:
                convertsub(a, '{0}_{1}-'.format('0'+str(stt_part), '0'+str(stt_chapter)) + name)
            else:
                convertsub(a, '{0}_{1}-'.format('0' + str(stt_part), str(stt_chapter)) + name)
            stt_chapter += 1
        os.chdir(main_directory)
        stt_part += 1




if __name__ == '__main__':
    main()