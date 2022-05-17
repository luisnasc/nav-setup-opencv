#!/bin/bash

#cp ./read_image.py nav_setup_app/script_nav_setup.py
#cp ./ScrollableImage.py ~/nav_setup_app
#cp ./icon.png ~/nav_setup_app
#cp ./config.json ~/nav_setup_app

caminho=`pwd`

chmod +x ./script_nav_setup.py
mkdir venv-setup-nav
cd venv-setup-nav
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py

pip3 install virtualenv 
source /venv-setup-nav/bin/activate


pip3 install virtualenvwrapper json tkinter cv2 numpy PIL matplotlib
virtualenv venv-setup-nav


cat <<EOF >~/.local/share/applications/setup-nav.desktop
#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Name=Setup-Nav
Comment=This is my comment
Exec=$caminho/venv-setup-nav/bin/python3 $caminho/read_image.py
Icon=$caminho/icon.png
Path=$caminho
Terminal=true
Type=Application
Categories=Utility;Application;
EOF

deactivate
