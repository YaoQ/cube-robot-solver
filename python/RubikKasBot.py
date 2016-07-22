## Rubik kasBot             @ kas 2014

## This script will:
##  launch Cube Explorer
##  move the cube, face by face, for color recognition by Cube Explorer ([Scan colors] button)
##  request and obtain the solution from Cube Explorer
##  transfer this solution to Arduino ([Solve cube] button)

## V1.3 communication with Cube Explorer (Web server)
## V1.2 slow/fast cube moves
## V1.1 communication error management
## V1.0 initial release, serial communication with Arduino only

from tkinter import *
import urllib.request
import serial, time
from serial import SerialException
import atexit
import subprocess

##  Settings
## webcam setUp: white balance 6253°K (manual), Exposition: -6 (manual) >> -9

defaultPortNumber = '3'                     ##  default Serial port
## cubeExplorerPath = 'C:\Program Files (x86)\Cube Explorer\cube512htm.exe'      ## Cube Explorer program path
cubeExplorerPath = 'C:\\Program Files\\Cube Explorer\\cube512htm.exe' ## Cube Explorer program path
cubeExplorer = 'http://127.0.0.1:8081/'     ## Cube Explorer web server address
webCamConnect = '?connect1'                 ##  connects to 2nd device in Cube Explorer device drop down
delayB4scan = 1                             ##  delay before scanning

scanSide = 0
root =Tk()
root.title('Rubik kasBot')
root.geometry('325x335+1575+0')    # window size + position

vSolve = StringVar()
comVar = IntVar()
speedVar = IntVar()
comSent = StringVar()
comIn = StringVar()
vErrror = StringVar()
vComPort = StringVar()
vComPort.set(defaultPortNumber)

vSolve.set("WB: 6253 (manual), Exposition: -7 to -9 (manual)")
comSent.set("")
comIn.set("")

def bGetScan_CallB():
  vSolve.set("")
  page = sendURL(webCamConnect)
  if 'Done' in page:
    if backScan() and leftScan() and frontScan() and rightScan() and upScan() and  downScan() and front2Scan():
      page = sendURL("?transfer")
      if 'wrong' in page:
        vSolve.set("** Bad scan **")
      else:
        time.sleep(delayB4scan)
        page = sendURL("?getLast")
        vSolve.set(page)

def sendURL(command):
  try:
    f = urllib.request.urlopen(cubeExplorer + command)
    print(cubeExplorer + command)
    page = str(f.read())
  except:
    vSolve.set("No response from Cube Explorer")
    page = "<HTML><BODY>    No response from Cube Explorer    </BODY></HTML>"
  print(page)
  page = page[page.find('<')+16:]
  page = page[:page.find('<')-4]
  return page

def bSolve_CallB():
  if not('Buffer' in vSolve.get()) and not('Error' in vSolve.get()) and not('response' in vSolve.get()):
    arduino.write(b"\x02")
    arduino.write(str.encode(vSolve.get() + 'T'))
    arduino.write(b"\x03")
  else:
    vSolve.set("")

#--< Scan >------------
def backScan():
  vSolve.set("Face #1")
  comSent.set("x02 b x03")
  arduino.flushInput()
  arduino.write(b"\x02 b \x03")
  data = str(arduino.readline())
  print (data)
  if 'OK' in data:
    comIn.set(data)
    time.sleep(delayB4scan)
    page = sendURL("?scanB")
    if 'Done' in page:
      vSolve.set("Face #1")
      root.update()
      return True
    else:
      vSolve.set("BACK scan Error")
      return False
  else:
    displayComError("Arduino not responding (B)")
    return False

def leftScan():
  comSent.set("x02 l x03")
  arduino.write(b"\x02 l \x03")
  data = str(arduino.readline())
  print (data)
  if 'OK' in data:
    comIn.set(data)
    time.sleep(delayB4scan)
    page = sendURL("?scanL")
    if 'Done' in page:
      vSolve.set("Face #2")
      root.update()
      return True
    else:
      vSolve.set("LEFT scan Error")
      return False
  else:
    displayComError("Arduino not responding (L)")
    return False

def frontScan():
  comSent.set("x02 f x03")
  arduino.write(b"\x02 f \x03")
  data = str(arduino.readline())
  print (data)
  if 'OK' in data:
    comIn.set(data)
    time.sleep(delayB4scan)
    page = sendURL("?scanF")
    if 'Done' in page:
      vSolve.set("Face #3")
      root.update()
      return True
    else:
      vSolve.set("FRONT scan Error")
      return False
  else:
    displayComError("Arduino not responding (F)")
    return False

def rightScan():
  comSent.set("x02 r x03")
  arduino.write(b"\x02 r \x03")
  data = str(arduino.readline())
  print (data)
  if 'OK' in data:
    comIn.set(data)
    time.sleep(delayB4scan)
    page = sendURL("?scanR")
    if 'Done' in page:
      vSolve.set("Face #4")
      root.update()
      return True
    else:
      vSolve.set("RIGHT scan Error")
      return False
  else:
    displayComError("Arduino not responding (R)")
    return False

def upScan():
  comSent.set("x02 u x03")
  arduino.write(b"\x02 u \x03")
  data = str(arduino.readline())
  print (data)
  if 'OK' in data:
    comIn.set(data)
    time.sleep(delayB4scan)
    page = sendURL("?scanU")
    if 'Done' in page:
      vSolve.set("Face #5")
      root.update()
      return True
    else:
      vSolve.set("UP scan Error")
      return False
  else:
    displayComError("Arduino not responding (U)")
    return False

