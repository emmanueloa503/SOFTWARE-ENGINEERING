import os
from pathlib import Path

class HighScores:
    
    def record_score(time):
        first = ""
        second = ""
        third = ""
        changedfile = False

        time = round(time, 2)
        
        #Gets the information from the file, or creates the file
        path = Path(__file__).parent
        try:
            ScoreFile = open(str(path) + os.path.join('/',"high_scores.txt"), "r+") #Open the text file and append.
            scores = ScoreFile.readlines() #create a list where each value is a line of text from the file.scores = ScoreFile.readlines() #create a list where each value is a line of text from the file.
            ScoreFile.truncate(0)
        except:
            ScoreFile = open(str(path) + os.path.join('/',"high_scores.txt"), "x") #Creates the text file.
            scores = ["1000","1000","1000"] #set to a high number so it will always be higher than the lap timer
            print("File couldn't be found, new file was created!")

        ScoreFile.close() #closing the file.

        #Prepares list for calculations
        for line in range(len(scores)):
            scores[line] = scores[line].strip()
        for line in range(len(scores)):
            try:
                scores.remove("None")
            except:
                pass
        while len(scores) < 3:
            scores.append("1000")

        for line in range(len(scores)):#Changes the values of a list if needed
            if changedfile == False:
                if time < float(scores[0]):
                    first = str(time)
                    second = scores[0]
                    third = scores[1]
                    changedfile = True
                elif time < float(scores[1]):
                    first = scores[0]
                    second = str(time)
                    third = scores[1]
                    changedfile = True
                elif time < float(scores[2]):
                    first = scores[0]
                    second = scores[1]
                    third = str(time)
                    changedfile = True
                else:
                    first = scores[0]
                    second = scores[1]
                    third = scores[2]

        #Resets all unused values
        if first == "1000":
            first = "None"
        if second == "1000":
            second = "None"
        if third == "1000":
            third = "None"

        #print(first, second, third)

        ScoreFile = open(str(path) + os.path.join('/',"high_scores.txt"), "a")
        ScoreFile.write(first + "\n")
        ScoreFile.write(second + "\n")
        ScoreFile.write(third)
        ScoreFile.close() #closing the file.
        return 0

        

