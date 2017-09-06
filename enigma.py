#!/usr/bin/env python

"""enigma.py: Enigma M3 Simulator"""

__author__ = "Kurt Giessel"
__copyright__ = "Copyright 2015, Dennyhill Demolition Company"
__credits__ = ["Kurt Giessel"]
__license__ = "GPL"
__version__ = "0.1.2"
__maintainer__ = "Kurt Giessel"
__email__ = "kurt@giessel.net"
__status__ = "Beta"

#####################################################################################################################
#Variables
alphabet = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
rotor1 = ('E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J')
rotor2 = ('A','J','D','K','S','I','R','U','X','B','L','H','W','T','M','C','Q','G','Z','N','P','Y','F','V','O','E')
rotor3 = ('B','D','F','H','J','L','C','P','R','T','X','V','Z','N','Y','E','I','W','G','A','K','M','U','S','Q','O')
rotor4 = ('E','S','O','V','P','Z','J','A','Y','Q','U','I','R','H','X','L','N','F','T','G','K','D','C','M','W','B')
rotor5 = ('V','Z','B','R','G','I','T','Y','U','P','S','D','N','H','L','X','A','W','M','J','Q','O','F','E','C','K')
reflector = ('Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T')
plugboard = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

rotorAClick = 0
rotorBClick = 0
rotorCClick = 1
encryptedMsg = ''
steckerCount = 1
lettersUsed = ['']

#####################################################################################################################
#Functions

#Plugboard Functions
def doSteckerbrett(stecker1,stecker2): #swap letters in plugboars list

    plugboard.remove(stecker1)
    plugboard.insert(alphabet.index(stecker2),stecker1)
    plugboard.remove(stecker2)
    plugboard.insert(alphabet.index(stecker1),stecker2)

def chooseWires(steckers): #choose a pair of letters to cross connect
    global ans
    global steckerCount #keeps track of how many wires have been used

    stecker1 = raw_input('Select first letter of the pair: ').upper()
    while lettersUsed.count(stecker1) == 1:
        if lettersUsed.count(stecker1) == 1:
            print 'You have already used %s.' % stecker1
            stecker1 = raw_input('Select first letter of the pair: ').upper()
        else:
            lettersUsed.append(stecker1)
    lettersUsed.append(stecker1)    
    stecker2 = raw_input('Select next letter of pair: ').upper()
    while lettersUsed.count(stecker2) == 1:
        if lettersUsed.count(stecker2) == 1:
            print 'You have already used %s.' % stecker2
            stecker2 = raw_input('Select next letter of the pair: ').upper()
        else:
            lettersUsed.append(stecker2)    
    lettersUsed.append(stecker2)

    doSteckerbrett(stecker1,stecker2)

    if steckers == 1:
        print 'You have used 1 wire.'
    else:
        print 'You have used %s wires.' % str(steckers)
    ans = raw_input('Do you want to configure another pair? (y,n): ').upper()

    steckerCount += 1 
    return
    
#Configure Rotors Function
def rotorConfig(): #configure each rotor with their initital setting
    global rotorA
    global rotorASetting
    global rotorB
    global rotorBNotch
    global rotorBSetting
    global rotorC
    global rotorCNotch
    global rotorCSetting
    
    selectRotor('Left','rotorA')
    rotorA = rotorUsed
    rotorASetting = rotorSetting
    selectRotor('Center','rotorB')
    rotorB = rotorUsed
    rotorBNotch = notch
    rotorBSetting = rotorSetting
    selectRotor('Right','rotorC')
    rotorC = rotorUsed
    rotorCNotch = notch
    rotorCSetting = rotorSetting
    return

#Select Rotors Function
def selectRotor(location,rotor): #select which rotors to use
    global rotorUsed
    global rotorSetting
    global notch
    rotorSelect = raw_input('Select %s Rotor (1-5): ' % location)
    if rotorSelect == '1':
	   rotorUsed = rotor1
	   notch = 17 #notch indicates where the next rotor rotates
    elif rotorSelect == '2':
	   rotorUsed = rotor2
	   notch = 5
    elif rotorSelect == '3':
	   rotorUsed = rotor3
	   notch = 22
    elif rotorSelect == '4':
	   rotorUsed = rotor4
	   notch = 10
    elif rotorSelect == '5':
	   rotorUsed = rotor5
	   notch = 0
    rotorSelectSetting = raw_input('Select Inital Setting for %s Rotor (A-Z): ' % location).upper()
    rotorSetting = alphabet.index(rotorSelectSetting)	
    return

