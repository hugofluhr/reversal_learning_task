from psychopy import visual, event, core, data
import numpy as np
from textwrap import dedent


def experiment():
    """
    Main function for the experiment
    """
    win = visual.Window(
        [1400, 1000], screen=0, color="black", pos=[200, 100], units="pix"
    )

    # create a fixation dot
    fix = visual.Circle(win, radius=10, color=(1, 1, 1))

    # generate trials
    trials = generate_trials(10)

    # first instructions
    instruction_text1 = """In this experiment, you need to choose between two shapes using the [F] and [J] keys of the keyboard for the left and right options respectively.\n
    Pick the shape that gives the largest reward.\n
    Press any key to continue."""
    instructions1 = visual.TextStim(
        win,
        text=instruction_text1,
        pos=(0, 150),
        color=(1, 1, 1),
        height=30,
        wrapWidth=1000,
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
        pos=(0, 150),
        color=(1, 1, 1),
        height=30,
        wrapWidth=1000,
    )
    instructions2.draw()
    fix.draw()
    win.flip()
    event.waitKeys()

    # create a file to store data
    log_file = open("elsa_data.csv", "w")
    log_file.write(
        "trial_nr,state,correct_shape,correct_shape_position,correct_reward,incorrect_reward,response,correct,rewarded,response_time\n"
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
        circle = visual.Circle(win, radius=75, fillColor=(1, 0, 0), pos=circle_pos)
        square = visual.Rect(
            win, width=150, height=150, fillColor=(0, 1, 0), pos=square_pos
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
            keyList=["f", "j"], maxWait=1.5, timeStamped=response_clock
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
                "+ {rewarded * 100}"
            )
        else:
            feedback_text = "Too slow!\n\n+ 0"

        feedback = visual.TextStim(
            win,
            text=feedback_text,
            pos=(0, 0),
            color=(1, 1, 1),
            height=50,
            wrapWidth=1000,
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
        wrapWidth=1000,
    )
    instructions3.draw()
    win.flip()
    core.wait(2)

    # close the log file and quit psychopy
    log_file.close()
    core.quit()


def generate_trials(trials_per_phase=50, reward_ranges=((0, 60), (40, 100))):
    """
    Function to generate trials for both pre and post reversal
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
        trial["correct_reward"] = stochastic_rewards(0.7)
        trial["incorrect_reward"] = stochastic_rewards(0.3)

    return trials


def stochastic_rewards(p_reward):
    """
    Function to generate stochastic rewards
    """
    if np.random.random() < p_reward:
        return 1
    else:
        return 0


if __name__ == "__main__":
    experiment()
