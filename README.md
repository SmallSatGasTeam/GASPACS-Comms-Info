# GASPACS CubeSat Communications Information
GASPACS is a 1U CubeSat designed, developed, and completed by undergraduate students on the Get Away Special team at Utah State University.

GASPACS stands for **G**et **A**way **S**pecial **P**assive **A**ttitude **C**ontrol **S**atellite. The satellite is a technology demonstration for an inflatable boom structure that will double as a passive attitude stabilization device due to the aerodynamic drag in Low Earth Orbit (LEO). 

GASPACS was launched on 12/21/2021 on SpaceX CRS-24. GASPACS is currently aboard the International Space Station (ISS), with deployment into orbit via the NanoRacks CubeSat Deployer (NRCSD) scheduled for the week of 1/24/2022. This page will be updated after deployment with information on tracking GASPACS and ongoing mission operations.

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


## GAS Team Ground Station:
- TO DO: Add List all of our equipment for receiving & brief description of software we use
