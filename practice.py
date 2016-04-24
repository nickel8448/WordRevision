# importing the required libraries
import csv  # to read the CSV which has the words
import sys  # to read command line arguments
import random  # to generate a random list to put the words in a random order
import datetime  # to read the date from the CSV
from os import system  # to give commands to the computer, for example the say command
from os import path  # to know if the file exists on the system or not
from time import sleep  # to make the program pause


class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'


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
    while True:
        try:
            opt3 = int(raw_input("Enter 1 to revise or 2 to add words: "))
            if opt3 == 1 or opt3 == 2:
                # Checking if he has given correct option
                opt, opt2 = 0, 0
                break
            else:
                continue
        except ValueError:
            # if an error is occured then an exception will be thrown
            print "Please enter either 1 or 2."
            continue
    if opt3 == 1:
        # True to keep running the loop till the user gives correct input
        while True:
            try:
                msg = "Enter 1 to revise meanings or 2 to revise words: "
                opt = int(raw_input(msg))  # Giving the user an option
                if opt == 1 or opt == 2:  # Checking the options
                    break
                else:
                    continue
            # if an error is occured then an exception will be thrown
            except ValueError:
                print "Please enter either 1 or 2."
                continue
        while True:  # To keep running the loop till the user gives correct input
            try:
                msg = "Enter 1 to revise for the day or 2 to all: "
                opt2 = int(raw_input(msg))  # Giving the user an option
                # Checking if he has given correct option
                if opt2 == 1 or opt2 == 2:
                    break
                else:
                    continue
            # if an error is occured then an exception will be thrown
            except ValueError:
                print "Please enter either 1 or 2."
                continue
    return opt, opt2, opt3


def writeWords(csvfile):
    try:
        maxnum = int(raw_input("Enter the number of words to be appended: "))
        print "-" * 25
    except ValueError:
        print "Please enter an integer value only."
    for num in range(0, maxnum):
        word = str(raw_input("Enter word " + str(int(num + 1)) + ": ")).lower()
        meaning = str(raw_input(
            "Enter the meaning for " + str(word) + ": ")
        ).lower()
        sentence = str(raw_input(
            "Enter sample sentence for " + str(word) + ": ")
        )
        print "-" * 25
        today = datetime.datetime.today().strftime("%d/%m/%Y")
        # if num == 0:
        #     csvfile.writerow([])
        row = [word, meaning, sentence, 0, today]
        csvfile.writerow(row)


