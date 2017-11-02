#!/usr/bin/python
import sys

# This program should display a typed string from a USB Key board capture as recovered from a pcap, as shown below with tshark
# It should support displaying a string typed in a single window. It probably won't work if the typing is spread across multiple windows. You would have to add additiona support for that situation.
# This program is provided mainly for my own reference but feel free to use it and modify it to suit your needs. It will likely have to be customized to suit various challenges.

# To get the usb capture data:
# tshark -Y ((usb.transfer_type == 0x01) && (frame.len == 35)) && !(usb.capdata == 00:00:00:00:00:00:00:00) -r deadly_arthropod.pcap -T fields -e usb.capdata > usb.capdata
# For the above, you may need to adjust the length of the cframe length

# Mappings from http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
mapping = {#0x00:("",""), # Leave this one out since it is not a character
           0x04:("a","A"),
           0x05:("b","B"),
           0x06:("c","C"),
           0x07:("d","D"),
           0x08:("e","E"),
           0x09:("f","F"),
           0x0b:("h","H"),
           0x0c:("i","I"),
           0x0e:("k","K"),
           0x0f:("l","L"),
           0x10:("m","M"),
           0x12:("o","O"),
           0x13:("p","P"),
           0x14:("q","Q"),
           0x15:("r","R"),
           0x16:("s","S"),
           0x17:("t","T"),
           0x18:("u","U"),
           0x1a:("w","W"),
           0x1b:("x","X"),
           0x1c:("y","Y"),
           0x1d:("z","Z"),
           0x1e:("1","!"),
           0x1f:("2","@"),
           0x20:("3","#"),
           0x22:("5","%"),
           0x27:("0",")"),
           0x28:("\n","\n"),
           0x29:("ESC","ESC"),
           0x2a:("DEL","DEL"),
           0x2b:("\t", "\t"),
           0x2c:(" "," "),
           0x2d:("-","_"),
           0x2e:("=","+"),
           0x2f:("[","{"),
           0x30:("]","}"),
           0x31:("\\","|"),
           0x32:("#","~"), #Non-Us Keyboard
           0x33:(":",";"),
           0x34:("\'","\""),
           0x35:("`","~"),
           0x36:(",","<"),
           0x37:(".",">"),
           0x38:("/","?"),
           0x39:("[ CAPS ]","[ Shift + CAPS ]"),
           0x3a:("[ F1 ]","[ Shift + F1 ]"),
           0x3b:("[ F2 ]","[ Shift + F2 ]"),
           0x3c:("[ F3 ]","[ Shift + F3 ]"),
           0x3d:("[ F4 ]","[ Shift + F4 ]"),
           0x3e:("[ F5 ]","[ Shift + F5 ]"),
           0x3f:("[ F6 ]","[ Shift + F6 ]"),
           0x40:("[ F7 ]","[ Shift + F7 ]"),
           0x41:("[ F8 ]","[ Shift + F8 ]"),
           0x42:("[ F9 ]","[ Shift + F9 ]"),
           0x43:("[ F10 ]","[ Shift + F10 ]"),
           0x44:("[ F11 ]","[ Shift + F11 ]"),
           0x45:("[ F12 ]","[ Shift + F12 ]"),
           0x46:("[ Printscreen ]","[ Shift + Printscreen ]"),
           0x47:("[ Scroll Lock ]","[ Shift + Scroll Lock ]"),
           0x48:("[ Pause ]","[ Shift + Pause ]"),
           0x49:("[ Insert ]","[ Shift + Insert ]"),
           0x4a:("[ Home ]","[ Shift + Home ]"),
           0x4b:("[ Page Up ]","[ Shift + Page Up ]"), 
           0x4c:("[ Delete forward ]","[ Shift + Delete Forward ]"),
           0x4d:("[ End ]","[ Shift + End ]"),
           0x4e:("[ Page Down ] ","[ Shift + Page Down ]"), 
           0x4f:("[ --> ]","[ Shift + --> ]"),
           0x50:("[ <-- ]","[ Shift + <-- ]")  }

if len(sys.argv) < 2:
    print("Please enter the filename that contains the usb capture data.")
    exit(1)

filename = sys.argv[1]

f=open(filename,"r")
strIndex = 0
displayIndex=0
typedString = ""
for line in f.readlines():
    parts = line.split(":")
    #print typedString
    isShift = 0

    # If the first byte is a 2, that means that the shift was pressed
    if (parts[0] == "02"):
      isShift = 1
    index = int(parts[2],16)

    # Ignore it if it isn't in the mapping or if it is a 0
    # In the pcap I looked at, pressing shift caused a 0 to be sent as the third byte, so we want to just ignore those
    # The 2 as the first byte remained when the real key was pressed.
    if index != 0x00 and index in mapping:
       nextLetter = mapping[index][isShift]
       #print "Next Letter: "+nextLetter
       if len(nextLetter)>1:
          #print "Control Character"
          if index == 0x4f: # right arrow
            strIndex+=1
            displayIndex+=1
          if index == 0x50: # left arrow
            strIndex-=1
            displayIndex-=1
          #print typedString
          #print " "*(displayIndex) + "^"
          #print ""
       else:
          # This is just so I can display the caret for debugging purposes
          if (nextLetter == "\n"):
            displayIndex=-1

          if strIndex == len(typedString):
            typedString += nextLetter
          elif strIndex == 0:
            typedString = nextLetter + typedString
          else:
            # It goes in the middle somewhere
            typedString = typedString[0:strIndex]+nextLetter+typedString[strIndex:]
          strIndex+=1  
          displayIndex+=1
    #else:
       #print '[NOT FOUND]',

print "Recovered String:"
print typedString
