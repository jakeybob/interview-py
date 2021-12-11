from os import system
import random
import os
import json

# all the macOS system voices that are native English
EN_VOICES = ['Fiona', 'Samantha', 'Daniel', 'Alex', 'Fred', 'Karen', 'Moira', 'Tessa', 'Veena', 'Victoria']

# print(system('say -v ?'))  # list all usable voices

def say_something(voice, text, rate, **kwargs):
    """"
    Speaks (using the system level "say" command) some text, using a given voice, at a given rate (words per
    minute). An optional keyword "print" can be passed to output the voice/text to the terminal (defaults to True).

    The text and rate variables can be defined as either strings or int/floats.

    Example 1:  say_something('Fiona', 'Hello world', 300)
                Fiona says 'Hello world' at 300wpm, with voice/text printed to terminal

    Example 2:  say_something('Daniel', 87.2, '220', print=False)
                Alex says 'Eighty seven point two' at 220wpm, with nothing printed to terminal.
    """

    # force rate and text into strings if not already
    if not isinstance(rate, str):
        rate = str(rate)
    if not isinstance(text, str):
        text = str(text)

    command = 'say ' + "\"" + text + "\"" + ' -v ' + voice + ' -r ' + rate  # using slashes to escape the quote marks
    # command = command + " -o test.aiff"  #  record to file


    # test to see if keyword "print" is defined. If not defined, or set to True, print the text. If defined and set
    # to False, do not print.
    try:
        if kwargs['print']:
            print(voice + ': ' + text)
    except KeyError:
        print(voice + ': ' + text)
    finally:
        system(command)

    return None


def do_interview(voices_list, questions_dict, my_voice_name, **kwargs):
    """
    Performs a mock interview. Different voices will ask different questions randomly. They will also use a range of
    vocal speeds (somewhere between 150 and 200 words per minute by default)
    Press RETURN to move to the next question, or type 'exit' to stop the interview.

    voices = list of system level voices to use as interviewers
    questions = list of strings to be used as questions

    (Optionally, can define min_rate and max_rate as keywords to set speed range)
    List of possible voices (in macOS) can be found with this python command: print(system('say -v ?')),
    or just typing "say -v ?" into e.g. bash terminal.

    Example:
        questions_list = ['who are you?', 'what day is it?', 'why not?']
        voices_list = ['Fred', 'Tessa']
        do_interview(voices, questions, min_rate=80, max_rate=300)
    """

    questions_list = list(questions_dict)  # list of keys in dict
    random.shuffle(questions_list)  # different question order each time

    min_rate = 150  # defaults to use if not specified
    max_rate = 200

    if kwargs is not None:
        if 'min_rate' in kwargs:
            min_rate = kwargs['min_rate']

            if isinstance(min_rate, float):  # if float or string, convert to nearest int
                min_rate = round(min_rate)
            if isinstance(min_rate, str):
                min_rate = round(float(min_rate))

        if 'max_rate' in kwargs:
            max_rate = kwargs['max_rate']

            if isinstance(max_rate, float):  # if float or string, convert to nearest int
                max_rate = round(max_rate)
            if isinstance(max_rate, str):
                max_rate = round(float(max_rate))

    # check to see max is more than min. If not set them equal and print warning
    if max_rate < min_rate:
        max_rate = min_rate
        print("Maximum speaking rate was defined to be less than the minimum speaking rate!\n")
        print("All voices will speak at " + str(max_rate) + " words per minute.\n")

    for question in questions_list:
        voice = random.choice(voices_list)  # choose random voice to ask question
        rate = random.randint(min_rate, max_rate)  # choose random speech rate in this range

        say_something(voice, question, rate)

        entry = input()  # wait for user to press Return, prints blank line

        # if user enters 'quit' or 'exit' or 'q' at command prompt, break the loop
        if entry == 'exit' or entry == 'quit' or entry == 'q':
            print("Interview ended!")
            break
        if entry == 'answer' or entry == 'a':  # if user enters 'a' or 'answer' and the answer is defined, speak it
            if questions_dict[question] == "":
                pass
            else:
                say_something(my_voice_name, questions_dict[question], 175)
                input()  # wait for user to press Return, prints blank line

    return None


def save_all_as_audio(voices_list, questions_dict, my_voice_name, path_to_file):
    """quick and dirty function to output the whole thing as an audio file in a one-er"""

    min_rate = 150  # defaults to use if not specified
    max_rate = 200

    questions_list = list(questions_dict)  # list of keys in dict
    random.shuffle(questions_list)  # different question order each time

    file_id = 0
    audiofiles = []
    files = []
    for question in questions_list:
        voice = random.choice(voices_list)  # choose random voice to ask question
        rate = random.randint(min_rate, max_rate)  # choose random speech rate in this range

        file_id_str= str(file_id)

        text = str(question)
        command = 'say ' + "\"" + text + "\"" + ' -v ' + voice + ' -r ' + str(rate)

        file = file_id_str + "_" + path_to_file
        audiofiles.append('file' + """ '""" + file + """'""")
        files.append(file)

        command = command + " -o " + file  # record to file

        system(command)
        file_id = file_id + 1
        file_id_str = str(file_id)


        text = questions_dict[question]
        command = 'say ' + "\"" + text + "\"" + ' -v ' + my_voice_name + ' -r ' + '175'
        file = file_id_str + "_" + path_to_file
        audiofiles.append('file' + """ '""" + file + """'""")
        files.append(file)

        command = command + " -o " + file  # record to file

        system(command)
        file_id = file_id + 1
        file_id_str = str(file_id)

    with open('files.txt', 'w') as f:
        f.write('\n'.join(audiofiles))

    if os.path.exists('output.aiff'):
        os.remove('output.aiff')  # stops ffmpeg from asking whether to overwrite
    if os.path.exists('output.mp3'):
        os.remove('output.mp3')  # stops ffmpeg from asking whether to overwrite

    system("ffmpeg -f concat -i " + "files.txt " + "-c copy output.aiff")
    system("ffmpeg -i output.aiff -codec:a libmp3lame -qscale:a 8 output.mp3")
    # below will copy to iCloud folder "Misc"
    # system("cp output.mp3 ~/Library/Mobile\ Documents/com~apple~CloudDocs/Misc/output.mp3")

    # remove unwanted files
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    if os.path.exists('files.txt'):
        os.remove('files.txt')
    if os.path.exists('output.aiff'):
        os.remove('output.aiff')


if __name__ == "__main__":
    voices = ['Fiona', 'Samantha', 'Moira', 'Alex']     # will pick these 4 voices as interviewers
    my_voice = 'Daniel'                                 # voice used to play answers
    generic_questions = "questions_generic.json"        # path to json file of general questions
    specific_questions = "questions_specific.json"      # path to json file of questions specific to interview

    with open(generic_questions) as fp:
        GENERIC_INTERVIEW_QUESTIONS = json.load(fp)
    with open(specific_questions) as fp:
        SPECIFIC_INTERVIEW_QUESTIONS = json.load(fp)

    # join (for dupes, entry in 2nd dict takes precedence)
    questions = {**GENERIC_INTERVIEW_QUESTIONS, **SPECIFIC_INTERVIEW_QUESTIONS}

    # comment in/out below for functionality
    # do_interview(voices, questions, my_voice, min_rate=150, max_rate=250)   # performs interactive interview
    save_all_as_audio(voices, questions, my_voice, 'test.aiff')            # write out a full interview to output.mp3


