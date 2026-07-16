#!/bin/bash
# Helper: connect Celestron GPS on /dev/ttyUSB0 @ 9600 after services up
set -e
source /home/pi/starwatch/.venv/bin/activate
python3 <<'PY'
import time, PyIndi
class C(PyIndi.BaseClient):
    def newDevice(self,d): pass
    def newProperty(self,p): pass
    def updateProperty(self,p): pass
    def removeProperty(self,p): pass
    def newMessage(self,d,i):
        try: print(d.messageQueue(i))
        except: pass
    def serverConnected(self): pass
    def serverDisconnected(self,c): pass
c=C(); c.setServer("localhost",7624)
assert c.connectServer()
time.sleep(1)
d=c.getDevice("Celestron GPS")
assert d
port=d.getText("DEVICE_PORT")
port[0].setText("/dev/ttyUSB0"); c.sendNewText(port); time.sleep(0.2)
baud=d.getSwitch("DEVICE_BAUD_RATE")
for i in range(len(baud)):
    baud[i].setState(PyIndi.ISS_ON if baud[i].getName()=="9600" else PyIndi.ISS_OFF)
c.sendNewSwitch(baud); time.sleep(0.2)
conn=d.getSwitch("CONNECTION")
for i in range(len(conn)):
    conn[i].setState(PyIndi.ISS_ON if conn[i].getName()=="CONNECT" else PyIndi.ISS_OFF)
c.sendNewSwitch(conn); time.sleep(3)
print("connected", d.isConnected())
n=d.getNumber("EQUATORIAL_EOD_COORD")
if n and len(n)>=2: print("RA", n[0].getValue(), "DEC", n[1].getValue())
c.disconnectServer()
PY
