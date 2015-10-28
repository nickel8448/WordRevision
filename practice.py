# importing the required libraries
import csv  # to read the CSV which has the words
import sys  # to read command line arguments
import random  # to generate a random list to put the words in a random order
import datetime  # to read the date from the CSV
from os import system  # to give commands to the computer, for example the say command
from os import path  # to know if the file exists on the system or not
from time import sleep  # to make the program pause


def _get_character_pairs(text):
    """Returns a defaultdict(int) of adjacent character pair counts.

    >>> _get_character_pairs('Test is')
    {'IS': 1, 'TE': 1, 'ES': 1, 'ST': 1}
    >>> _get_character_pairs('Test 123')
    {'23': 1, '12': 1, 'TE': 1, 'ES': 1, 'ST': 1}
    >>> _get_character_pairs('Test TEST')
    {'TE': 2, 'ES': 2, 'ST': 2}
    >>> _get_character_pairs('ai a al a')
    {'AI': 1, 'AL': 1}
    >>> _get_character_pairs('12345')
    {'34': 1, '12': 1, '45': 1, '23': 1}
    >>> _get_character_pairs('A')
    {}
    >>> _get_character_pairs('A B')
    {}
    >>> _get_character_pairs(123)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "strikeamatch.py", line 31, in _get_character_pairs
        if not hasattr(text, "upper"): raise ValueError
    ValueError: Invalid argument

    """

    if not hasattr(text, "upper"):
        raise ValueError("Invalid argument")

    results = dict()

    for word in text.upper().split():
        '''This function is used for
        splitting the word and making them in paid
        '''
        for pair in [word[i]+word[i+1] for i in range(len(word)-1)]:
            if pair in results:
                results[pair] += 1
            else:
                results[pair] = 1
    return results


def compare_strings(string1, string2):
    """Returns a value between 0.0 and 1.0 indicating the similarity between the
    two strings. A value of 1.0 is a perfect match and 0.0 is no similarity.

    >>> for w in ('Sealed', 'Healthy', 'Heard', 'Herded', 'Help', 'Sold'):
    ...     compare_strings('Healed', w)
    ...
    0.8
    0.5454545454545454
    0.4444444444444444
    0.4
    0.25
    0.0
    >>> compare_strings("Horse", "Horse box")
    0.8
    >>> compare_strings("Horse BOX", "Horse box")
    1.0
    >>> compare_strings("ABCD", "AB") == compare_strings("AB", "ABCD")
    True


    """
    s1_pairs = _get_character_pairs(string1)
    s2_pairs = _get_character_pairs(string2)

    s1_size = sum(s1_pairs.values())
    s2_size = sum(s2_pairs.values())

    intersection_count = 0

    # determine the smallest dict to optimise the calculation of the
    # intersection.
    if s1_size < s2_size:
        smaller_dict = s1_pairs
        larger_dict = s2_pairs
    else:
        smaller_dict = s2_pairs
        larger_dict = s1_pairs

    # determine the intersection by counting the subtractions we make from both
    # dicts.
    for pair, smaller_pair_count in smaller_dict.items():
        if pair in larger_dict and larger_dict[pair] > 0:
            if smaller_pair_count < larger_dict[pair]:
                intersection_count += smaller_pair_count
            else:
                intersection_count += larger_dict[pair]

    return (2.0 * intersection_count) / (s1_size + s2_size)


def timeaddition(date, numdays):
    """
    Adds number to days to a given date
    :param date: Date
    :param numdays: int
    :return: True or False
    """
    if (datetime.datetime.strptime(date, "%d/%m/%Y") + datetime.timedelta(days=int(numdays))).strftime("%d/%m/%Y") == datetime.datetime.today().strftime("%d/%m/%Y"):  # Adding number of days to the date and checking if today's date matches with it
        return True
    else:
        return False


def option():
    """
    Gives an option to the user
    :return: Chosen Option, int
    """
    system('clear')  # Set a system command to clear the window
    while True:  # True to keep running the loop till the user gives correct input
        try:
            opt = int(raw_input("Enter 1 to revise meanings or 2 to revise words: "))  # Giving the user an option
            if opt == 1 or opt == 2:  # Checking if he has given correct option
                break
            else:
                continue
        except ValueError:  # if an error is occured then an exception will be thrown
            print "Please enter either 1 or 2."
            continue
    while True:  # True to keep running the loop till the user gives correct input
        try:
            opt2 = int(raw_input("Enter 1 to revise for the day or 2 to all: "))  # Giving the user an option
            if opt2 == 1 or opt2 == 2:  # Checking if he has given correct option
                break
            else:
                continue
        except ValueError:  # if an error is occured then an exception will be thrown
            print "Please enter either 1 or 2."
            continue
    return opt, opt2


