import csv
import random

def get_user_data(name):
    # Check if user has saved data
    with open('user_data.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == name:
                likes = row['likes']
                dislikes = row['dislikes']
                birthdate = row['birthdate']
                return likes, dislikes, birthdate
    # If user is not found in file, ask for data
    likes = input("What are some things you like? ")
    dislikes = input("What are some things you dislike? ")
    birthdate = input("What's your birthdate? (MM/DD/YYYY) ")
    # Save data to file
    with open('user_data.csv', mode='a', newline='') as file:
        fieldnames = ['name', 'likes', 'dislikes', 'birthdate']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'name': name, 'likes': likes, 'dislikes': dislikes, 'birthdate': birthdate})
    return likes, dislikes, birthdate

def get_compliment():
    # Return a random compliment
    compliments = ['You are pretty cool!', 'You have a beautiful smile!', 'You are so talented!', 'Hope you are having a great day!']
    return random.choice(compliments)

def get_joke():
    # Return a random joke
    jokes = ['Why did the tomato turn red? Because it saw the salad dressing!', 'Why don’t scientists trust atoms? Because they make up everything!', 'Why did the coffee file a police report? It got mugged!', 'Why do programmers prefer dark mode? Because light attracts bugs!']
    return random.choice(jokes)

def get_lifepath_number(birthdate):
    # Calculate lifepath number based on birthdate
    birthdate = birthdate.replace("/", "")
    lifepath_number = sum(int(digit) for digit in birthdate)
    while lifepath_number > 9:
        lifepath_number = sum(int(digit) for digit in str(lifepath_number))
    return lifepath_number

def get_lifepath_meaning(lifepath_number):
    # Get lifepath meaning from CSV file
    with open('lifepath_meanings.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['lifepath_number'] == str(lifepath_number):
                return row['meaning']
    return "No meaning found for lifepath number " + str(lifepath_number)

def chatbot():
    while True:
        name = input("Hello I'm LifePath Bot, what's your name? (type 'exit' to end the program) ")
        if name == 'exit':
            print("Goodbye ," + name + "it was nice talking to you!" )
            break
        likes, dislikes, birthdate = get_user_data(name)
        print("Nice to meet you, " + name + "!")
        print(get_compliment())
        lifepath_number = get_lifepath_number(birthdate)
        print("Your lifepath number is:", lifepath_number)
        print("Your lifepath meaning is:", get_lifepath_meaning(lifepath_number))
        print("I also remember that you like", likes, "and dislike", dislikes + ".")
        print("Here's a joke to brighten your day! " + get_joke())

chatbot()