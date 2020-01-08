import os
import shutil

if os.path.exists("dist"):
    shutil.rmtree("dist")

os.system("sphinx-build -E -b html . build index.rst")

os.mkdir("dist")
os.rename("build/index.html", "dist/index.html")
shutil.move("build/_static", "dist/_static")
# shutil.rmtree("build")
