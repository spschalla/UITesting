import sys
import random
import time
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt;
from PySide6.QtGui import *


# Checks whether windows are open or not 
zero_windows = 0;
selection_windows = 0;

# Check how we measure (type of sensor)
strain_gauge = None;
pressure_transduce = None;

# Check what the zeroed for pressure sensor is 
zero_pressure = 0;

# Check the units we display
mmHg = -1;
cmHg = -1;

# Check what opening pressure is 
openPressure = 0;
closePressure = None;

# Record what open delay is 
openDelay = None;

# volume info
volumeFlowRate = 0;
unlimit = False;


# clamp info

unlimitTime = False;
clampTime = 0;

class Selection(QWidget):

  def __init__(self):
    super().__init__();
    self.setFixedWidth(800);
    self.setFixedHeight(480);
    
    self.grid = QGridLayout();
    for i in range(0,9):
      for j in range(0,9):
        self.grid.addWidget(QLabel(""), i, j);
    
    # Welcome Label    
    self.drainType = QLabel("How would you like to drain?");
    self.drainType.setFont(QFont("Times", 38));
    
    # Pressure Drainage Option 
    self.pressure = QPushButton("By Pressure");
    self.pressure.setFont(QFont("Times", 24));  
    self.pressure.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding);
    self.pressure.clicked.connect(self.units);
    

 
    # Volume Drainage Option
    self.volume = QPushButton("By Volume");
    self.volume.setFont(QFont("Times", 24));
    
    self.volume.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding);
    self.volume.clicked.connect(self.VolumeScreen) 
    # Clamped Drainage Option
    self.clamped = QPushButton("Clamped");
    self.clamped.setFont(QFont("Times", 24));
    self.clamped.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding);
    self.clamped.clicked.connect(self.Clamped)
    # Unit Buttons     
    self.mmHg = QPushButton("mmHg");
    self.mmHg.setFont(QFont("Times", 30));
    self.cmHg = QPushButton("cmHg");
    self.cmHg.setFont(QFont("Times", 30));
    self.mmHg.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding); 
    self.cmHg.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding);
    self.cmHg.clicked.connect(self.setcmHg)
    self.mmHg.clicked.connect(self.setmmHg)   
    # Sliders 

    # Pressure Slider 

    # Opening Pressure Slider 
    self.opening_label = QLabel("What is the Opening Pressure?");
    self.opening_label.setFont(QFont("Times", 40));
  
    # Opening Pressure Slider
    self.opening_pressure = QSlider(Qt.Horizontal);
    self.opening_pressure.setMinimum(-5);
    
    self.opening_pressure.setMaximum(20);
    self.opening_pressure.setTickPosition(QSlider.TicksBelow);
    self.opening_pressure.setTickInterval(1);
    self.opening_pressure.valueChanged.connect(self.showPressure); 
  
    # Pressure Label Text
    self.pressure_label= QLabel("");
    self.pressure_label.setFont(QFont("Times", 30)); 

    # Tick Labels
    self.startTick = QLabel(str(-5));
    self.startTick.setFont(QFont("Times", 24));
    self.endTick = QLabel(str(20));
    
    self.endTick.setFont(QFont("Times", 24));
    # Pressure Enter Button
    self.pressure_enter = QPushButton("Enter");
    self.pressure_enter.setFont(QFont("Times",34));
    self.pressure_enter.clicked.connect(self.setOpenPressure);
   

