from psychopy import visual, event, core, data
import numpy as np
import os

def experiment(participant_name, output_dir, trials_per_phase, p_correct, p_incorrect, response_window):
    """
    Main function for the experiment

    Args
        participant_name (string): The name of the participant
        output_dir (string): The directory where the experiment output will be saved
        trials_per_phase (int): The number of trials to run in the experiment
        p_correct (float): Probability of receiving a correct reward.
        p_incorrect (float): Probability of receiving an incorrect reward.
        response_window (float): The time window for the participant to respond to a trial (in seconds).
    """

    win = visual.Window(
        [1400, 1000], screen=0, color="black", pos=[200, 100], units="pix"
    )

    # create a fixation dot
    fix = visual.Circle(win, radius=5, color=(1, 1, 1))

    # generate trials
    trials = generate_trials(trials_per_phase, p_correct, p_incorrect)

    # first instructions
    instruction_text1 = """In this experiment, you need to choose between two shapes using the [F] and [J] keys of the keyboard for the left and right options respectively.\n
    Your goal is to maximize your points.\n\n
    Press any key to continue."""
    instructions1 = visual.TextStim(
        win,
        text=instruction_text1,
        pos=(0, 300),
        color=(1, 1, 1),
        height=40,
        wrapWidth=1200,
    )
    instructions1.draw()
    fix.draw()
    win.flip()
    event.waitKeys()

    # second instructions
    instruction_text2 = "Please fixate the white dot in the middle of the screen in between trials.\n\nPress any key to start."
    instructions2 = visual.TextStim(
        win,
        text=instruction_text2,
        pos=(0, 300),
        color=(1, 1, 1),
        height=40,
        wrapWidth=1200,
    )
    instructions2.draw()
    fix.draw()
    win.flip()
    event.waitKeys()

    # create a file to store data
    log_file_path = create_log_file(participant_name, output_dir)
    log_file = open(log_file_path, "w")
    log_file.write(
        "trial_nr,phase,correct_shape,correct_shape_position,correct_reward,incorrect_reward,response,correct,rewarded,response_time\n"
    )

    # create trial handler
    trial_handler = data.TrialHandler(trials, nReps=1, method="sequential")

    # actual experiment
    for trial_nr, trial in enumerate(trial_handler):
        correct_shape = trial["correct_shape"]
        correct_shape_position = trial["correct_shape_position"]

        # draw fixation dot
        fix.draw()
        win.flip()
        core.wait(0.5)

        # create shapes at correct position depending on conditions
        circle_pos = (
            (-200, 0)
            if (correct_shape == "circle") == (correct_shape_position == 1)
            else (200, 0)
        )
        square_pos = (
            (200, 0)
            if (correct_shape == "circle") == (correct_shape_position == 1)
            else (-200, 0)
        )
        circle = visual.Circle(win, radius=75, fillColor=(1, 1, 0), pos=circle_pos)
        square = visual.Rect(
            win, width=150, height=150, fillColor=(0, 0, 1), pos=square_pos
        )

        # draw shapes
        circle.draw()
        square.draw()
        win.flip()

        # get response within a time window
        # create a new clock at each trial to reset the time
        response_clock = core.Clock()

        # wait for response and record it
        keys = event.waitKeys(
            keyList=["f", "j"], maxWait=response_window, timeStamped=response_clock
        )  # Reset the clock and clear previous events
        if keys:
            response = "left" if keys[0][0] == "f" else "right"
            response_time = keys[0][1]
        else:
            response = "no response"
            response_time = None

        # check if correct
        correct = (
            1
            if response == "left"
            and correct_shape_position == 1
            or response == "right"
            and correct_shape_position == 0
            else 0
        )
        # check if rewarded
        rewarded = (
            1
            if correct
            and trial["correct_reward"]
            or not correct
            and trial["incorrect_reward"]
            else 0
        )

        # write to log file
        log_file.write(
            f'{trial_nr},{trial["state"]},{correct_shape},{correct_shape_position},{trial["correct_reward"]},{trial["incorrect_reward"]},{response},{correct},{rewarded},{response_time}\n'
        )

        # give feedback
        if response_time is not None:
            feedback_text = (
                f"+ {rewarded * 100}"
            )
        else:
            feedback_text = "Too slow!\n\n+ 0"

        feedback = visual.TextStim(
            win,
            text=feedback_text,
            pos=(0, 0),
            color=(1, 1, 1),
            height=50,
            wrapWidth=1200,
        )
        feedback.draw()
        win.flip()
        core.wait(0.5)

        # ITI
        fix.draw()
        win.flip()
        core.wait(0.5)

    # end of experiment
    instruction_text3 = "Thank you for your participation!"
    instructions3 = visual.TextStim(
        win,
        text=instruction_text3,
        pos=(0, 150),
        color=(1, 1, 1),
        height=50,
        wrapWidth=1200,
    )
    instructions3.draw()
    win.flip()
    core.wait(3)

    # close the log file and quit psychopy
    log_file.close()
    core.quit()

