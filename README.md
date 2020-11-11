## python-HTTPServer
##
## Allow a user to remotely shutdown raspberry pi zero W
## and change the date and time.
##
## Start an HTTPServer to change date and time on rpi when rpi is not coonected to the internet
## and not able to update the date-time.
## Also it allows to reboot or shutdown rpi when there is no keyboard
##
## 
## Change ip addess (python code) to match the user's network settings
## Modify rc.local to run on powerup.
##  $ sudo nano /etc/rc.local
##    sudo python /home/pi/rpiserver.py &
##
## Use a web browser and type: 
##     http://192.188.9.191:8008
## 
## See diagram.png for network setup.
