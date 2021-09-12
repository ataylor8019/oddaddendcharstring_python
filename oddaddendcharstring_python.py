# Odd addend character string
# Common problem statement: given an integer X between 1 and some number,
# generate a string of random characters containing X characters such that
# each individual character appears an odd number of times.

#
#
# By: Allan Taylor
# 09/12/2021
import random
import string


# Primary driver entry point. Function calls the 3 functions that generate
# the collection of odd addends, letters to be selected, and the final
# string of letters to be output to the user.
def randomLetterStringGenerator(numberToSum):
    oddAddendList = getListOfOddAddends(numberToSum)    # Get list of odd numbers that sum to desired number.
    if (oddAddendList is None):
        return None

    letterSampleList = getRandomLetterSample(len(oddAddendList))    # Get list of letters that will be chosen from (more efficient to choose randomly from this list than randomly from all 26 letters).
    if (letterSampleList is None):
        return None

    letterString = getRandomLetterString(letterSampleList, oddAddendList, numberToSum)    #Get string of letters made of letters generated in letterSampleList appearing the number of times specified by the values in oddAddendList.
    if (letterString is None):
        return None

    return letterString    # If an actual list is returned, all of the above functions worked. Otherwise None will be returned, and an error message will be output.


# Function responsible for splitting our initial sum into a collection of odd addends.
def getListOfOddAddends(numberToSum):
    if (numberToSum <= 0):    # If the number given to sum is less than or equal to zero, returns None, which will cause the program to exit with user notification.
        return None

    originalNumber = numberToSum    # Assign parameter to local variable to avoid any possibility of side effects
    workNumber = numberToSum    # Assign parameter to local variable to avoid any possibility of side effects
    numberOfAddends = 0    # Variable to tally number of addends - if we have more than 26 we should stop splitting the sum randomly and stick the remainder of the calculation in the list in a manner to be described below.
    returnList = list()    # The list of numbers we will return.

    while ((workNumber > 0) and (numberOfAddends < 26)):    # If the workNumber (the number to sum) is still greater than zero, and we have less than 26 addends, have another pass at the algorithm.
        candidate = random.randint(1, workNumber)    #Pick a number between 1 and the work number inclusive. If it's an even number, pick the next number down. This guarantees that the number is smaller than workNumber, even if workNumber is even, and it gives us another chance to pick an odd number to create an even sum if numberToSum is even.
        if (candidate % 2 == 0):
            candidate-=1

        returnList.append(candidate)    # We are guaranteed to have an odd number here, therefore append it to the list to return

        workNumber-=candidate    # Decrease the workNumber by the amount of the candidate number
        numberOfAddends+=1    # Increase the numberOfAddends variable by 1

        if (numberOfAddends == 26):    # If we have 26 addends, exit this part of the algorithm, we have more numbers to assign than we have letters in the alphabet.
            break

        if (workNumber % 2 == 0):    # If workNumber is even, have another pass at the algorithm. In the case of workNumber == zero, have another pass anyway, as the while loop will simply end.
            continue
        else:
            coinFlip = random.randint(1, 2)    # If workNumber is odd, perform a coin flip as to whether or not to continue subdividing: can technically end here, as the number(s) in the list already is/are guaranteed to be odd. If coin flip comes up 1, exit the loop, otherwise continue dividing into more addends.
            if (coinFlip == 1):
                returnList.append(workNumber)
                workNumber=0
                break

    # In the case that we have as many addends as we have letters in the alphabet, and workNumber may not be zero yet:
    if (numberOfAddends == 26):
        i=0    # counter to be used to cycle through returnList
        if (workNumber % 2 == 1):    # If workNumber is odd, then remove the last entry from returnList (which is guaranteed to be odd), and add it to workNumber (which we just determined to be odd). This creates an even workNumber, and lets us perform the last operation without needing to explicitly check for an even workNumber.
            workNumber+=returnList[25]
            returnList.pop(25)

        while (workNumber > 0):    # If here, workNumber is guaranteed to be even. At this point, we cycle through returnList, and just add 2 to each existing odd entry in the list, keeping the entries odd, and shrinking workNumber down to zero in increments of 2.
                listLen = len(returnList)
                returnList[i]+=2
                workNumber-=2
                i = (i + 1) % listLen    # Used to ensure we don't cycle past returnList's list size. Every listLen entries i is reset to 0, whether i is 25 or 26 entries long.


    return returnList


# Function responsible for generating random samples of letters to pick.
def getRandomLetterSample(letterCount):
    letterCollection = list(string.ascii_lowercase)    # create list of lowercase letters to pick from
    randomLetters = list()    # will hold list of letters we select
    usedLetters = list()    # will hold list of numbers representing already selected numbers
    
    while (len(randomLetters) < letterCount):    # Loop while we have not selected a collection of letters equal to our letter count yet.
        nextChar = random.randint(0,25)    # Pick a number between 0 and 25 inclusive (the number represents a value in our letterCollection list)
        if (not(nextChar in usedLetters)):    # If the number hasn't been picked already, append the value in the letterCollection variable equal to the number selected, toss the number in the usedLetters list
            randomLetters.append(letterCollection[nextChar])
            usedLetters.append(nextChar)

    return randomLetters    

# Function that creates the string of random letters
def getRandomLetterString(randomLetterList, randomLetterCountList, sumToReach):    # Function takes the list of random letters, the list of odd addends generated, and the sum these addends should total to as arguments
    if (len(randomLetterList) != len(randomLetterCountList)):    #If the lengths of the letter list and the odd addends list are different, something is wrong, return None, which will end the program
        return None

    sumToReachCounter = sumToReach    # Assign parameter to local variable to avoid any possibility of side effects
    returnRandomLetterString = str()    # Creates string to hold selected random letters
    lettersToSelect = len(randomLetterList)-1   # Creates a limit which will be used to select random letters from list variable randomLetterList  

    while (sumToReachCounter > 0):    # pick letters from randomLetterList variable, decrement corresponding count value in randomLetterCountList every time the letter is picked, decrease the sumToReach counter. Skip letter if corresponding count value in randomLetterCountList is zero. When sumToReachCounter is zero, all letters have been picked the proper number of times.
        nextChar = random.randint(0,lettersToSelect)
        if (randomLetterCountList[nextChar] > 0):
            returnRandomLetterString += randomLetterList[nextChar]
            randomLetterCountList[nextChar] -= 1
            sumToReachCounter -= 1
        else:
            continue    # If here, randomLetterCountList value corresponding to the letter in randomLetterList is zero, pick another letter

    return returnRandomLetterString




# Main program script



letterStringLength = int(input("Please enter a number. A string of letters consisting of odd values of characters will be generated: "))    # Prompt for number of characters in string
stringOutput = randomLetterStringGenerator(letterStringLength)    # get string of random characters

stringDescription = str()    # Create string holding final output

if (stringOutput is None):
    stringDescription = "String is empty or was not generated."    # If here, there was a problem with the user input or generating the list, notify that string is empty or not generated.
else:
    stringDescription = "The following random sequence of characters was generated: " + stringOutput    # If here, the string was generated, put prompt and string output in the same variable.

print(stringDescription)    # Print stringDescription variable