# ALL OPENING DELAY STUFF 
    self.openDelayLabel = QLabel("What is the Opening Delay?");
    self.openDelayLabel.setFont(QFont("Times", 40));
    
    self.openDelaySlider = QSlider(Qt.Horizontal);
    self.openDelaySlider.setMinimum(0);
    self.openDelaySlider.setMaximum(5000);
    self.openDelaySlider.setTickPosition(QSlider.TicksBelow);
    self.openDelaySlider.setTickInterval(500);
    self.openDelaySlider.setSingleStep(150);   
    self.openDelaySlider.valueChanged.connect(self.showOpenDelay);
 
    self.openDelay = QLabel("");
    self.openDelay.setFont(QFont("Times", 30));
    
    # Tick Labels
    self.openTick = QLabel(str(0) + "ms");
    self.closeTick = QLabel(str(5000) + "ms");
    self.openTick.setFont(QFont("Times", 24));
    self.closeTick.setFont(QFont("Times", 24));

    # Open Delay Enter Button
    self.openDelayEnter = QPushButton("Enter");
    self.openDelayEnter.setFont(QFont("Times", 34));
    self.openDelayEnter.clicked.connect(self.saveOpenDelay);    

    # Closing Pressure Prompts 
    self.closingLabel = QLabel("Would you like to Enter a Closing Delay?");
    self.closingLabel.setFont(QFont("Times", 35));

    self.Yes = QPushButton("Yes");
    self.Yes.setFont(QFont("Times", 30));
    self.Yes.clicked.connect(self.closingDelay);
  
    self.No = QPushButton("No");
    self.No.setFont(QFont("Times", 30));
    self.No.clicked.connect(self.pressure_summary1);

    

    # Grid placement
    self.grid.addWidget(self.drainType, 0,2,2,4);
    self.grid.addWidget(self.pressure, 5, 0, 2,3);
    self.grid.addWidget(self.volume, 5,3,2,3);
    self.grid.addWidget(self.clamped,5,6,2,3);

    self.setLayout(self.grid)

  def Clamped(self):
    
    self.drainType.setVisible(False);
    self.pressure.setVisible(False);
    self.volume.setVisible(False);
    self.clamped.setVisible(False);
    
    self.clampedLabel = QLabel("How long would you like to clamp the drain?");
    self.clampedLabel.setFont(QFont("Times", 36));
    
    self.clampedSlider = QSlider(Qt.Horizontal);
    self.clampedSlider.setMinimum(0);
    self.clampedSlider.setMaximum(60);
    self.clampedSlider.setTickPosition(QSlider.TicksBelow);
    self.clampedSlider.setTickInterval(1);
    self.clampedSlider.valueChanged.connect(self.showTime);
      
    self.timeClamped = QLabel("");
    self.timeClamped.setFont(QFont("Times", 30));
    
    self.timeMin = QLabel(str(0));
    self.timeMax = QLabel(str(60));
    self.timeMin.setFont(QFont("Times", 28));
    self.timeMax.setFont(QFont("Times", 28));
    
    self.unlimitedTime = QPushButton("Unlimited");
    self.unlimitedTime.setFont(QFont("Times", 27));
    self.unlimitedTime.clicked.connect(self.setUnlimitedTime);
    
    self.enterTime = QPushButton("Enter");
    self.enterTime.setFont(QFont("Times", 28));
    self.enterTime.clicked.connect(self.EnterTime);

    self.grid.addWidget(self.clampedLabel, 0, 2, 2, 5);
    self.grid.addWidget(self.clampedSlider, 4,2,2,5);
    self.grid.addWidget(self.enterTime, 6,3,3,3);
    self.grid.addWidget(self.timeMin, 3,2);
    self.grid.addWidget(self.timeMax, 3,7);
    self.grid.addWidget(self.timeClamped, 3,4,2,5);
    self.grid.addWidget(self.unlimitedTime, 4,3,3,3);
  def clampSummary(self):
    self.clampedLabel.setVisible(False);
    self.clampedSlider.setVisible(False);
    self.enterTime.setVisible(False);
    self.timeMin.setVisible(False);
    self.timeMax.setVisible(False);
    self.timeClamped.setVisible(False);
    self.unlimitedTime.setVisible(False);

    self.controllingSummary3 = QLabel("Controlling Summary");
    self.controllingSummary3.setStyleSheet("bordeR: 1px solid black;");
    self.controllingSummary3.setFont(QFont("Times", 38));  
    
    self.control1 = QLabel("Clamped for Pressure Monitoring");
    self.control1.setFont(QFont("Times", 24));
    
    duration = None;
    if unlimitTime == True:
      duration = "Unlimited"
    else:
      duration = str(clampTime)
    
    self.target_clamp = QLabel("Clamp For: " + duration + " minutes");
    self.target_clamp.setFont(QFont("Times", 24));
    
    self.home2 = QPushButton("Home");
    self.home2.setFont(QFont("Times", 24));
    self.home2.clicked.connect(self.backhome);
  
    self.grid.addWidget(self.controllingSummary3, 0,2,3,5);
    self.grid.addWidget(self.control1, 3,2,3,5);
    self.grid.addWidget(self.target_clamp,4,2,3,5)
    self.grid.addWidget(self.home2, 7,2,3,5)
    
  def showTime(self):
    self.timeClamped.setText(str(self.clampedSlider.value()) + " minutes");
  def setUnlimitedTime(self):
    global unlimitTime;
    unlimitTime = True;
  def EnterTime(self):
    global clampTime;
    if unlimitTime == False:
      clampTime = self.clampedSlider.value();
    self.clampSummary();
  def VolumeScreen(self):
    self.drainType.setVisible(False);
    self.pressure.setVisible(False);
    self.volume.setVisible(False);
    self.clamped.setVisible(False);
    
    # Make the labels we need now 
    self.volumeLabel = QLabel("What is the amount to be drained in 1 hour?");
    self.volumeLabel.setFont(QFont("Times", 36));
    
    self.volumeSlider = QSlider(Qt.Horizontal);
    self.volumeSlider.setMinimum(0);
    self.volumeSlider.setMaximum(50);
    self.volumeSlider.setTickPosition(QSlider.TicksBelow);
    self.volumeSlider.setTickInterval(1);
    self.volumeSlider.valueChanged.connect(self.showVolume);
  
    self.VFR = QLabel("");
    self.VFR.setFont(QFont("Times", 30));
    
    self.volMin = QLabel(str(0));
    self.volMax = QLabel(str(50));
    self.volMin.setFont(QFont("Times", 28));
    self.volMax.setFont(QFont("Times", 28));
    
    self.unlimited = QPushButton("Unlimited Flow");
    self.unlimited.setFont(QFont("Times", 27));
    self.unlimited.clicked.connect(self.unlimitedCheck);

    self.enterVolume = QPushButton("Enter");
    self.enterVolume.setFont(QFont("Times", 28)); 
    self.enterVolume.clicked.connect(self.enterVol);
    
    self.grid.addWidget(self.volumeLabel, 0,2,2,5);
    self.grid.addWidget(self.volumeSlider,4,2,2,5);
    self.grid.addWidget(self.enterVolume, 6,3,3,3);
    self.grid.addWidget(self.volMin, 3,2);
    self.grid.addWidget(self.volMax, 3,7);
    self.grid.addWidget(self.VFR, 3,4,2,5);
    self.grid.addWidget(self.unlimited, 4,3,3,3)    
  def enterVol(self):
    global VolumeFlowRate
    if unlimit == False:
      VolumeFlowRate = self.volumeSlider.value();
    self.volume_summary();

  def unlimitedCheck(self):
    global unlimit;
    unlimit = True;

  def volume_summary(self):
    self.volumeLabel.setVisible(False); 
    self.volumeSlider.setVisible(False);
    self.enterVolume.setVisible(False)
    self.volMin.setVisible(False);
    self.volMax.setVisible(False);
    self.VFR.setVisible(False);
    self.unlimited.setVisible(False);


    self.controllingSummary2 = QLabel("Controlling Summary");
    self.controllingSummary2.setStyleSheet("bordeR: 1px solid black;");
    self.controllingSummary2.setFont(QFont("Times", 38));  
    
    self.control = QLabel("Control by volume drained per hour");
    self.control.setFont(QFont("Times", 24));
    
    drainage = None;
    if unlimit == True:
      drainage = "Unlimited"
    else:
      drainage = str(VolumeFlowRate)
    
    self.target_Drain = QLabel("Target Drainage: " + drainage + " mL/hr");
    self.target_Drain.setFont(QFont("Times", 24));
    
    self.home2 = QPushButton("Home");
    self.home2.setFont(QFont("Times", 24));
    self.home2.clicked.connect(self.backhome);
  
    self.grid.addWidget(self.controllingSummary2, 0,2,3,5);
    self.grid.addWidget(self.control, 3,2,3,5);
    self.grid.addWidget(self.target_Drain,4,2,3,5)
    self.grid.addWidget(self.home2, 7,2,3,5)


  def showVolume(self):
    self.VFR.setText(str(self.volumeSlider.value()) + "mL");
  def showOpenDelay(self):
    self.openDelay.setText(str(self.openDelaySlider.value()) + "ms"); 
  # Set the cmHg Flag
  def setcmHg(self):
    global cmHg;
    cmHg = 1;
    self.drainType.setVisible(False);
    self.cmHg.setVisible(False);
    self.mmHg.setVisible(False);  
    self.open_pressure();
    

  # Set the mmHg Flag
  def setmmHg(self):
    global mmHg;
    mmHg = 1;
    self.drainType.setVisible(False);
    self.cmHg.setVisible(False);
    self.mmHg.setVisible(False);  
    
    self.open_pressure();

  def showPressure(self):
    txt = None;
    if cmHg == 1:
      txt = " cm Hg"
    else:
      txt = " mm Hg"
    self.pressure_label.setText(str(self.opening_pressure.value()) + txt); 

  def units(self):
    self.pressure.setVisible(False);
    self.volume.setVisible(False);
    self.clamped.setVisible(False);   

    self.grid.addWidget(self.cmHg,5,0,2,3);
    self.grid.addWidget(self.mmHg,5,6,2,3);
  
  def open_pressure(self):
    self.grid.addWidget(self.opening_label, 0,2,2,5);
    self.grid.addWidget(self.pressure_label, 4,4,2,4);
    self.grid.addWidget(self.opening_pressure, 3,2,2,5);
    self.grid.addWidget(self.pressure_enter, 6,3,3,3);
    self.grid.addWidget(self.startTick, 3,2);
    self.grid.addWidget(self.endTick, 3,7)    
  def setOpenPressure(self):
  
    global openPressure;
    openPressure = self.opening_pressure.value();
   
    self.opening_label.setVisible(False);
    self.pressure_label.setVisible(False);
    self.opening_pressure.setVisible(False);
    self.pressure_enter.setVisible(False);
    self.startTick.setVisible(False);
    self.endTick.setVisible(False);

    self.grid.addWidget(self.openDelayLabel, 0,2,2,5);
    self.grid.addWidget(self.openDelaySlider, 4,2,2,5);
    self.grid.addWidget(self.openDelayEnter, 6,3,3,3);
    self.grid.addWidget(self.openDelay,3,4,2,5);
    self.grid.addWidget(self.openTick, 3,2);
    self.grid.addWidget(self.closeTick,3,7);
  def saveOpenDelay(self):
    # saving opening delay
    global openDelay;
    openDelay = self.openDelaySlider.value();
    
    # making all dissapear
    self.openDelayLabel.setVisible(False);
    self.openDelaySlider.setVisible(False);
    self.openDelayEnter.setVisible(False);
    self.openDelay.setVisible(False);
    self.openTick.setVisible(False);
    self.closeTick.setVisible(False);
  
    # need to load the prompt for closing delay
    self.grid.addWidget(self.closingLabel, 0,3,2,5);  
    self.grid.addWidget(self.Yes, 4,0,2,4);
    self.grid.addWidget(self.No, 4,6,2,4);
  def closingDelay(self):
    self.closingLabel.setVisible(False);
    self.Yes.setVisible(False);
    self.No.setVisible(False);
    # Closing Pressure
    self.closingPrompt = QLabel("What is the closing pressure?");
    self.closingPrompt.setFont(QFont("Times", 38));


    self.closingSlider = QSlider(Qt.Horizontal);
    self.closingSlider.setMinimum(0);
    self.closingSlider.setMaximum(openPressure);
    self.closingSlider.setTickPosition(QSlider.TicksBelow);
    self.closingSlider.setTickInterval(1);  
    self.closingSlider.valueChanged.connect(self.showClosingPressure);
    
    self.closingPressure = QLabel("");
    self.closingPressure.setFont(QFont("Times", 30));

    self.closeTickMin = QLabel(str(0));
    self.closeTickMax = QLabel(str(openPressure));
    self.closeTickMin.setFont(QFont("Times", 28));
    self.closeTickMax.setFont(QFont("Times", 28));
    self.confirmClosePressure = QPushButton("Enter");
    self.confirmClosePressure.setFont(QFont("Times", 35));
    self.confirmClosePressure.clicked.connect(self.pressure_summary2);
    self.grid.addWidget(self.closingPrompt, 0,2,2,5);
    self.grid.addWidget(self.closingSlider, 4,2,2,5);
    self.grid.addWidget(self.confirmClosePressure, 6,3,3,3);
    self.grid.addWidget(self.closeTickMin, 3,2);
    self.grid.addWidget(self.closeTickMax,3,7);
    self.grid.addWidget(self.closingPressure, 3,4,2,5);      
  def showClosingPressure(self):
    txt = None;
    if cmHg == 1:
      txt = " cm Hg"
    else:
      txt = " mm Hg"
    self.closingPressure.setText(str(self.closingSlider.value()) + txt); 
  
  def pressure_summary1(self):    
    
    self.closingLabel.setVisible(False);
    self.Yes.setVisible(False);
    self.No.setVisible(False);
    
    self.controllingSummary = QLabel("Controlling Summary");
    self.controllingSummary.setStyleSheet("bordeR: 1px solid black;");
    self.controllingSummary.setFont(QFont("Times", 38));  
    
    self.driveBy = QLabel("Drive by: Pressure");
    self.driveBy.setFont(QFont("Times", 24));
  
    if cmHg == 1:
      txt = " cm Hg"
    else:
      txt = " mm Hg"
    
    self.open_label = QLabel("Opening Pressure: " + str(openPressure) + txt);
    self.open_label.setFont(QFont("Times", 24)); 
    
    self.open_delay = QLabel("Opening Delay: " + str(openDelay) + " ms.");
    self.open_delay.setFont(QFont("Times", 24));
      
    self.home = QPushButton("Home");
    self.home.setFont(QFont("Times", 24));
    self.home.clicked.connect(self.backhome);
    
    self.grid.addWidget(self.controllingSummary, 0,2,2,5);
    self.grid.addWidget(self.driveBy, 2,3,2,5); 
    self.grid.addWidget(self.open_label, 4,3,2,5);
    self.grid.addWidget(self.open_delay,6,3,2,5);
    self.grid.addWidget(self.home,8,2,2,5);
    
  def backhome(self):
    global selection_windows;
    selection_windows -=1;
    self.close();

  def pressure_summary2(self):
    global closePressure
    closePressure = self.closingSlider.value();
        
    self.closingPrompt.setVisible(False); 
    self.closingSlider.setVisible(False);
    self.confirmClosePressure.setVisible(False);
    self.closeTickMin.setVisible(False);
    self.closeTickMax.setVisible(False);
    self.closingPressure.setVisible(False); 
    self.controllingSummary1 = QLabel("Controlling Summary");
    self.controllingSummary1.setStyleSheet("bordeR: 1px solid black;");
    self.controllingSummary1.setFont(QFont("Times", 38));  
    
    self.driveBy1 = QLabel("Drive by: Pressure");
    self.driveBy1.setFont(QFont("Times", 24));
  
    if cmHg == 1:
      txt = " cm Hg"
    else:
      txt = " mm Hg"
    
    self.open_label1 = QLabel("Opening Pressure: " + str(openPressure) + txt);
    self.open_label1.setFont(QFont("Times", 24)); 
    
    self.close_label = QLabel("Closing Pressure: " + str(closePressure) + txt);
    self.close_label.setFont(QFont("Times", 24)); 
    
    
    self.open_delay1 = QLabel("Opening Delay: " + str(openDelay) + " ms.");
    self.open_delay1.setFont(QFont("Times", 24));
      
    self.home1 = QPushButton("Home");
    self.home1.setFont(QFont("Times", 24));
    self.home1.clicked.connect(self.backhome);
    
    self.grid.addWidget(self.controllingSummary1, 0,2,2,5);
    self.grid.addWidget(self.driveBy1, 2,3,2,5); 
    self.grid.addWidget(self.open_label1, 4,3,2,5);
    self.grid.addWidget(self.close_label, 5,3,2,5);
    self.grid.addWidget(self.open_delay1,6,3,2,5);
    self.grid.addWidget(self.home1,8,2,2,5);

