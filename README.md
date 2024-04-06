# Generell für den Webserver/Skripte
sudo apt-get install python3
sudo apt-get install python3-rpi.gpio
sudo apt-get install python3-pip

# spidev installieren - Zum Auslesen des MCP3008-Chips (ADC)
sudo apt-get install git
git clone https://github.com/Gadgetoid/py-spidev
cd py-spidev
sudo python3 setup.py install

# SPI-Schnittstelle dauerhaft aktivieren
sudo raspi-config -> Interfacing Options -> SPI -> Yes/Ja
sudo shutdown -r 0

# requirements.txt installieren - FastAPI-Webserver PIP-Plugins
cd /home/water/pflanze
sudo pip3 install -r requirements.txt

# Weitere Dokumentationen:
~/doc/cronjob_doc.txt
-> Erklärt, wie man CronJobs einrichtet, um die Pflanzen automatisch zu bewässern, falls sie zu trocken sind
~/dpc/autostart_doc.txt
-> Erklärt, wie man den Web-Server automatisch beim Boot des Raspberry-Pi's starten kann