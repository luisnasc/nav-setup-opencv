#!/bin/bash

#cp ./read_image.py nav_setup_app/script_nav_setup.py
#cp ./ScrollableImage.py ~/nav_setup_app
#cp ./icon.png ~/nav_setup_app
#cp ./config.json ~/nav_setup_app

caminho=`pwd`



chmod +x ./source/script_nav_setup.py


mkdir -p venv-setup-nav
cd venv-setup-nav
#wget https://bootstrap.pypa.io/get-pip.py
#python3 get-pip.py
apt-get install python3-pip
pip install virtualenv

rm get-pip.py
cd ..

python3 -m pip install virtualenv
python3 -m virtualenv venv-setup-nav
source venv-setup-nav/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow



pip3 install virtualenvwrapper tk opencv-python numpy matplotlib


cat <<EOF >~/.local/share/applications/setup-nav.desktop
#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Name=Setup-Nav
Comment=This is my comment
Exec=$caminho/venv-setup-nav/bin/python3 $caminho/source/script_nav_setup.py
Icon=$caminho/source/icon.png
Path=$caminho
Terminal=true
Type=Application
Categories=Utility;Application;
EOF

deactivate

cat <<EOF >./executar.sh
#!/bin/bash
clear
cd source/
../venv-setup-nav/bin/python3 script_nav_setup.py
EOF

chmod +x ./executar.sh

mv ./instalacao.sh $caminho/source
