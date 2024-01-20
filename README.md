**Parts list for my device:**

Raspberry Pi Zero 2W -  https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/

4 inch E-ink display -  https://www.amazon.com/gp/product/B074NR1SW2

External battery - https://www.amazon.com/gp/product/B08D678XPR

**System Settings**

Run it with:
```
$ python main.py
```

Python Dependencies:
```
pip install Flask 
```

Linux Dependencies:
```
brew install qrencode
```

E-Paper Dependencies:
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
sudo apt install python3-gpiozero
```
