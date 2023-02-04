import sys
import os
import re
import pickle

# Defining a Person class with fields: last, first, mi, id, and phone
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

#  display() method to output fields
    def display(self):
        print('\nEmployee ID    :', self.id)
        print('Employee Name  : ' + self.first + ' ' + self.mi + ' ' + self.last)
        print('Employee Phone : ' + self.phone)

    # openes the  file from a data folder
def readFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in


# return user's console input
def getInput(errorMsg):
    print(errorMsg)
    consoleResponse = input("Enter your new input: ")
    return consoleResponse


# remove the header line and return the data back to user
def removeHeader(data):
    data.reverse()
    for i in range(0, 5):
        data.pop(len(data) - 1)
    data.reverse()
    return data

#verifying the name vs the qualifications
def verifyName(name):
    if len(name) == 0:
        return verifyName(getInput("Enter a name."))
    else:
        name = re.sub(r'[^a-zA-Z]', '', name)
    return name.capitalize()


# only alpha, capital, single letter
def verifyMidInitial(middleInitial):
    middleInitial = re.sub(r'[^a-zA-Z]', '', middleInitial)  # only read the a-z and A-Z characters as MI
    middleInitial = middleInitial.upper()  # capitalize MI
    if len(middleInitial) < 1:  # if MI is empty, set as X
        middleInitial = 'X'
    return middleInitial[0]


# returning the ID with 2 uppercase letters followed by 4 digits
def verifyID(id):
    if not len(id) == 6:  # verifying length
        return verifyID(
            getInput("\nEmployee ID: " + id + " is invalid. Please enter two letters followed by four digits for a valid ID."))
    else:
        if not id[0:2].isalpha():  # verifying that first 2 are letters
            return verifyID(getInput(
                "\nEmployee ID: " + id + " is invalid. Please enter tWO letters followed by four digits for a valid ID."))
        else:
            if not id[2:6].isdigit():  # verify that last 4 are digits
                return verifyID(getInput(
                    "\nEmployee ID: " + id + " is invalid. Please enter two letters followed by four digits for a valid ID."))
            else:
                return id.upper()

            # returns a phone number with format 999-999-9999


def verifyPhone(num):
    num = re.sub('\D', '', num)  # read the numbers
    if not len(num) == 10:  # ask for a number if number is not == 10 digits
        return verifyPhone(getInput("\nPhone Number: " + num + " is invalid. Please enter a 10 digit number."))
    num = num[0:3] + '-' + num[3:6] + '-' + num[6:]  # add dashes
    return num


# process data using above methods and put it all in a dictionary, then return the dictionary
def processData(inFile):
    inFile = inFile.replace("\n", ',')  # Replace \n to ,
    data = inFile.split(',')  # split by comma
    data = removeHeader(data)  # remove first line

    i = 0
    personDict = {}
    while i < len(data):
        # LAST: capital case
        data = data[:i] + [verifyName(data[i])] + data[i + 1:]
        i += 1

        # verifying the FirstName capitalize
        data = data[:i] + [verifyName(data[i])] + data[i + 1:]
        i += 1

        # verifying the MidInitial single upper case letter
        data = data[:i] + [verifyMidInitial(data[i])] + data[i + 1:]
        i += 1

        #verfiying the ID 2 letters followed by 4 digits
        data = data[:i] + [verifyID(data[i])] + data[i + 1:]
        i += 1

        # verifying the PHONE NUMBER data: 999-999-9999
        data = data[:i] + [verifyPhone(data[i])] + data[i + 1:]
        i += 1

        # initializing variable to hold person's data
        p = Person(data[i - 5], data[i - 4], data[i - 3], data[i - 2], data[i - 1])

        # add to dictionary if id is unique of not display error
        if personDict.__contains__(p.id):
            print("Error adding: ")
            p.display()
            print("Found a duplicate id.\n")
        else:
            personDict[data[i - 2]] = p
    return personDict


# main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('File to be opened: ')
    else:
        filePath = sys.argv[1]
        fileData = readFile(filePath)
        employeeList = processData(fileData)  # process data.csv into employee list

        if len(employeeList) < 1:
            print("Error: Dictionary empty.")
        else:
            # save dict in pickle
            pickle.dump(employeeList, open('employeeList.p', 'wb'))
            # load pickle file
            employee = pickle.load(open('employeeList.p', 'rb'))
            # display pickle file
            print("\nEmployee list")
            for e in employee:
                employee[e].display()