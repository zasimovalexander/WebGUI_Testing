import os
from datetime import datetime
from tkinter import Tk


def directory_create(name):
    if not os.access(name, os.F_OK):
        os.mkdir(name)


window = Tk()
screensize = (window.winfo_screenwidth(), window.winfo_screenheight())
window.destroy()
path = ['Reports', '', 'screenshots']
directory_create(path[0])
for cook_status in ('False', 'True'):
    for browser in ('Chrome', 'Firefox'):
        path[1] = browser
        for ph in (path[:2], path):
            directory_create('\\'.join(ph))
        date_time = datetime.now().strftime('%Y-%b-%d--%H..%M..%S')
        file = open('tmp.py', 'w')
        file.write('from selenium.webdriver import %s\n\n'
                   'browser = %s\n'
                   'screensize = %s\n'
                   'path = %s\n'
                   'date_time = "%s"\n'
                   'cook = (%s, "cookies%s")\n'
                   % (browser,
                      browser,
                      (screensize[0]-10, screensize[1]-50),
                      tuple(path),
                      date_time,
                      cook_status, cook_status))
        file.close()
        # os.system('_clean_cache.py')
        os.system('py.test --html=%s\\%s__%s__cookies%s.html'
                  ' --junit-xml=%s\\_ciserv\\%s__cookies%s.xml -o junit_suite_name=IvyPanda_testing(PyTest-Selenium-%s)'
                  % ('\\'.join(path[:2]), date_time, browser, cook_status,
                     path[0], browser, cook_status, browser.upper()))
        # from pytest import main; main(['-v', 'Tests\\'])  # it replaces the upper line for debug mode
os.remove('tmp.py')