def generate_trials(trials_per_phase, p_correct, p_incorrect):
    """
    Generates trials for both pre and post reversal phases
    
    Args:
        trials_per_phase (int): Number of trials per phase.
        p_correct (float): Probability of receiving a correct reward.
        p_incorrect (float): Probability of receiving an incorrect reward.
        
    
    Returns:
        list: List of trial dictionaries containing information about each trial.
            Each trial dictionary has the following keys:
            - "state": The state of the trial ("pre" or "post").
            - "correct_shape": The correct shape for the trial ("circle" or "square").
            - "correct_shape_position": The correct shape position for the trial (0 or 1).
            - "correct_reward": If the correct response is rewarded.
            - "incorrect_reward": If the incorrect response is rewarded.
    """

    # choose which shape is correct for pre and post reversal
    correct_shape_pre = np.random.choice(["circle", "square"])
    correct_shape_post = "square" if correct_shape_pre == "circle" else "circle"

    # randomize the positions of the shapes, it's randomized within each phase
    half_trials = trials_per_phase // 2
    shape_positions = np.concatenate(
        [np.ones(half_trials), np.zeros(trials_per_phase - half_trials)]
    )
    correct_shape_position_pre = np.random.permutation(shape_positions)
    correct_shape_position_post = np.random.permutation(shape_positions)

    # create trials
    trials = []
    for i in range(trials_per_phase):
        trial = {
            "state": "pre",
            "correct_shape": correct_shape_pre,
            "correct_shape_position": correct_shape_position_pre[i],
        }
        trials.append(trial)
    for i in range(trials_per_phase):
        trial = {
            "state": "post",
            "correct_shape": correct_shape_post,
            "correct_shape_position": correct_shape_position_post[i],
        }
        trials.append(trial)

    # add stochastic rewards
    for trial in trials:
        trial["correct_reward"] = stochastic_rewards(p_correct)
        trial["incorrect_reward"] = stochastic_rewards(p_incorrect)

    return trials

def stochastic_rewards(p_reward):
    """
    Generates stochastic rewards
    
    Args:
        p_reward (float): The probability of getting a reward
    
    Returns:
        1 if a reward is obtained, 0 otherwise
    """
    if np.random.random() < p_reward:
        return 1
    else:
        return 0
    
def create_log_file(participant_name, output_dir):
    """
    Creates a log file name
    
    Args
        participant_name (string): Name of the participant
        output_dir (string): Directory where the log file will be created')
    
    Returns
        Path of the created log file
    """
    # Create the data directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a file name for the log file
    run = 0
    log_file_path = os.path.join(output_dir, f'{participant_name}_run_{run}.csv')
    
    # Check if a log file already exists for this participant with run 0
    while os.path.exists(log_file_path):
        run += 1
        log_file_path = os.path.join(output_dir, f'{participant_name}_run_{run}.csv')

    return log_file_path