def main():
    """
    The main function of the program
    :return: None
    """
    opt, opt2, opt3 = option()
    if opt3 == 1:
        # Take the file in command line argument
        openFile = open(sys.argv[1], 'rb')
        # Read the file as a CSV
        csvFile = csv.reader(openFile, delimiter='\t')
        row_count = 0  # A variable to count the number of rows in the CSV
        words = []  # Empty list to get the words in it
        wordsList = []
        sentences = []  # Empty list to store sentences in it
        meanings = []  # Track the meanings of the words to be revised today
        for data in csvFile:  # Loop to get all the Words in the list
            if "Times Revision" in data:
                pass
            else:
                if opt2 == 1:
                    try:
                        # Checking which words to revise today
                        if (timeaddition(data[4], 2) or
                                timeaddition(data[4], 3) or
                                timeaddition(data[4], 5) or
                                timeaddition(data[4], 7) or
                                timeaddition(data[4], 15) or
                                timeaddition(data[4], 10) or
                                timeaddition(data[4], 20) or
                                timeaddition(data[4], 40) or
                                timeaddition(data[4], 50) or
                                timeaddition(data[4], 30) or
                                timeaddition(data[4], 60) or
                                timeaddition(data[4], 90) or
                                timeaddition(data[4], 120) or
                                timeaddition(data[4], 150)):
                            words.append(data)  # Add the words to the list
                            wordsList.append(data[0])
                            # Augmented statement to count rows
                            row_count += 1
                    except ValueError:
                        print "Error with entry : %s" % str(data[4])
                # To revise all the words and not only for the day
                elif opt2 == 2:
                    try:
                        words.append(data)
                        wordsList.append(data[0])
                        row_count += 1
                    except ValueError:
                        print "Error with entry : %s" % str(data[4])
        # sample will get unique elements for the list
        randomList = random.sample(range(row_count), row_count)
        if words != []:  # If the words list is not empty then go to the loop
            tries = 1  # A variable to count the number of tries
            counter = 1  # Counter to see the number of words being revised
            # Checking which option has been choosen and countinuing with it
            if opt == 1:
                for num in randomList:# Iterate through the random list
                    print "Word learnt on : %s" % (str(words[num][4]).strip())
                    tempWord = str(words[num][1]).strip()
                    # Print the meaning of the word
                    print "%d. Meaning of the word : %s" % (counter, tempWord)
                    meanings.append(words[num][1])
                    while True:  # Start an infinite loop for tries
                        try:
                            # Take an input for the word
                            word = str(raw_input("Word : "))
                        except ValueError:  # If a string value is not entered
                            print "Please enter a correct value."
                            continue
                        # If he enters the correct word
                        if str(word).strip() == str(words[num][0]).strip():
                            print "Correct. :)"
                            cmd = 'say %s --voice=Samantha --rate=60'
                            tempWord = str(words[num][0])
                            system(cmd % tempWord)  # Say the word
                            tries = 0  # Set the number of tries to 0
                            while True:
                                msg = "Make a sentence with the word : \n"
                                # To make a sentence with the word
                                sentence = raw_input(msg)
                                sentence = sentence.lower()
                                # Check if it's a proper sentece or not
                                if (word in sentence and
                                        len(sentence.split()) >= 2):
                                    sentences.append(sentence)
                                    print ("Sample sentence : \n" +
                                        bcolors.OKGREEN +
                                        words[num][2] +
                                        bcolors.ENDC)
                                    break  # break the loop if he did
                                elif len(sentence.split()) < 4:
                                    print "Make a proper sentence please."
                                else:
                                    continue
                            break
                        else:
                            cword = compare_strings(str(word), str(words[num][0]))
                            # Try again if he hasn't guessed the right word
                            msg = "The current word is %s percent similar to the word entered."
                            print msg % str(round(float((cword)*100)))
                            tries += 1  # Augmented statement to keep adding the number of tries
                        # If the tries are 5 or more than 5 then give a hint
                        if tries >= 5:
                            msg = "The first two letters of the word are %s"
                            # Printing the first letter of the word as a hint
                            print msg % words[num][0][:2]
                    counter += 1
                    print "-" * 25
            else:
                for num in randomList:  # Iterating through the random generated list
                    # Printing the date of leaning
                    print "Date of learning : %s" % (words[num][4])
                    tmpword = str(words[num][0]).strip()
                    # Print the word
                    print "%d. Word is : %s" % (counter, tmpword)
                    raw_input("Press Enter to continue.")
                    pronword = str(words[num][0])  # Word to pronounce
                    system('say %s --voice=Samantha --rate=60' % pronword)
                    pronmean = str(words[num][1]).strip()
                    print "Meaning of the word : %s" % (pronmean)
                    raw_input("Press Enter for the next word.")
                    print "-" * 25
                    counter += 1  # Augmented statement to keep the counter running
            print "Done for the day."
            # Take the file in command line argument
            openFile = open(sys.argv[1], 'rb')
            csvFile = csv.reader(openFile, delimiter='\t')
            system("rm "+sys.argv[1])  # Remove the file
            # Open a new file with the same name
            with open(sys.argv[1], 'a') as openNFile:
                nCSV = csv.writer(openNFile, delimiter='\t')
                for data in csvFile:
                    if data[0] in wordsList:
                        data[3] = int(data[3]) + 1
                    nCSV.writerow(data)
            counter = 1
            if opt == 1:
                raw_input("Press Enter to read the sentences.")
                print "-" * 25
                for data in sentences:
                    print str(counter) + ". " + data
                    print "Meaning: " + meanings[counter - 1]
                    raw_input()
                    print "-" * 25
                    counter += 1
            sleep(1)  # Making the program sleep for 5 seconds
            raw_input("Press Enter to end the program.")
            exit(0)  # Exit after it's done
        else:
            print "No words for the day."  # There is nothing to revise
            sleep(15)
    else:
        with open(sys.argv[1], 'a') as openFile:
            openCSV = csv.writer(openFile, delimiter='\t')
            writeWords(openCSV)
    exit(0)


if __name__ == "__main__":
    main()
