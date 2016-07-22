# Cube Robot Solver
The robot will be semi-autonomous

* Color recognition and solving to be made at PC level
* Cube movements performed under Arduino control, at robot level

Solving will be done through already existing software, [Cube Explorer](http://kociemba.org/cube.htm) appears to be a good candidate

A middleware will be developed  (using Processing or Python) to convey information back and forth 
between Arduino and cube solver software

Road map:
- design a suitable gripper
- robot construction (2 grippers), test and tuning
- develop Arduino code for moving the Cube
- develop the software link between solving and moving
- final integration

**Frame**
- Plywood 10mm

**Grippers**
- Plywood 5mm (plexiglass, or PVC)
- 4 standard servo's
- M3 screws 10, 16, 20 and 24mm 
- 3mm washers
- M3 nuts
- M3 Nylock nuts
- 14mm brass standoff spacers

** Cube**
- Dayan GuHong (57 mm)

**Other parts**
- Flexible mini 28 LED USB lamp  (4 bucks shipped)
- Custom shield with 4 servo's sockets
- Webcam with optional manual White Balance

**Software**
- Arduino:   [CubeMover V1.2](http://forum.arduino.cc/index.php?PHPSESSID=nr959s43t7dku2gdtrahj3qtb3&topic=271827.msg2063754#msg2063754)        [VarSpeedServo Library](https://github.com/netlabtoolkit/VarSpeedServo)
- Python (PC):   [RubikKasBot V1.3](http://forum.arduino.cc/index.php?PHPSESSID=nr959s43t7dku2gdtrahj3qtb3&topic=271827.msg2094567#msg2094567)
- Solving (PC):   [Cube Explorer](http://kociemba.org/cube.htm)


![](http://i.imgur.com/WrbkEFr.png)


![](http://i.imgur.com/72XtOIn.jpg)
# Ref
[Rubik's cube Robot solver](http://forum.arduino.cc/index.php?topic=271827.0)