class Calibration(QWidget):

  global strain_gauge;
  global pressure_transducer;

  def __init__(self):
    super().__init__();
  
    # Set dimensions of the window 
    self.setFixedWidth(800);
    self.setFixedHeight(480);
    


    # Make the window not closable 
    self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint);
    self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint);

    
    # Create the local grid layout
    self.grid = QGridLayout();
    for i in range(0,9):
      for j in range(0,9):
        self.grid.addWidget(QLabel(""), i,j);
    
    # Adds the the type of label to the main screen   
    self.sensor_type = QLabel("How are you measuring ICP?");
    self.sensor_type.setFont(QFont("Times", 36));
    self.sensor_type.setWordWrap(True);    
    self.sensor_type.setAlignment(Qt.AlignCenter);
    # Add the two button types to the main screen
    self.pressure_transducer = QPushButton("Pressure Transducer");
    self.pressure_transducer.setFont(QFont("Times", 24))
    self.strain_gauge = QPushButton("Strain Gauge");
    self.strain_gauge.setFont(QFont("Times", 24))
    
    # Checking Transducer Open to the Air
    self.openAir = QLabel("Confirm the transducer is open to air");
    self.openAir.setFont(QFont("Times", 24));
    self.openAir.setStyleSheet("bordeR: 1px solid black;");
    

    # Confirmation Button
    self.confirmAir = QPushButton("Confirm");
    self.confirmAir.setFont(QFont("Times", 24));
    self.confirmAir.clicked.connect(self.confirmCalibration);
    
    # Back Button 
  
    self.backButton = QPushButton("Back");
    self.backButton.setFont(QFont("Times", 24));
    self.backButton.clicked.connect(self.back);

    
    # Zeroing Label
    self.zeroLabel = QLabel("Press Button to Zero Device");
    self.zeroLabel.setFont(QFont("Times", 24));
    

    # Zero Button 
    self.zeroButton = QPushButton("Zero");
    self.zeroButton.setFont(QFont("Times", 24));
    self.zeroButton.clicked.connect(self.zeroDevice)
    self.zeroButton.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding);
    #self.zeroButton.resize(500,500);
    
    # Sucess Label
    self.works = QLabel("Calibration Successful");
    self.works.setFont(QFont("Times", 24));

    # Return Home
    self.home_button = QPushButton("Return to Home");
    self.home_button.setFont(QFont("Times", 24));
    self.home_button.clicked.connect(self.exit);
    self.home_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding);
    # Connecting buttons to correct methods

    self.pressure_transducer.clicked.connect(self.setPressureTransducer);
    self.strain_gauge.clicked.connect(self.setStrainGauge);    



    # Adding the correct buttons widgets to the grid 
    self.grid.addWidget(self.sensor_type, 0,3,2,3);
    self.grid.addWidget(self.pressure_transducer, 5, 0,2,3);
    self.grid.addWidget(self.strain_gauge, 5,7, 2, 2);
    
    self.setLayout(self.grid);


  # To confirmation screen 
  def setPressureTransducer(self):
    print("Reached");
    # Change the global fields to tell how we are measuring ICP
    global strain_gauge;
    global pressure_transducer;
    strain_gauge = 0;
    pressure_transducer = 1;

    # Hide all of the assests that were involved in the previous step
    self.pressure_transducer.setVisible(False);
    self.strain_gauge.setVisible(False);
    self.sensor_type.setVisible(False);


    # Make the buttons open again
    self.grid.addWidget(self.openAir, 0,3, 2, 3);
    self.grid.addWidget(self.confirmAir,5,7,2,2);
    self.grid.addWidget(self.backButton, 5,0,2,3);

    
  def exit(self):
    global zero_windows;
    zero_windows -=1;
    self.close();
  
  
  def back(self):

    # Hide all of the assests that were involved in the previous step
    self.pressure_transducer.setVisible(True);
    self.strain_gauge.setVisible(True);
    self.sensor_type.setVisible(True);
    
    self.grid.addWidget(self.sensor_type, 0,3,2,3);
    self.grid.addWidget(self.pressure_transducer, 5, 0,2,3);
    self.grid.addWidget(self.strain_gauge, 5,7, 2, 2);
   
     # Make current widgets close
    self.openAir.setVisible(False);
    self.confirmAir.setVisible(False);
    self.backButton.setVisible(False);

    
    # Reconnect the two buttons to signals
    self.pressure_transducer.clicked.connect(self.setPressureTransducer);
    self.strain_gauge.clicked.connect(self.setStrainGauge);    

  # Return back to the home menu (Welcome Screen);
  def setStrainGauge(self):
    global zero_windows;
    global strain_gauge;
    global pressure_transducer;
    
    # Decrement number of calibration windows we have open 
    zero_windows -=1;    
    print(zero_windows)
    # Set other fields as needed
    pressure_transducer = 0;
    strain_gauge = 1; 
    
    self.close();
  def confirmCalibration(self):
        # Make current widgets close
    self.openAir.setVisible(False);
    self.confirmAir.setVisible(False);
    self.backButton.setVisible(False);
    
    self.grid.addWidget(self.zeroLabel, 0,3,2,6);
    self.grid.addWidget(self.zeroButton, 5,2,2,5);
  def zeroDevice(self):
    global zero_pressure;
    temp = 0;
    for i in range(5):
      temp += random.randint(1,10);
      time.sleep(1);      
    zero_pressure = temp/5.0;

    self.zeroButton.setVisible(False);
    self.zeroLabel.setVisible(False);
    self.grid.addWidget(self.works, 0,3,2,5);
    self.grid.addWidget(self.home_button, 5,3,2,3);    
