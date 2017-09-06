#!/usr/bin/env python

"""bombe.py: Turing Bombe Simulator"""

__author__ = "Kurt Giessel"
__copyright__ = "Copyright 2015, Dennyhill Demolition Company"
__credits__ = ["Kurt Giessel"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Kurt Giessel"
__email__ = "kurt@giessel.net"
__status__ = "Beta"

#####################################################################################################################

import itertools
import time

#####################################################################################################################
#Variables
alphabet = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
rotor1 = ('E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J','Rotor1')
rotor2 = ('A','J','D','K','S','I','R','U','X','B','L','H','W','T','M','C','Q','G','Z','N','P','Y','F','V','O','E','Rotor2')
rotor3 = ('B','D','F','H','J','L','C','P','R','T','X','V','Z','N','Y','E','I','W','G','A','K','M','U','S','Q','O','Rotor3')
rotor4 = ('E','S','O','V','P','Z','J','A','Y','Q','U','I','R','H','X','L','N','F','T','G','K','D','C','M','W','B','Rotor4')
rotor5 = ('V','Z','B','R','G','I','T','Y','U','P','S','D','N','H','L','X','A','W','M','J','Q','O','F','E','C','K','Rotor5')
reflector = ('Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T')

global encryptedTextMsg
global plainTextMsg

#Configure Rotors Function
def selectRotor(i,n): #select which rotors to use
    global rotorUsed
    global notch
    rotorSelect = rotorPerm[i][n]
    if rotorSelect == 1:
        rotorUsed = rotor1
        notch = 17
    elif rotorSelect == 2:
        rotorUsed = rotor2
        notch = 5
    elif rotorSelect == 3:
        rotorUsed = rotor3
        notch = 22
    elif rotorSelect == 4:
        rotorUsed = rotor4
        notch = 10
    elif rotorSelect == 5:
        rotorUsed = rotor5
        notch = 0 
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

def doRotors(inputLetter,compareIndex): #get rotor letter for outbound pass
    global rotorsOutLetter
    global rotorAClicked
    global rotorBClicked
	
    rotorCClick = compareIndex + 1

    offset = 0
    getContactIndex(inputLetter,offset)
    offset = rotorCClick + rotorCSetting
    if offset >= 26:
    	offset -= 26
    if offset == rotorCNotch:
		rotorBClicked = True
    rotorIn(contactIndex,rotorC,offset)
    
    getContactIndex(outputLetter,offset)
    offset = rotorBSetting
    if rotorBClicked == True:
	offset += 1
    if offset >= 26:
    	offset -= 26
    if offset == rotorBNotch and rotorBClicked == True:
		rotorAClicked = True
    rotorIn(contactIndex,rotorB,offset)

    getContactIndex(outputLetter,offset)
    offset = rotorASetting
    if rotorAClicked == True:
	offset +=1
    if offset >= 26:
    	offset -= 26
    rotorIn(contactIndex,rotorA,offset)
    
    getContactIndex(outputLetter,offset)
    doReflector(contactIndex,reflector)
    
    offset = 0
    getContactIndex(outputLetter,offset)
    offset =  rotorASetting
    if rotorAClicked == True:
	offset += 1
    if offset >= 26:
    	offset -= 26
    rotorOut(contactIndex,rotorA,offset)
    
    getContactIndex(outputLetter,offset)
    offset =  rotorBSetting
    if rotorBClicked == True:
	offset += 1
    if offset >= 26:
    	offset -= 26
    rotorOut(contactIndex,rotorB,offset)
    
    getContactIndex(outputLetter,offset)
    offset = rotorCClick + rotorCSetting
    if offset >= 26:
    	offset -= 26
    rotorOut(contactIndex,rotorC,offset)

    getContactIndex(outputLetter,offset)
    rotorsOutLetter = alphabet[contactIndex]
    return

def compareLetter(compareIndex): #compare the plaintext letter with suspected results
	global rotorsOutLetter
	inputLetter = encryptedTextMsg[compareIndex]
	plainTextLetter = plainTextMsg[compareIndex]
	doRotors(inputLetter,compareIndex)
	#print 'Trying '+ alphabet[rotorASetting]+ alphabet[rotorBSetting]+ alphabet[rotorCSetting]
	if rotorsOutLetter == plainTextLetter:
		#print 'Possible Solution... Checking Next Letter'
		compareIndex += 1
		if compareIndex == 7:
			print 
			print 
			print '#####################################################'
			print 'Solution Found!!!!!'
			print 'Settings: '+ rotorA[26]+':'+alphabet[rotorASetting]+'  '+rotorB[26]+':'+alphabet[rotorBSetting]+'  '+rotorC[26]+':'+alphabet[rotorCSetting]
			rAs = rotorASetting + 1
			rBs = rotorBSetting + 1
			rCs = rotorCSetting + 1
			possibleSolutions = i * (rAs * (26 * 26)) + (rBs * 26) + rCs
			endTime = time.time()
			totalTime = endTime - startTime 
			print 'Checked '+str(possibleSolutions)+' possible solutions in '+str(totalTime)+' seconds'
			print '#####################################################'
			print 
			print 
			quit()
		compareLetter(compareIndex)

#####################################################################################################################    

print '##########################'
print '# Turing Bombe Simulator #'
print '##########################'
print 

encryptedTextMsg = raw_input('Enter Encrypted Text: ').upper()
plainTextMsg = raw_input('Enter Plain Text: ').upper()

startTime = time.time()

#Check All Rotor Permutations
rotorPerm = list(itertools.permutations([1,2,3,4,5], 3)) 

i = 0
for list in rotorPerm:

    rotorASetting = 0
    rotorBSetting = 0
    rotorCSetting = 0
    selectRotor(i,0)
    rotorA = rotorUsed
    selectRotor(i,1)
    rotorB = rotorUsed
    rotorBNotch = notch
    selectRotor(i,2)
    rotorC = rotorUsed
    rotorCNotch = notch

    print 'Trying '+ rotorA[26] +':'+ rotorB[26]+ ':'+rotorC[26] 

    i += 1

    #Check All Rotor Setting
    while 1 == 1:
	rotorAClicked = False
	rotorBClicked = False
        compareIndex = 0
        compareLetter(compareIndex)
        rotorCSetting += 1
        if rotorCSetting == 26:
            rotorCSetting = 0
            rotorBSetting += 1
        if rotorBSetting == 26:
            rotorBSetting = 0
            rotorASetting += 1
        if rotorASetting == 26:
            break

	





