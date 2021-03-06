# Import libraries
import faulthandler; faulthandler.enable()
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()

# MY VARS
trackAns = 0
value = 0
pi_pwm_LED = None
pi_pwm_buzzer = None
numGuesses = 0
userName = ""

# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    global value
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        print("████████████████████")
        print("█ Current guess: {} █".format(0))
        print("████████████████████")
        
        while not end_of_game:
            pass
        end_of_game = False
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, cleanData):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))

    # print out the scores in the required format
    for i in range(3):
        print("{} - {} took {} guesses".format(i+1, cleanData[i][0], cleanData[i][1]))

    pass


# Setup Pins
def setup():
    global pi_pwm_LED
    global pi_pwm_buzzer

    # Setup board mode
    GPIO.setmode(GPIO.BOARD)

    # Setup regular GPIO
    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for i in range(3):
        GPIO.setup(LED_value[i], GPIO.OUT) # LEDs set to output
        GPIO.output(LED_value[i], GPIO.LOW)

    # Setup PWM channels
    GPIO.setup(LED_accuracy, GPIO.OUT) # PWM LED set to output
    pi_pwm_LED = GPIO.PWM(LED_accuracy, 100) # PWM instance for LED_accuracy with frequency 1kHz
    pi_pwm_LED.start(0) # Duty cycle 0 at start()

    GPIO.setup(buzzer, GPIO.OUT) # PWM buzzer set to output
    pi_pwm_buzzer = GPIO.PWM(buzzer, 1) # Pwm instance for buzzer with frequency 250Hz
    pi_pwm_buzzer.start(0) # Duty cycle 0 at start() - changed later
    
    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_increase, GPIO.RISING, callback=btn_increase_pressed, bouncetime=250)
    GPIO.add_event_detect(btn_submit, GPIO.FALLING, callback=btn_guess_pressed, bouncetime=250)
    # Working now ... issue was GPIO.PUD_DOWN should have been GPIO.PUD_UP ... ?

    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    scoreCount = eeprom.read_byte(0)
    
    # Get the scores
    rawScores = eeprom.read_block(1, scoreCount*4)

    # convert the codes back to ascii
    cleanScores = [None]*scoreCount
    currentName = ""
    currentScore = 0
    iterCount = 0
    for i in range(len(rawScores)):
        currentScore = 0
        if (i+1)%4==0:
            currentScore = ord(chr(rawScores[i]))
        else:
            if len(currentName)==3:
                currentName = ""
                currentName += chr(rawScores[i])
            else:
                currentName += chr(rawScores[i])
        if currentScore>0:
            cleanScores[iterCount] = [currentName, currentScore]
            iterCount += 1
            
    # return back the results
    return scoreCount, cleanScores


# Save high scores
def save_scores():
    global userName
    global numGuesses

    # fetch scores
    count, scores = fetch_scores()

    # include new score
    scores.append([userName, numGuesses])

    # sort
    scores.sort(key=lambda x: x[1])
    
    # update total amount of scores
    for i, score in enumerate(scores):
        data_to_write = []
        # get the string
        for letter in score[0]:
            data_to_write.append(ord(letter))
        data_to_write.append(score[1])        
        # write new scores
        eeprom.write_block(i+1, data_to_write)

    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    global trackAns

    trackAns += 1

    if trackAns>7:
        trackAns=0

    # binAns = bin(trackAns)
    
    if trackAns==0:
        GPIO.output(LED_value[0], GPIO.LOW)
        GPIO.output(LED_value[1], GPIO.LOW)
        GPIO.output(LED_value[2], GPIO.LOW)
    elif trackAns==1:
        GPIO.output(LED_value[0], GPIO.LOW)
        GPIO.output(LED_value[1], GPIO.LOW)
        GPIO.output(LED_value[2], GPIO.HIGH)
    elif trackAns==2:
        GPIO.output(LED_value[0], GPIO.LOW)
        GPIO.output(LED_value[1], GPIO.HIGH)
        GPIO.output(LED_value[2], GPIO.LOW)
    elif trackAns==3:
        GPIO.output(LED_value[0], GPIO.LOW)
        GPIO.output(LED_value[1], GPIO.HIGH)
        GPIO.output(LED_value[2], GPIO.HIGH)
    elif trackAns==4:
        GPIO.output(LED_value[0], GPIO.HIGH)
        GPIO.output(LED_value[1], GPIO.LOW)
        GPIO.output(LED_value[2], GPIO.LOW)
    elif trackAns==5:
        GPIO.output(LED_value[0], GPIO.HIGH)
        GPIO.output(LED_value[1], GPIO.LOW)
        GPIO.output(LED_value[2], GPIO.HIGH)
    elif trackAns==6:
        GPIO.output(LED_value[0], GPIO.HIGH)
        GPIO.output(LED_value[1], GPIO.HIGH)
        GPIO.output(LED_value[2], GPIO.LOW)
    elif trackAns==7:
        GPIO.output(LED_value[0], GPIO.HIGH)
        GPIO.output(LED_value[1], GPIO.HIGH)
        GPIO.output(LED_value[2], GPIO.HIGH)

    print("\033[A                      \033[A")
    print("\033[A                      \033[A")
    print("\033[A                      \033[A")

    print("████████████████████")
    print("█ Current guess: {} █".format(trackAns))
    print("████████████████████")
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess

    pass


# Guess button
def btn_guess_pressed(channel):
    global pi_pwm_LED
    global pi_pwm_buzzer
    global trackAns
    global end_of_game
    global value
    global currentName
    global numGuesses
    global userName

    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    
    start = time.time()
    time.sleep(0.2)

    while GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.01)
    
    length = time.time()- start

    if length>2:
        if trackAns==value:
            numGuesses += 1
            print("\033[H\033[J")    
            print("██████████████████████")
            print("█       Correct!     █".format(trackAns))
            print("█ You took {} guesses █".format(numGuesses))   
            print("██████████████████████")
            
            pi_pwm_LED.stop()
            pi_pwm_buzzer.stop()
            
            userName = input("Enter your name below to join the Hall of Fame:\n")
            userName = userName[0:3]
            save_scores()
            
            end_of_game = True
        else:
            accuracy_leds()
            trigger_buzzer()
            numGuesses += 1
            print("\033[H\033[J")               
            print("██████████████████████")
            print("█Incorrect, try again!█".format(trackAns))
            print("██████████████████████")
    pass


# LED Brightness
def accuracy_leds():
    global trackAns
    global value
    global pi_pwm_LED

    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
   
    dutyCycle = 0
    if trackAns<value:
        dutyCycle = trackAns/value*100
    else:
        dutyCycle = ((8-trackAns)/(8-value))*100
    
    pi_pwm_LED.ChangeDutyCycle(dutyCycle)
    pass

# Sound Buzzer
def trigger_buzzer():
    global pi_pwm_buzzer
    global trackAns
    global value

    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    pi_pwm_buzzer.start(50)

    frequency = 0

    if abs(value-trackAns)==3:
        frequency = 1
        pi_pwm_buzzer.ChangeFrequency(frequency)
    elif abs(value-trackAns)==2:
        frequency = 2
        pi_pwm_buzzer.ChangeFrequency(frequency)
    elif abs(value-trackAns)==1:
        frequency = 4        
        pi_pwm_buzzer.ChangeFrequency(frequency)
    else:
        pi_pwm_buzzer.stop()

    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
