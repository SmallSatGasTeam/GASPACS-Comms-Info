# GASPACS CubeSat Communications Information
GASPACS is a 1U CubeSat designed, developed, and completed by undergraduate students on the Get Away Special team at Utah State University.

GASPACS stands for **G**et **A**way **S**pecial **P**assive **A**ttitude **C**ontrol **S**atellite. The satellite is a technology demonstration for an inflatable boom structure that will double as a passive attitude stabilization device due to the aerodynamic drag in Low Earth Orbit (LEO). 

GASPACS was launched on 12/21/2021 on SpaceX CRS-24. GASPACS is currently aboard the International Space Station (ISS), with deployment into orbit via the NanoRacks CubeSat Deployer (NRCSD) scheduled for the week of 1/24/2022. This page will be updated after deployment with information on tracking GASPACS and ongoing mission operations.

# UPDATE: 1/28/2022!!
GASPACS is in orbit and fully operational!! Several images, and telemetry data have been received. For updates and copies of the pictures, see: [twitter.com/GASPACS_CubeSat](twitter.com/GASPACS_CubeSat)

# HOW TO DEMODULATE/DECODE GASPACS IMAGES AND TELEMETRY:
## Note: this has only been tested to work on Windows 10. It should work on linux as well, but it is not tested.
1. GASPACS only transmits images and telemetry by command. The GAS team can schedule downlinks over other ground stations. If you would like us to attempt a downlink over your ground station, email coordinator@gas.usu.edu
2. Record a GASPACS observation containing image or telemetry downlink (or find a recording)
	- An example recording that has been succesfully turned into an image can be found here: [https://network.satnogs.org/observations/5365011/](https://network.satnogs.org/observations/5365011/)
3. Download the soundmodem made by UZ7HO: [https://uz7.ho.ua/gaspacs.zip](https://uz7.ho.ua/gaspacs.zip)
	- Note: gr-satellites has also been able to demodulate GASPACS packets, however the output format of the packets has not been tested to work with the GASPACS decoding script.
4. Route your computer's audio output into its audio input, so you can have the recorded audio as an input for the soundmodem program.
	- We used the VB-Audio software which worked on Windows: [https://vb-audio.com/Cable/](https://vb-audio.com/Cable/)
5. Run the soundmodem program. Under Settings, click "Open monitor log file". Save the log file somewhere you'll remember (make sure the log file is a .txt file).
6. Play the audio recording, and watch as packets are decoded in the soundmodem program.
7. Download the GASPACS decoder software: [https://github.com/SmallSatGasTeam/GASPACS-Comms-Info/tree/main/GASPACS-Receive-Data-Files](https://github.com/SmallSatGasTeam/GASPACS-Comms-Info/tree/main/GASPACS-Receive-Data-Files)
8. Install the GAS team fork of SSDV: [https://github.com/SmallSatGasTeam/ssdv](https://github.com/SmallSatGasTeam/ssdv)
9. Edit line 329 of decode.py to point to the full PATH/FILENAME of your SSDV executable
10. Test the decoder software by moving the file "Example-W7KKE-soundmodem-ouput.txt" into the "new" folder, and run the decode.py script.
	- If all goes well, you should see a lot of packets printed to the console, and there will now be a "0" folder in the "Pictures" folder, which will contain a .bin file, and the decoded .jpeg! The Example .txt file will be moved into the "old" folder. To decode it again, simply move the .txt file back into the "new" folder.
11. To demodulate and decode your own recording: simply move your soundmodem log .txt file into the "new" folder, and run decode.py.
	- This program will work with images, TTNC data, Attitude Data, and Deployment Data from GASPACS. Images are placed in the "Pictures" folder under their appropriate image ID, and data is stored in the "allData.csv" file. 
    - This program can handle missing image packets, out of order packets, and images received over multiple different transmissions. It will automatically combine picture packets from multiple .txt files, so if you receive half of the picture in one transmission, and the other half in another, it will put them together into a final .jpeg!
    

## RF Specifications:
- Center frequency: 437.365 MHz
- Baudrate: 9600 bps
- Modulation: 2GFSK
- Frequency Deviation: 2400 Hz
- ModInd: 0.5
- Polarization: Circular 
	- Both RHCP and LCHP
    - Polarization will change as GASPACS slowly rotates in space
- TX Power: 1W
- Antenna Gain: ~ 0 dBi, omnidirectional
- AX.25 beacon every 120 seconds
- Audio beacon every 300 seconds
- Telemetry & images downlinked when passing over Logan, Utah
- Additional telemetry & images can be scheduled over compatible ground stations. Please email coordinator@gas.usu.edu with your request.
- Telemetry packets use custom structure (described below)
- Image packets use SSDV format (described below)
- LEO orbit, deployed from ISS

## CubeSat Communications Hardware:

- Radio: [Endurosat UHF Transceiver](https://www.endurosat.com/cubesat-store/cubesat-communication-modules/uhf-transceiver-ii/)
- Antenna: [Endurosat UHF Antenna](https://www.endurosat.com/cubesat-store/cubesat-antennas/uhf-antenna/)

## Packet Structure:
_**All packets transmitted by GASPACS utilize the Endurosat radio packet structure, containing a preamble, sync word, payload, and CRC16:**_
![Screenshot 2022-01-11 025351.jpg]({{site.baseurl}}/Screenshot 2022-01-11 025351.jpg)
![Screenshot 2022-01-11 025456.jpg]({{site.baseurl}}/Screenshot 2022-01-11 025456.jpg)
     
### AX.25 Packet Structure:
Every 120 seconds, an AX.25 beacon is broadcasted:
- Dest. Callsign: CQ
- Source Callsign: N7GAS
- Content: "Hello from the GASPACS CubeSat!"
- Structure:
![Screenshot 2022-01-11 025657.jpg]({{site.baseurl}}/Screenshot 2022-01-11 025657.jpg)
- The AX.25 protocol UI frame fits inside the Data Field 2 "Payload" and is surrounded by a Preamble and Postamble.
- Note from Endurosat: The  used  scrambling  polynomial  is 1  +  X12  + X17.  This  means the  currently  transmitted  bit  is  the EXOR of the current data bit, plus the bits that have been transmitted 12 and 17 bits earlier. Likewise, the  unscrambling  operation  simply  EXORs  the  bit  received  now  with  those  sent  12  and  17  bits earlier. The unscrambler perforce requires 17 bits to synchronize.
- **Sample AX.25 Packet IQ Data:**
- [IQ Data in Wav format](https://github.com/SmallSatGasTeam/GASPACS-Comms-Info/blob/main/GASPACS_AX25_437365000Hz_IQ.wav)
- **Sample AX.25 Packet Audio File:**
- [Audio file in Wav format](https://github.com/SmallSatGasTeam/GASPACS-Comms-Info/blob/main/GASPACS_48K_AF.wav)
- The Audio Wav file has been successfully decoded by PE0SAT using [this GASPACS.yml file](https://github.com/SmallSatGasTeam/GASPACS-Comms-Info/blob/main/GASPACS.yml) and gr_satellites:
```
gr_satellites GASPACS.yml --wavfile GASPACS_48K_AF.wav --samp_rate 48e3 --disable_dc_block --hexdump
```




### Audio Beacon Information:
Every 500 seconds, an audio beacon is broadcasted:
- The audio beacon consists of the N7GAS callsign in morse code, followed by "The Scotsman" tune.

### Telemetry Packet Structure:
_**All telemetry and image packets fit inside of the Data Field 2 "Payload" portion of the Endurosat packet structure.**_ 

GASPACS has three types of telemetry packets: Attitude, Deployment, and TT&C

**Attitude Data:**
- Collected at 1Hz for 30 minutes of every 24 hour period.
- Consists of all the data necessary to perform attitude determination calculations on the ground.
- Includes time, sun sensor, and magnetometer data.
- Structure:
![Screenshot 2022-01-11 031118.jpg]({{site.baseurl}}/Screenshot 2022-01-11 031118.jpg)

- **Sample Attitude Hex Data (This is the Data Field 2 Content):**
```
474153504143530061807d14000000000000000000000000000000000000000042ca000042ca000042ca000047415350414353
```
- The decoded values are:
```
0, 1635810580, 0.0, 0.0, 0.0, 0.0, 0.0, 101.0, 101.0, 101.0
```

**Deployment Data:**
- Collected at 10-15 Hz for ~90 seconds during AeroBoom deployment.
- Includes time, accelerometer, and UV sensor data.
- Structure:
![Screenshot 2022-01-11 031315.jpg]({{site.baseurl}}/Screenshot 2022-01-11 031315.jpg)

**TTNC Data:**
- Collected every 2 minutes throughout the mission.
- This is the "housekeeping" data that shows the satellite's health over time.
- Includes temperatures, battery voltages, solar panel power, and more.
- Structure:
![Screenshot 2022-01-11 031517.jpg]({{site.baseurl}}/Screenshot 2022-01-11 031517.jpg)
![Screenshot 2022-01-11 031528.jpg]({{site.baseurl}}/Screenshot 2022-01-11 031528.jpg)

- **Sample TTNC Hex Data (This is the Data Field 2 Content):**    
```
474153504143530161832dd002001700000000000000000000000042473333431c0000431c0000431c000040c333334120000040c333333ff00000408000004080000040d00000403333334033333340d00000403333334033333340d000004033333347415350414353
```
- The decoded values are:
```
1, 1635986896, 2, 23, 0.0, 0.0, 0.0, 49.79999923706055, 156.0, 156.0, 156.0, 6.099999904632568, 10.0, 6.099999904632568, 1.875, 4.0, 4.0, 6.5, 2.799999952316284, 2.799999952316284, 6.5, 2.799999952316284, 2.799999952316284, 6.5, 2.799999952316284
```

### Image Packet Structure:
- The primary mission of GASPACS is to transmit down a clear image of the deployed AeroBoom. A raspberry pi camera onboard the CubeSat will photgraph the deployed boom. 
- A [custom SSDV implementation](https://github.com/SmallSatGasTeam/ssdv) where the packet length is changed from 256 bytes to 128 bytes (to fit inside the Data Field 2 "Payload") is used to compress the images. 
- The original SSDV packet structure is shown below. 
- "Normal mode" is used with FEC enabled.
- Note that the payload portion of the GASPACS SSDV implementation is shorted by 128 bytes, to allow a single SSDV packet to fit inside the Endurosat packet structure's Data Field 2.
![Screenshot 2022-01-11 032010.jpg]({{site.baseurl}}/Screenshot 2022-01-11 032010.jpg)

- **Sample Image Packet Hex Data (This is the Data Field 2 content):**
```
556604f02a5b020000281e00000000e1f65284c53b70a5dc0f6ad0c84c52d191ef46e1e94007414dfe2a4249340a606ba9f968a621f947d29e2900b4d20337d29d484503241c8a7638a8c3714e04d2014ad331cd3cf2314cf2fe6077695507cf23592c439b6a02af675f65c16a131e978af017ddcdfa6ac69d96c8bd1be990b1
```
- **[Full Sample Image Bin File](https://github.com/SmallSatGasTeam/GASPACS-Comms-Info/blob/main/GASPACS_SSDV_Picture_2.bin) (note this data would have to be extracted from the Data Field 2 content for each packet)**



## GAS Team Ground Station:
- TO DO: Add List all of our equipment for receiving & brief description of software we use