class newWindow(QWidget): 
  def __init__(self):
    super().__init__();
    layout = QVBoxLayout();
    self.label = QLabel("Another Window");
    layout.addWidget(self.label);
    self.setLayout(layout);
    



class WelcomeWindow(QWidget):
  global pressure_transducer;
  global strain_gauge;
  def __init__(self):
    super().__init__();

    grid = QGridLayout();
    
    for i in range(0,8):
      for j in range(0,9):
        grid.addWidget(QLabel(""), i , j );

    # Welcome Label
    welcome_label = QLabel("Welcome to the FlowMo");
#    welcome_label.setStyleSheet("background-color: blue");
    welcome_label.setFont(QFont("Times", 28));
    welcome_label.setAlignment(Qt.AlignCenter)

    # Home Screen Label    
    homebutton = QLabel(self);
    pixmap = QPixmap("homebutton.png");
    homebutton.setPixmap(pixmap);
    homebutton.show();
    
    
    # Brightness Button (need to modify still to work properly)
    brightness = QPushButton("Brightness");
    brightness.setGeometry(100,100,100,100);
    brightness.setStyleSheet("background-color: green");
    brightness.setFont(QFont("Times", 24));
     
    # ZEROING BUTTON
    self.ZeroWindow = None;
    zeoring_button = QPushButton("Sensor Zeroing");
    zeoring_button.setFont(QFont("Times", 24)); 
    zeoring_button.clicked.connect(self.Calibration);

    # SELECTION BUTTON
    self.selectionWindow = None;
    selection = QPushButton("Operational Drain Settings");
    selection.setFont(QFont("Times", 24));
    selection.clicked.connect(self.select);
     
    # ALARMS BUTTON 
    alarms = QPushButton("Alarm Settings");
    alarms.setFont(QFont("Times", 24));
   

    # RUNNING BUTTON
    run = QPushButton("Run");
    run.setFont(QFont("Times", 24));
    run.clicked.connect(self.testing_values);

    # Set the layout properly
    grid.addWidget(welcome_label, 0,3);
    grid.addWidget(homebutton, 0, 0);
    grid.addWidget(brightness, 0,7);
    grid.addWidget(zeoring_button, 1,3)
    grid.addWidget(selection, 3,3);
    grid.addWidget(alarms, 5,3);
    grid.addWidget(run, 7,3);

    # Set the actual background :)
    self.setLayout(grid);
  def select(self):
    global selection_windows;
    if self.selectionWindow is None or selection_windows == 0:
      self.selectionWindow = Selection();
      selection_windows +=1;
      self.selectionWindow.show();     


  def Calibration(self):
    global zero_windows; 

    if self.ZeroWindow is None or zero_windows == 0:
      self.ZeroWindow = Calibration();
      zero_windows +=1;
      self.ZeroWindow.show();
    print(zero_windows);   
  def testing_values(self):
    print(strain_gauge);
    print(zero_pressure);
    

class MainWindow(QMainWindow):
  def __init__(self):

    super(MainWindow, self).__init__()
    self.setWindowTitle("My App");
    self.setFixedWidth(800);
    self.setFixedHeight(480);
  
    w = WelcomeWindow();
    self.setCentralWidget(w);

app = QApplication(sys.argv);
w = MainWindow();
w.show();
app.exec();