#Get Contact Index Function
def getContactIndex(inputLetter,offset): #get the contact position of the rotor
    global contactIndex
    contactIndex = alphabet.index(inputLetter) - offset
    if contactIndex < 0:
	   contactIndex += 26
    return 

#Rotor In Function
def rotorIn(contactIndex,rotor,offset): #get rotor letter for inbound pass
    global outputLetter
    letterIndex = contactIndex + offset
    if letterIndex >= 26:
	   letterIndex -= 26
    outputLetter = rotor[letterIndex]    
    return

#Reflector Function
def doReflector(contactIndex,reflector): #get reflector letter
    global outputLetter
    outputLetter = reflector[contactIndex]
    return

#rotor Out Function    
def rotorOut(contactIndex,rotor,offset): #get rotor letter for outbound pass
    global outputLetter
    innerLetterIndex = contactIndex + offset
    if innerLetterIndex >= 26:
	   innerLetterIndex -= 26
    innerLetter = alphabet[innerLetterIndex]
    outerLetterIndex = rotor.index(innerLetter)
    outputLetter = alphabet[outerLetterIndex]    
    return

def doRotors(inputLetter): #get letter after going through all rotors
    global rotorsOutLetter
    global rotorAClick
    global rotorBClick
    global rotorCClick
	
    offset = 0

    getContactIndex(inputLetter,offset)
    offset = rotorCClick + rotorCSetting
    if offset >= 26:
        offset -= 26
    if offset == rotorCNotch:
	   rotorBClick = 1
    rotorIn(contactIndex,rotorC,offset)
    
    getContactIndex(outputLetter,offset)
    offset = rotorBClick + rotorBSetting
    if offset >= 26:
        offset -= 26
    if offset == rotorBNotch and rotorBClick == 1:
	   rotorAClick = 1
    rotorIn(contactIndex,rotorB,offset)

    getContactIndex(outputLetter,offset)
    offset = rotorAClick + rotorASetting
    if offset >= 26:
        offset -= 26
    rotorIn(contactIndex,rotorA,offset)
    
    getContactIndex(outputLetter,offset)
    doReflector(contactIndex,reflector)
    
    offset = 0
    getContactIndex(outputLetter,offset)
    offset = rotorAClick + rotorASetting
    if offset >= 26:
        offset -= 26
    rotorOut(contactIndex,rotorA,offset)
    
    getContactIndex(outputLetter,offset)
    offset = rotorBClick + rotorBSetting
    if offset >= 26:
        offset -= 26
    rotorOut(contactIndex,rotorB,offset)
    
    getContactIndex(outputLetter,offset)
    offset = rotorCClick + rotorCSetting
    if offset >= 26:
        offset -= 26
    rotorOut(contactIndex,rotorC,offset)
    
    rotorsOutLetter = outputLetter
    return

#####################################################################################################################    

print '#######################'
print '# Enigma M3 Simulator #'
print '#######################'
print 

print 'The plugbord cross-connects pairs of letters using wires.'
print 'You can use up to 10 wires on the plugboard.'
ans = raw_input('Do you want to configure the plugboard? (y,n): ').upper()

while ans == 'Y' and steckerCount < 10: #you can only choose 10 sets of wires

    chooseWires(steckerCount)

print 
print 'Now you will select the rotors and their initial settings.'
print 'There are 5 rotors to choose from. You will use 3 of them.'
print 'Then you will select an initial setting for each rotor.'

rotorConfig()

print 
print '#########################################################################'
print '# The Enigma machine is configured. You are ready to send your message. #'
print '#########################################################################'
print 

while 1 == 1 :
    keyPress = raw_input('Type a Letter (! to quit): ').upper()
    checkKeyPress = alphabet.count(keyPress)
    if keyPress == '!':
        quit()
    while checkKeyPress != 1:
        print keyPress+' is not a letter. Please type a letter (A-Z)'
        keyPress = raw_input('Type a Letter (* to quit): ').upper()
        checkKeyPress = alphabet.count(keyPress)
        if keyPress == '!':
            quit()

    #Plugboard In
    keyPressIndex = alphabet.index(keyPress)
    plugboardInLetter = plugboard[keyPressIndex]
    doRotors(plugboardInLetter)
    
    #Plugboard Out
    offset = rotorCClick + rotorCSetting
    getContactIndex(rotorsOutLetter,offset)
    plugboardOutLetter = plugboard[contactIndex]
    illuminatedLetter = plugboardOutLetter
	
    #Encrypted Message
    encryptedMsg += str(illuminatedLetter)
    print 'Encrypted Message: %s' % encryptedMsg
    
    rotorCClick += 1

    

