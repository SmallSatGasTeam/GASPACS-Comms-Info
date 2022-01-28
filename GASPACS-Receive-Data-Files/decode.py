'''
This program is intented to decode images and telemetry data from the GASPACS CubeSat.
Please see https://smallsatgasteam.github.io/GASPACS-Comms-Info/ for information on using the program
'''
'''Note: The picture processing operates under the assumption that a single txt file will only contain data from one Picture ID'''
#Take raw data file, separate into different packets
import binascii
import os
import struct
import shutil
import subprocess
from datetime import datetime
from time import sleep
import logging


class decodeData():
  def __init__(self):
    self.previousFolderNum = 999 #this is an initial placeholder number that could not occur. Picture numbers only go up to 255
    #Make a list containing all of the old packets
    self.packetList = ['0'] * 30000
    self.binFilePath = ""
    self.newFileFolder = './new/'
    self.oldFileFolder = './old/'
    self.csvFilePath = './allData.csv'
    self.backupCsvFilePath = './backupAllData.csv'
    self.pictureFolder = './Pictures/'
    # Set up logging

    # Set up logging
    self.logger = logging.getLogger("decode")
    # Set initial level - anything below this level will not be passed to the handlers.
    self.logger.setLevel(logging.DEBUG)

    # Set formatting
    self.formatter = logging.Formatter('%(asctime)s %(message)s')

    # Log to console:
    self.consoleHandler = logging.StreamHandler()
    self.consoleHandler.setLevel(logging.DEBUG)
    self.consoleHandler.setFormatter(self.formatter)
    self.logger.addHandler(self.consoleHandler)


  def processData(self):
      # This loads raw data files from a folder in a loop and saves the data into a variable.
      #self.logger.info(self.newFileFolder)
      for filename in sorted(os.listdir(self.newFileFolder)):

        # Path to file in "new" folder
        newFilePath = os.path.join(self.newFileFolder, filename)
        # Path to file in "old" folder
        oldFilePath = os.path.join(self.oldFileFolder, filename)

        if filename.endswith('.txt'):
            with open(newFilePath) as f:
                # Read each raw data file into a variable
                rawDataFile = f.read().lower().replace(" ", "")
                self.logger.debug("Raw Data: " + str(rawDataFile))
                # Get list of potentially valid packets (everything between two sync bytes)
                potentialGASPackets, potentialSSDVPackets = self.separatePackets(rawDataFile)
                #self.logger.debug("Potential GAS Packets: " + str(potentialGASPackets))
                self.logger.debug("Potential SSDV Packets: " + str(potentialSSDVPackets))
                validGASPackets = self.validateGASPackets(potentialGASPackets)
                self.logger.info("Valid GAS Packets: " + str(validGASPackets))
                # Next, call decode GAS data, pass in validGASPackets
                self.decodeGASPackets(validGASPackets)

                validSSDVPackets = self.validateSSDVPackets(potentialSSDVPackets)
                self.logger.info("Valid SSDV Packets: " + str(validSSDVPackets))

                #for picturePacket in validSSDVPackets:
                #  self.processPicture(picturePacket)

                if len(validSSDVPackets) > 0:
                  self.processPicture(validSSDVPackets)
                  self.writePicture()

            # Copy file from "new" folder to "old" folder, and remove it from the "new" folder
            shutil.copy(newFilePath, oldFilePath)
            os.remove(newFilePath)

            #copy allData to a backup file
            shutil.copy(self.csvFilePath, self.backupCsvFilePath)

      
  # Takes the raw data and splits it into potential packets based on GASPACS header or SSDV header
  def separatePackets(self,rawDataFile):
      # GASPACS Header
      gaspacsHex = str(b'GASPACS'.hex())
      # SSDV Header
      SSDVHex = '556604f02a5b'

      potentialGASPackets=[]
      # Finds all occurences of GASPACS hex in the data
      occurencesOfGASPACS = self.findOccurences(rawDataFile, gaspacsHex)
      # Returns list of data between every pair of GASPACS occurences
      for i in range(len(occurencesOfGASPACS)-1):
          potentialGASPackets.append(rawDataFile[occurencesOfGASPACS[i]+14:occurencesOfGASPACS[i+1]])

      potentialSSDVPackets = []
      occurencesOfSSDV = self.findOccurences(rawDataFile,SSDVHex)

      # Returns list of data after every SSDV Header occurences
      for i in range(len(occurencesOfSSDV)):
          potentialSSDVPackets.append(rawDataFile[occurencesOfSSDV[i]:occurencesOfSSDV[i]+256])

      return potentialGASPackets, potentialSSDVPackets

  #Finds all occurences of syncByte in dataToParse, returns a list of all the indices where syncByte appeared
  def findOccurences(self,dataToParse, syncByte): 
    occurenceList = []
    minIndex = 0
    while True:
      foundIndex = dataToParse.find(syncByte, minIndex)
      if(foundIndex != -1):
        minIndex = foundIndex + 1
        occurenceList.append(foundIndex)
      else:
        break
    return occurenceList

  # This validates the packets based on their data type (which is stored in each packet) and the correct length for each data type.
  def validateGASPackets(self,potentialGASPackets):
    validGASPackets = []
    for packet in potentialGASPackets:
      #self.logger.debug("packet length: " + str(len(packet)))
      if (packet[0:2] == '00') and (len(packet) == 74): #Attitude Data
        #self.logger.debug("Valid Attitude data: " + str(packet))
        validGASPackets.append(packet)
      elif (packet[0:2] == '01') and (len(packet) == 184): # TTNC Data
        #self.logger.debug("Valid TTNC data: " + str(packet))
        validGASPackets.append(packet)
      elif (packet[0:2] == '02') and (len(packet) == 50): # Deploy Data
        #self.logger.debug("Valid TTNC data: " + str(packet))
        validGASPackets.append(packet)

    return validGASPackets

  # This checks to see if there is another occurence of the SSDV header inside of the packet.
  # If there is another occurence, it prints out the flagged packet, but keeps it to try and process it.
  def validateSSDVPackets(self,potentialSSDVPackets):
    validSSDVPackets = []
    SSDVHex = '556604f02a5b'

    for packet in potentialSSDVPackets:
      validSSDVPackets.append(packet)
      occurenceInSSDVPacket = self.findOccurences(packet[12:-1],SSDVHex)
      if len(occurenceInSSDVPacket) > 0:
        self.logger.info("FLAG! Found SSDV Header inside of SSDV Packet: " + str(packet))

    return validSSDVPackets


  # Takes the validGASPackets list, iterates through, and appends decoded data to .csv file
  def decodeGASPackets(self, validGASPackets):
    csvFile = open(self.csvFilePath, 'a+')
    for data in validGASPackets:
      #data is a string of hex bytes
      #Decode data, store raw data and decoded data in a file
      packetType = data[0:2]
      dataContent = []
      if packetType == '00': #Attitude Data
        dataContent.append(0) #Datatype 0
        dataContent.append(self.intFromHex(data[2:10])) #Timestamp, int 4
        dataContent.append(self.floatFromHex(data[10:18])) #Sun-Sensor 1, float 4
        dataContent.append(self.floatFromHex(data[18:26])) #Sun-Sensor 2, float 4
        dataContent.append(self.floatFromHex(data[26:34])) #Sun-Sensor 3, float 4
        dataContent.append(self.floatFromHex(data[34:42])) #Sun-Sensor 4, float 4
        dataContent.append(self.floatFromHex(data[42:50])) #Sun-Sensor 5, float 4
        dataContent.append(self.floatFromHex(data[50:58])) #Magnetic field x, float 4
        dataContent.append(self.floatFromHex(data[58:66])) #Magnetic field y, float 4
        dataContent.append(self.floatFromHex(data[66:74])) #Magnetic field z, float 4
      elif packetType == '01': #TT&C Data
        dataContent.append(1) #Datatype 1
        dataContent.append(self.intFromHex(data[2:10])) #Timestamp, int 4
        dataContent.append(self.intFromHex(data[10:12])) #Mission mode, int 1
        dataContent.append(self.intFromHex(data[12:16])) #Reboot count, int 2
        dataContent.append(self.floatFromHex(data[16:24])) #Boombox uv, float 4
        dataContent.append(self.floatFromHex(data[24:32])) #SPX+ temp, float 4
        dataContent.append(self.floatFromHex(data[32:40])) #SPZ+ temp, float 4
        dataContent.append(self.floatFromHex(data[40:48])) #CPU temp, float 4
        dataContent.append(self.floatFromHex(data[48:56])) #EPS MCU temp, float 4
        dataContent.append(self.floatFromHex(data[56:64])) #Cell 1 battery temp, float 4
        dataContent.append(self.floatFromHex(data[64:72])) #Cell 2 battery temp, float 4
        dataContent.append(self.floatFromHex(data[72:80])) #Battery voltage, float 4
        dataContent.append(self.floatFromHex(data[80:88])) #Battery current, float 4
        dataContent.append(self.floatFromHex(data[88:96])) #BCR voltage, float 4
        dataContent.append(self.floatFromHex(data[96:104])) #BCR current, float 4
        dataContent.append(self.floatFromHex(data[104:112])) #EPS 3v3 current, float 4
        dataContent.append(self.floatFromHex(data[112:120])) #EPS 5v current, float 4
        dataContent.append(self.floatFromHex(data[120:128])) #SPX voltage, float 4
        dataContent.append(self.floatFromHex(data[128:136])) #SPX+ current, float 4
        dataContent.append(self.floatFromHex(data[136:144])) #SPX- current, float 4
        dataContent.append(self.floatFromHex(data[144:152])) #SPY voltage, float 4
        dataContent.append(self.floatFromHex(data[152:160])) #SPY+ current, float 4
        dataContent.append(self.floatFromHex(data[160:168])) #SPY- current, float 4
        dataContent.append(self.floatFromHex(data[168:176])) #SPZ voltage, float 4
        dataContent.append(self.floatFromHex(data[176:184])) #SPZ+ current, float 4
      elif packetType == '02': #Deployment Data
        dataContent.append(2) #Datatype 2
        dataContent.append(self.intFromHex(data[2:18])) #Timestamp in ms, int 8
        dataContent.append(self.floatFromHex(data[18:26])) #Boombox UV, float 4
        dataContent.append(self.floatFromHex(data[26:34])) #Acceleration x, float 4
        dataContent.append(self.floatFromHex(data[34:42])) #Acceleration y, float 4
        dataContent.append(self.floatFromHex(data[42:50])) #Acceleration z, float 4

      csvFile.write(str(dataContent)[1:-1] + '\n')
      
      #self.logger.debug(str(dataContent)[1:-1] + '\n')
      
    csvFile.close()

  def processPicture(self, validSSDVPackets):
    """This function is currently built to be passed a packet of a picture. If this is the first time it is passed a packet, it will 
    check the picture number and create the folder to hold the picture (if it doesn't already exist). Then, a list to hold the incoming 
    packets is created. If there is an old .bin file of the same picture, it will be read and its packets will be put into the list at 
    the correct indexes. The new packet will then be put into the list at the correct index. If there is no .bin file to be read, the
    .bin read process will be skipped and the packet that was passed in will be written to the list at its correct index. Allsubsequent 
    packets will be written into the list as long as their picture number matches the current picture number."""
    
    #folder number is the same as the picture number
    try:
      #hexFolderNum = hex(int(picturePacket[12:14], 16))
      hexFolderNum = hex(int(validSSDVPackets[0][12:14], 16))
    except:
      hexFolderNum = hex(999)

    self.folderNum = int(hexFolderNum, 16)
    #self.logger.debug("folderNum: " + str(folderNum))

    self.pictureIDFolder = self.pictureFolder + str(self.folderNum) + '/'

    previousBin = False
    
    self.binFilePath = self.pictureIDFolder + "pictureData" + str(self.folderNum) + ".bin"

    #if self.folderNum != self.previousFolderNum:

    #self.writePicture()
    os.makedirs(self.pictureIDFolder, exist_ok=True) #Create picture number based on Image ID from compression, bits 12 and 13

    #Try to pull in an old existing .bin file for the same picture.

    try:
      binFile = open(self.binFilePath, 'rb')
      previousBin = True
    except:
      self.logger.info("Failed to open .bin file")
      previousBin = False
      #If there is no bin file to read, we do not want to try and make an list out of a file that doesn't exist. We just want to start adding packets to packetList.
    if previousBin:
      try:
        size = os.path.getsize(self.binFilePath)
      except:
        self.logger.info("Failed to get size of .bin file")
        size = 0
      currentByte = 0
      while currentByte < size: #Read complete packets until EOF
        #Read the bin file and assign it as the current packet
        currentPacket = ""
        try:
          currentPacket = binascii.hexlify(binFile.read(128))
        except:
          self.logger.info("Failed to read something in the bin file")
          
        #If the line in the .bin file was blank, continue to the next thing in the .bin file.
        if currentPacket == "":
          continue
        else:
          try:
            #The .bin file packet is converted into a usable hex packet
            strCurrentPacket = str(currentPacket)
            #self.logger.debug("This is strCurrent:", strCurrentPacket)
            stripped = strCurrentPacket[2:-1]
            #self.logger.debug("This is stripped:", stripped)
            
            #This finds the packet number and then puts the packet at the corresponding index in the list
            x = stripped[14:18]
            if x == "0000":
              num = 0
            else:
              num = int(x.lstrip("0"), 16)
          except:
            self.logger.info("Failed to convert packet into usable format")
          #self.logger.debug("This is num:", num)
          try:
            self.packetList[num] = stripped
          except:
            self.logger.info("Failed to add packet to list of packets")
          try:
            currentByte += 128
            continue
          except:
            self.logger.info("Failed to increment currentByte and continue")
      binFile.close()
    #This is the end of pulling in the old packets from the .bin file
  
    #self.binFilePath = self.pictureIDFolder + "pictureData" + str(self.folderNum) + ".bin"

    self.previousFolderNum = self.folderNum
    for picturePacket in validSSDVPackets:
      try:
        packetNumber = int(picturePacket[14:18], 16) #gets the packet number
        self.packetList[packetNumber] = picturePacket #puts the packet into the correct index of the list
      except:
        self.logger.info("Invalid packet Number: " + str(picturePacket))


  def writePicture(self):
    #if self.binFilePath != '':
    saveFile = open(self.binFilePath, "wb+")
    for packet in self.packetList:
      if str(packet) == "0":
        continue
      else:
        try:
          saveFile.write(bytearray.fromhex(str(packet)))
        except:
          self.logger.info("Failed to write a packet to the .bin file")
          self.logger.info("Failed packet:" + packet)
    self.logger.info("Finished writing picture")
    self.packetList = ["0"] * 30000
    saveFile.close()
    
    # Run SSDV to decode the file
    outputJPEGFile = self.pictureIDFolder + "picture_" + str(self.folderNum) + "_" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpeg'
    self.logger.info("output JPEG file: " + str(outputJPEGFile))
    ssdvProcess = subprocess.run(["/home/pi/ssdv/ssdv", "-d", self.binFilePath, outputJPEGFile],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    # Log SSDV subprocess
    self.logger.info(ssdvProcess.stdout.decode("utf-8"))
    
    #self.binFilePath = ''
    sleep(1)

  def intFromHex(self,hex):
    return int(hex, 16)

  def floatFromHex(self,hex):
    return struct.unpack('!f', bytes.fromhex(hex))[0]

if __name__ == "__main__":       
  DecodeData = decodeData()
  DecodeData.processData()
