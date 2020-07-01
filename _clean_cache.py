import os

for name in ('.pytest_cache', '__pycache__', 'Pages\\__pycache__', 'Tests\\__pycache__'):
    if os.access(name, os.F_OK):
        os.system('rd /s /q %s' % name)
for name in ('geckodriver.log',):
    if os.access(name, os.F_OK):
        os.remove(name)

"""
# Universal way:
for dir_path, dir_names, file_names in os.walk('.', topdown=False):
    for name in file_names:
        if name in ('geckodriver.log',):
            os.remove(os.path.join(dir_path, name))
    for name in dir_names:
        if name in ('.pytest_cache', '__pycache__'):
            os.system('rd /s /q %s' % os.path.join(dir_path, name))
"""
