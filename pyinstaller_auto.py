import os

command = """
rm -rf ./for_window ./for_linux
pyinstaller kkutuHack.py --onefile
mkdir for_linux
mv ./build ./dist ./kkutuHack.spec ./for_linux
cp ./driverpath.txt ./db.txt ./no_list.txt ./for_linux/dist

wine pyinstaller kkutuHack.py --onefile
mkdir for_window
mv ./build ./dist ./kkutuHack.spec ./for_window
cp ./driverpath.txt ./db.txt ./no_list.txt ./for_window/dist 
"""

os.system(command)