def main():
    """
    The main function of the program
    :return: None
    """
    openFile = open(sys.argv[1], 'rb')  # Take the file in command line argument
    csvFile = csv.reader(openFile, delimiter='\t')  # Read the file as a CSV
    row_count = 0  # A variable to count the number of rows in the CSV
    words = []  # Empty list to get the words in it
    opt, opt2 = option()
    sentences = []  # Empty list to store sentences in it
    for data in csvFile:  # Loop to get all the Words in the list
        if "Date of Learning" in data:
            pass
        else:
            if opt2 == 1:
                try:
                    if timeaddition(data[2], 2) or timeaddition(data[2], 3) or timeaddition(data[2], 5) or timeaddition(data[2], 7) or timeaddition(data[2], 15) or timeaddition(data[2], 10) or timeaddition(data[2], 20) or timeaddition(data[2], 40) or timeaddition(data[2], 50) or timeaddition(data[2], 30) or timeaddition(data[2], 60) or timeaddition(data[2], 90) or timeaddition(data[2], 120) or timeaddition(data[2], 150):  # Checking which words to revise today
                        words.append(data)  # Add the words to the list which are required to be studied today
                        row_count += 1  # Augmented statement to keep adding the number of rows
                except ValueError:
                    print "Error with entry : %s" % str(data[2])
            elif opt2 == 2:  # To revise all the words and not only for the day
                try:
                    words.append(data)
                    row_count += 1
                except ValueError:
                    print "Error with entry : %s" % str(data[2])
    randomList = random.sample(range(row_count), row_count)  # sample will get unique elements for the list
    if words != []:  # If the words list is not empty then go to the loop
        tries = 0  # A variable to count the number of tries
        counter = 1  # Counter to see the number of words being revised
        if opt == 1:  # Checking which option has been choosen and countinuing with it
            for num in randomList:  # Iterate through the random list
                print "Word learnt on : %s" % (str(words[num][2]).strip())
                print "%d. Meaning of the word : %s" % (counter, str(words[num][1]).strip())  # Print the meaning of the word
                while True:  # Start an infinite loop because we don't know how many tries the user will take to guess the correct word
                    try:
                        word = str(raw_input("Word : "))  # Take an input for the word
                    except ValueError:  # If a string value is not entered
                        print "Please enter a correct value."
                        continue
                    if str(word).strip() == str(words[num][0]).strip():  # If he enters the correct word
                        print "Correct. :)"  # Print that the word he entered was correct
                        system('say %s --voice=Samantha --rate=60' % str(words[num][0]))  # Make the computer say the word
                        tries = 0  # Set the number of tries to 0
                        while True:
                            sentence = raw_input("Make a sentence with the word : \n")  # Ask the user to make a sentence with the word
                            sentence = sentence.lower()
                            if word in sentence and len(sentence.split()) >= 2:  # Check if the user made a proper sentece or not
                                sentences.append(sentence)
                                break  # break the loop if he did
                            elif len(sentence.split()) < 4:  # if the sentence is just a single word then of course it's not a legitimate sentence
                                print ("Make a proper sentence please.")
                            else:
                                continue
                        break
                    else:
                        print "The current word is "+str(round(float(compare_strings(str(word), str(words[num][0])))*100))+"% similar to the word entered. Try again."  # Asking user to try again if he hasn't guessed the right word
                        tries += 1  # Augmented statement to keep adding the number of tries
                    if tries >= 5:  # If the tries are 5 or more than 5 then give a hint
                        print "The first two letters of the word are %s" % words[num][0][:2]  # Printing the first letter of the word as a hint
                counter += 1
                print "-" * 25
        else:
            for num in randomList:  # Iterating through the random generated list
                print "Date of learning : %s" % (words[num][2])  # Printing the date of leaning
                print "%d. Word is : %s" % (counter, str(words[num][0]).strip())  # Print the word
                raw_input("Press Enter to continue.")  # Ask user to press enter to reveal the meaning
                system('say %s --voice=Samantha --rate=60' % str(words[num][0]))  # Make the computer say the word
                print "Meaning of the word : %s" % (str(words[num][1]).strip())  # Print the meaning of the word
                raw_input("Press Enter for the next word.")  # Asking enter to continue
                print "-" * 25
                counter += 1  # Augmented statement to keep the counter running
        print "Done for the day."
        counter = 1
        if opt == 1:
            raw_input("Press Enter to read the sentences.")
            print "-" * 25
            for data in sentences:
                print  str(counter) + ". " + data
                raw_input()
                print "-" * 25
                counter += 1
        sleep(1)  # Making the program sleep for 5 seconds
        raw_input("Press Enter to end the program.")
        exit(0)  # Exit after it's done
    else:
        print "No words for the day."  # There is nothing to revise
        sleep(15)
    exit(0)


if __name__ == "__main__":
    main()