def downScan():
  comSent.set("x02 d x03")
  arduino.write(b"\x02 d \x03")
  data = str(arduino.readline())
  print (data)
  if 'OK' in data:
    comIn.set(data)
    time.sleep(delayB4scan)
    page = sendURL("?scanD")
    if 'Done' in page:
      vSolve.set("Face #6")
      root.update()
      return True
    else:
      vSolve.set("DOWN scan Error")
      return False
  else:
    displayComError("Arduino not responding (D)")
    return False

def front2Scan():
  comSent.set("x02 g x03")
  arduino.write(b"\x02 g \x03")
  data = str(arduino.readline())
  print (data)
  if 'OK' in data:
    comIn.set(data)
    return True
  else:
    displayComError("Arduino not responding (F2)")
    return False
 ## ------------------------------------------------

def bTestScan_CallB():  ## move the cube to check and tune color recognition
  global scanSide
  try:
    if scanSide == 0:
      arduino.write(b"\x02 b \x03")
      print('b')
    elif scanSide == 1:
      arduino.write(b"\x02 l \x03")
      print('l')
    elif scanSide == 2:
      arduino.write(b"\x02 f \x03")
      print('f')
    elif scanSide == 3:
      arduino.write(b"\x02 r \x03")
      print('r')
    elif scanSide == 4:
      arduino.write(b"\x02 u \x03")
      print('u')
    elif scanSide == 5:
      arduino.write(b"\x02 d \x03")
      print('d')
    elif scanSide == 6:
      arduino.write(b"\x02 g \x03")
      print('g')

    scanSide += 1
    time.sleep(1)
    vSolve.set("Face #" + str(scanSide))
    root.update()
    if scanSide > 6:
      arduino.write(b"\x02 V2 \x03")
      scanSide = 0
  except:
    displayComError('COM' + vComPort.get() +" closed")

def speed_CallB():
  if speedVar.get():
    arduino.write(b"\x02 S2 \x03")
  else:
    arduino.write(b"\x02 S1 \x03")

def com_CallB():
  if comVar.get():
    root.update()
    global arduino
    try:
      arduino = serial.Serial('COM' + vComPort.get(), 57600, timeout=15)
      time.sleep(1.25)                           #give time to settle
      sComPort.config(state = DISABLED)
      print("COM  <ON>")
      comSent.set("COM  <ON>")
      EnableButtons(True)
      speedVar.set(True)
    except SerialException:
      EnableButtons(False)
      comVar.set(False)
      displayComError('COM' + vComPort.get() +" not available")
  else:
    speedVar.set(False)
    EnableButtons(False)
    arduino.close()
    sComPort.config(state = NORMAL)
    print("COM  <OFF>")
    comSent.set("COM  <OFF>")
    comIn.set("")

## utilities ------------------------------------
def displayComError(message):
  vErrror.set(message)
  root.update()
  print(message)
  time.sleep(delayB4scan)
  vErrror.set("")

def bReset_CallB():
  global scanSide
  vSolve.set("")
  comIn.set("-")
  comSent.set("-")
  scanSide = 0
  page = sendURL("?clear")
  if comVar.get():
    arduino.write(b"\x02 T \x03")
    print("\x02 T \x03")

def EnableButtons(flag):
  if flag == True:
    aspect = NORMAL
  else:
    aspect = DISABLED
  bGetScan.config(state=aspect)
  bSolve.config(state=aspect)
  eSolve.config(state=aspect)
  checkSpeed.config(state=aspect)

def cleanup():  ## Exit Cube Explorer and close COM port
  if comVar.get():
    arduino.close()
  p.kill()
atexit.register(cleanup)

## UI elements --------------------------
bGetScan = Button(padx=56, pady=0, bd=3,text="Scan colors ", fg="black", font=('arial', 16), command = bGetScan_CallB)
bGetScan.place(x=20, y=25, height=55, width=285)

bTestScan = Button(padx=0, pady=0, bd=2, text="test", fg="black", font=('consolas', 6), command = bTestScan_CallB)
bTestScan.place(x=240, y=84, height=17, width=31)

bReset = Button(padx=0, pady=0, bd=2, text="reset", fg="black", font=('consolas', 6), command = bReset_CallB)
bReset.place(x=273, y=84, height=17, width=31)

eSolve = Entry(textvariable = vSolve, width = 60, fg="Blue", bd = 2, font=('arial', 6))
eSolve.place(x=20, y=135, height=20, width=285)

bSolve = Button(padx=59, pady=0, bd=3, text="Solve cube ", fg="black", font=('arial', 16), command = bSolve_CallB)
bSolve.place(x=20, y=160, height=55, width=285)

checkSpeed = Checkbutton(text = "High speed", variable = speedVar, command = speed_CallB)
checkSpeed.place(x=20, y=255)

tError = Label(textvariable = vErrror, fg = "red", bd = 3, font=('arial', 8))
tError.place(x=160, y=260)

checkCom = Checkbutton(text = "COM", variable = comVar, command = com_CallB)
checkCom.place(x=20, y=287)

tComOut = Label(textvariable = comSent, bd = 3, font=('arial', 8))
tComOut.place(x=140, y=278)

tComIn = Label(textvariable = comIn, bd = 3, font=('arial', 8))
tComIn.place(x=140, y=297)

sComPort = Spinbox(from_=1, to=9, width = 1, textvariable=vComPort)
sComPort.place(x=80, y=289)

try:
  p=subprocess.Popen([cubeExplorerPath])    ## Cube Explorer launching
except:
  vSolve.set("** Cube Explorer not found **")
checkCom.invoke()
root.mainloop()

