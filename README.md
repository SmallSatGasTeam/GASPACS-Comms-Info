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
- Note from Endurosat: The  used  scrambling  polynomial  is 1  +  X12  + X17.  This  means the  currently  transmitted  bit  is  the EXOR of the current data bit, plus the bits that have been transmitted 12 and 17 bits earlier. Likewise, the  unscrambling  operation  simply  EXORs  the  bit  received  now  with  those  sent  12  and  17  bits earlier. The unscrambler perforce requires 17 bits to synchronize.

### Audio Beacon Information:
Every 500 seconds, an audio beacon is broadcasted:
- The audio beacon consists of the N7GAS callsign in morse code, followed by "The Scotsman" tune.

### Telemetry Packet Structure:
_**All telemetry packets fit inside of the Data Field 2 "Payload" portion of the Endurosat packet structure.**_ 

GASPACS has three types of telemetry packets: Attitude, Deployment, and TT&C

**Attitude Data:**
- Collected at 1Hz for 30 minutes of every 24 hour period.
- Consists of all the data necessary to perform attitude determination calculations on the ground.
- Includes time, sun sensor, and magnetometer data.
- Structure:
![Screenshot 2022-01-11 031118.jpg]({{site.baseurl}}/Screenshot 2022-01-11 031118.jpg)

**Deployment Data:**
- Collected at 10-15 Hz for ~90 seconds during AeroBoom deployment.
- Includes time, accelerometer, and UV sensor data.
- Structure:
![Screenshot 2022-01-11 031315.jpg]({{site.baseurl}}/Screenshot 2022-01-11 031315.jpg)

**TT&C Data:**
- This is the "housekeeping" data that shows the satellite's health over time.
- Includes temperatures, battery voltages, solar panel power, and more.
- Structure:
![Screenshot 2022-01-11 031517.jpg]({{site.baseurl}}/Screenshot 2022-01-11 031517.jpg)
![Screenshot 2022-01-11 031528.jpg]({{site.baseurl}}/Screenshot 2022-01-11 031528.jpg)

    
### Image Packet Structure:
The primary mission of GASPACS is to transmit down a clear image of the deployed AeroBoom. A raspberry pi camera onboard the CubeSat will photgraph the deployed boom. A [custom SSDV implementation](https://github.com/SmallSatGasTeam/ssdv) where the packet length is changed from 256 bytes to 128 bytes (to fit inside the Data Field 2 "Payload") is used to compress the images. The SSDV packet structure is:
![Screenshot 2022-01-11 032010.jpg]({{site.baseurl}}/Screenshot 2022-01-11 032010.jpg)


## GAS Team Ground Station:
- TO DO: Add List all of our equipment for receiving & brief description of software we use
