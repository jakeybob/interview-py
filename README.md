# interview-py
A python script that performs a mock job interview using macOS's system level text-to-speech.

Questions/answers are defined in the `questions_generic.json` and `questions_specific.json` files.

Script has two functions:
1. `do_interview()` will perform a mock interview using the voices defined in the script, and the questions from the .json files. Questions are asked randomly, one at a time, by different interviewers, using a range of random voice speeds etc. The question text will print to the console. If the user inputs "a" or "answer", the user's voice will then read the answer. Otherwise, pressing ENTER will advance to the next question, and entering "q", "quit" or "exit" will stop and exit.
2. `save_all_as_audio()` will save a full interview (questions and answers) as `output.mp3`. This does not involve any user interaction.


## Notes:
1. this script relies on macOS system level `say` command, and has not been tested on any other system. (I *think* `say` can be installed via e.g. `apt-get install gnustep-gui-runtime` on Debian-likes but have no idea if it works)
2. the `save_all_as_audio()` function relies on a functioning `ffmpeg` install being in the PATH
3. python version >= 3.5