import array as arr
import pygame
import os
import re

from sky_racers.classes.Car import Car
from pathlib import Path

'''
This class reads input files and outputs a user command list. This list is used as a set of instructions for the car to run every frame.

Current issues that need to be addressed:
    -No keyword angle is coded in (Everything is based on distance currently).
    -Number inports to command def may become out of order if more than 1 is used currently.
    -The calculation for angle in the defs turn_towards and turn_away, 90 works as 0? Print statements of the actual angle show the issue.
    -Inability to reliabily use wall and checkpoint calculations concurently, one will return before other is exicuted.
'''

acc = 0
reverse = 0
turnleft = 0
turnright = 0

class CommandCall:

      
    def turn_towards(car, turnleft, turnright,  checkpoint_or_wall):
 
        if checkpoint_or_wall == 1:
            if (90 <= int(car.angle_to_checkpoint)):
                #print("Turned right: 90 =",(int (car.angle_to_checkpoint)))
                return pygame.USEREVENT+0
            elif (90 >= int(car.angle_to_checkpoint)):
                #print("Turned left: 90 =",(int (car.angle_to_checkpoint)))
                return pygame.USEREVENT+1
            else:
                return pygame.USEREVENT+4

        if checkpoint_or_wall == 2:
            if (90 <= int(car.angle_to_wall)) and (turnright != True):
                return pygame.USEREVENT+0
            elif (90 >= int(car.angle_to_wall)) and (turnleft != True):
                return pygame.USEREVENT+1
            else:
                return pygame.USEREVENT+4

  
    def turn_away(car, turnleft, turnright, checkpoint_or_wall):

        if checkpoint_or_wall == 1:
            if (90 <= int(car.angle_to_checkpoint)) and (turnleft != True):
                return pygame.USEREVENT+1
            elif (90 >= int(car.angle_to_checkpoint)) and (turnright != True):
                return pygame.USEREVENT+0
            else:
                return pygame.USEREVENT+4
        elif checkpoint_or_wall == 2:
            if (90 <= int(car.angle_to_wall)) and (turnleft != True):
                return pygame.USEREVENT+1
            elif (90 >= int(car.angle_to_wall)) and (turnright != True):
                return pygame.USEREVENT+0
            else:
                return pygame.USEREVENT+4
        

    def fileread(filename, car):
        word = [] #create an empty string to hold a word of the instrucion
        instruction = [] #create an empty string to hold the important parts of the instruction
        InstructionList = []#Create an empty string to hold every instruction
        InstructionListnum = 0
        CommandList =[]
        NumList = []
        wordnum = 0
        ListNum = 0

        #Sets the list to the length of 50
        x = 0
        while x < 50:
            InstructionList.append('')
            x+=1
        
        path = Path(__file__).parent
        file = open(str(path) + os.path.join('/', filename), "r") #open the file the user entered
        code = file.readlines() #create a list where each value is a line of text from the file.
        file.close() #closing the file.

        try:
            datacheck = code
        except:
            return 0
        
        for line in code: #loop through every character in each line
            if line == "\n":
                #word += character #if the character is not a new line character add it to the instruciton string 
                break
            word = re.split(r'\n|\s', line)
            for wordnum in range(len(word)):
                if word[wordnum] == "if":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "accelerate":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "reverse_accelerate":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "distance":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "angle":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "wall":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "checkpoint":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "increase":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "decrease":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "greater":
                    instruction.append(word[wordnum])
                elif word[wordnum] == "less":
                    instruction.append(word[wordnum])
                elif word[wordnum] == '':#This happens when there is a new line
                    InstructionList[InstructionListnum] = instruction
                    instruction = []
                    wordnum = 0
                    InstructionListnum += 1
                elif word[wordnum].isdigit():
                    instruction.append(word[wordnum])          

        #Removes all the extra characters, words, and whitespace
        while "" in InstructionList:
            InstructionList.remove('')

        #Reset previous uses
        InstructionListnum = 0
        ListNum = 0
        
        for InstructionListnum in range(len(InstructionList)):
            if (InstructionList[InstructionListnum][ListNum] == "accelerate"):#Accelerate the car
                CommandList.append(0)#Accelerate

            if (InstructionList[InstructionListnum][ListNum] == "reverse"):#Breaking, then going in reverese
                CommandList.append(1)#Reverse Accelerate
            
            if InstructionList[InstructionListnum][ListNum] == "if":
                if InstructionList[InstructionListnum][ListNum+1] == "distance":
                    if InstructionList[InstructionListnum][ListNum+2] == "wall":#This chunk checks to change the course to turn away from a wall
                        if InstructionList[InstructionListnum][ListNum+3] == "greater":
                            InstructionList[InstructionListnum][ListNum+4] = float(InstructionList[InstructionListnum][ListNum+4])
                            if InstructionList[InstructionListnum][ListNum+4] <= car.dist_to_wall:
                                NumList.append(InstructionList[InstructionListnum][ListNum+4])#Records all number occurances
                                if InstructionListnum + 1 <= len(InstructionList):
                                    if InstructionList[InstructionListnum+1][ListNum] == "increase":#Turn car away from wall
                                        CommandList.append(2)#Increase distance to wall(MORE)
                                    if InstructionList[InstructionListnum+1][ListNum] == "decrease":#Turn car toward wall
                                        CommandList.append(3)#Decrease distance to wall(MORE)

                        if InstructionList[InstructionListnum][ListNum+3] == "less":
                            InstructionList[InstructionListnum][ListNum+4] = float(InstructionList[InstructionListnum][ListNum+4])
                            if InstructionList[InstructionListnum][ListNum+4] >= car.dist_to_wall:
                                if InstructionListnum + 1 <= len(InstructionList):
                                    NumList.append(InstructionList[InstructionListnum][ListNum+4])#Records all number occurances
                                    if InstructionList[InstructionListnum+1][ListNum] == "increase":#Turn car away from wall
                                        CommandList.append(4)#Increase distance to wall(LESS)
                                    if InstructionList[InstructionListnum+1][ListNum] == "decrease":#Turn car toward wall
                                        CommandList.append(5)#Decrease distance to wall(LESS)

                    if InstructionList[InstructionListnum][ListNum+2] == "checkpoint":#This chunk checks to change the course towards a checkpoint
                        if InstructionList[InstructionListnum][ListNum+3] == "greater":
                            InstructionList[InstructionListnum][ListNum+4] = int(InstructionList[InstructionListnum][ListNum+4])
                            if InstructionList[InstructionListnum][ListNum+4] <= car.dist_to_checkpoint:
                                NumList.append(InstructionList[InstructionListnum][ListNum+4])#Records all number occurances
                                if InstructionList[InstructionListnum+1][ListNum] == "increase":#Turn car away from checkpoint
                                    CommandList.append(6)#Increase distance to checkpoint(MORE)
                                if InstructionList[InstructionListnum+1][ListNum] == "decrease":#Turn car toward checkpoint
                                    CommandList.append(7)#increase distance to checkpoint(MORE)
                            

                        if InstructionList[InstructionListnum][ListNum+3] == "less":
                            InstructionList[InstructionListnum][ListNum+4] = int(InstructionList[InstructionListnum][ListNum+4])
                            if InstructionList[InstructionListnum][ListNum+4] >= car.dist_to_checkpoint:
                                NumList.append(InstructionList[InstructionListnum][ListNum+4])#Records all number occurances
                                if InstructionListnum + 1 <= len(InstructionList):
                                    if InstructionList[InstructionListnum+1][ListNum] == "increase":#Turn car away from checkpoint
                                        CommandList.append(8)#Increase distance to checkpoint(MORE)
                                    if InstructionList[InstructionListnum+1][ListNum] == "decrease":#Turn car toward checkpoint
                                        CommandList.append(9)#Increase distance to checkpoint(MORE)
                
        if NumList != None:
            return CommandList, NumList

    def command(CommandList, DistList, car, acc, reverse, turnleft, turnright):
        CommandListnum = 0
        wordnum = 0
        angle = 40

        #These check to see if the command is currently being used

        for CommandListnum in range(len(CommandList)):
            if (CommandList[CommandListnum] == 0) and (acc != True):#Accelerate the car
                ev = pygame.event.Event ( pygame.USEREVENT + 2 )
                return pygame.event.post(ev)

            if (CommandList[CommandListnum] == 1) and (reverse != True):#Breaking, then going in reverese
                ev = pygame.event.Event ( pygame.USEREVENT + 3 )
                return pygame.event.post(ev)
            
            if (CommandList[CommandListnum] == 2) and (DistList[wordnum] <= car.dist_to_wall):
                ev = pygame.event.Event ( CommandCall.turn_away(car, turnleft, turnright, 2))
                wordnum += 1
                if ev != pygame.USEREVENT+4:
                    return pygame.event.post(ev)
            
            if (CommandList[CommandListnum] == 3) and (DistList[wordnum] <= car.dist_to_wall):
                ev = pygame.event.Event ( CommandCall.turn_towards(car, turnleft, turnright, 2))
                wordnum += 1
                if ev != pygame.USEREVENT+4:
                    return pygame.event.post(ev)
            
            if (CommandList[CommandListnum] == 4) and (DistList[wordnum] >= car.dist_to_wall):#This chunk checks to change the course to turn away from a wall
                ev = pygame.event.Event ( CommandCall.turn_away(car, turnleft, turnright, 2))
                wordnum += 1
                if ev != pygame.USEREVENT+4:
                    return pygame.event.post(ev)

            if (CommandList[CommandListnum] == 5) and (DistList[wordnum] >= car.dist_to_wall):#This chunk checks to change the course to turn away from a wall
                ev = pygame.event.Event ( CommandCall.turn_towards(car, turnleft, turnright, 2))               
                wordnum += 1
                if ev != pygame.USEREVENT+4:
                    return pygame.event.post(ev)
    
            if (CommandList[CommandListnum] == 6) and (DistList[wordnum] <= car.dist_to_checkpoint):#This chunk checks to change the course to turn away from a wall
                ev = pygame.event.Event ( CommandCall.turn_away(car, turnleft, turnright, 1))                
                wordnum += 1
                if ev != pygame.USEREVENT+4:
                    return pygame.event.post(ev)

            if (CommandList[CommandListnum] == 7) and (DistList[wordnum] <= car.dist_to_checkpoint):#This chunk checks to change the course to turn away from a wall
                ev = pygame.event.Event ( CommandCall.turn_towards(car, turnleft, turnright, 1))
                wordnum += 1
                if ev != pygame.USEREVENT+4:
                    return pygame.event.post(ev)

            if (CommandList[CommandListnum] == 8) and (DistList[wordnum] >= car.dist_to_checkpoint):#This chunk checks to change the course to turn away from a wall
                ev = pygame.event.Event ( CommandCall.turn_away(car, turnleft, turnright, 1))
                wordnum += 1
                if ev != pygame.USEREVENT+4:
                    return pygame.event.post(ev)

            if (CommandList[CommandListnum] == 9) and (DistList[wordnum] >= car.dist_to_checkpoint):#This chunk checks to change the course to turn away from a wall
                ev = pygame.event.Event ( CommandCall.turn_towards(car, turnleft, turnright, 1))
                wordnum += 1
                if ev != pygame.USEREVENT+4:
                    return pygame.event.post(ev)


