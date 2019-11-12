# Attention: folder 'dist' in 'frontend' should be exist!
print('Run build.py')

import os
import shutil
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DIST_ROOT = f"{BASE_DIR}/frontend/dist"

STATIC_ROOT = f"{BASE_DIR}/mainService/mainService/static"
TEMPLATE_ROOT = f"{BASE_DIR}/mainService/mainService/template"


print('Moving folders and files ', end='')

#Move js and css to static
if os.path.exists(f"{STATIC_ROOT}/vue/"):
    shutil.rmtree(f"{STATIC_ROOT}/vue/")
os.mkdir(f"{STATIC_ROOT}/vue/")
shutil.move(f"{DIST_ROOT}/static/js/", f"{STATIC_ROOT}/vue/js/")
shutil.move(f"{DIST_ROOT}/static/css/", f"{STATIC_ROOT}/vue/css/")

print('.', end='')

#Move index.html to template
shutil.move(f"{DIST_ROOT}/index.html", f"{TEMPLATE_ROOT}/index.html")

shutil.rmtree(DIST_ROOT)

print('.')



"""		Modifying index.html	 """
#BEGIN
print('Modifying index.html ', end='')

with open(f"{TEMPLATE_ROOT}/index.html", 'r') as index_file:
	index_data = index_file.read()

print('.', end='')

#Add {% load staticfiles %}
index_data = index_data.replace(r'<html><head>', r'<html>{% load staticfiles %}<head>')

#Change: url -> "{% static 'url' %}"
links_static = re.findall(r'(src|href)=(\S*?)[ >]', index_data)
prefix = '"' + r"{% static '"
suffix = r"' %}" + '"'
for link_static in links_static:
	new_link_static = prefix + link_static[1].replace('static', 'vue') + suffix
	index_data = index_data.replace(link_static[1], new_link_static)

#Beautiful looking
index_data = index_data.replace('<', '\n<')

print('.', end='')

with open(f"{TEMPLATE_ROOT}/index.html", 'w') as index_file:
	index_file.write(index_data)

print('.')
	
#END

print('Success build!')


