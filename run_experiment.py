from psychopy import visual, event, core
import numpy as np

def experiment():
    """
    Main function for the experiment
    """
    win = visual.Window([1400, 1000], screen=0, color='black', pos=[200,100], units='pix')

    # create a fixation dot
    fix = visual.Circle(win, radius=10, color=(1, 1, 1))

    # generate trials
    trials = generate_trials(6)

    # first instructions
    instruction_text1 ='''In this experiment, you need to choose between two shapes using the [F] and [J] keys of the keyboard for the left and right options respectively.\n
    Pick the shape that gives the largest reward.\n
    Press any key to continue.'''
    instructions1 = visual.TextStim(win, text=instruction_text1, pos=(0, 150), color=(1, 1, 1), height=30, wrapWidth=1000)
    instructions1.draw()
    fix.draw()
    win.flip()
    event.waitKeys()

    # second instructions
    instruction_text2 = 'Please fixate the white dot in the middle of the screen in between trials.\n\nPress any key to start.'
    instructions2 = visual.TextStim(win, text= instruction_text2,
                                    pos=(0, 150), color=(1, 1, 1), height=30, wrapWidth=1000)
    instructions2.draw()
    fix.draw()
    win.flip()
    event.waitKeys()

    # actual experiment
    for state in ['pre', 'post']:
        correct_shape = trials[state]['correct_shape']
        for trial in range(len(trials[state]['correct_shape_position'])):
            # draw fixation dot
            fix.draw()
            win.flip()
            core.wait(0.5)

            # create shapes at correct position depending on conditions
            circle_pos = (-200, 0) if (correct_shape == 'circle') == (trials[state]['correct_shape_position'][trial] == 1) else (200, 0)
            square_pos = (200, 0) if (correct_shape == 'circle') == (trials[state]['correct_shape_position'][trial] == 1) else (-200, 0)
            circle = visual.Circle(win, radius=75, fillColor=(1, 0, 0), pos=circle_pos)
            square = visual.Rect(win, width=150, height=150, fillColor=(0, 1, 0), pos=square_pos)

            # draw shapes
            circle.draw()
            square.draw()
            win.flip()

            # get response
            keys = event.waitKeys(keyList=['f', 'j'])
            response = 'left' if keys[0] == 'f' else 'right'

            # check if correct
            correct = 1 if response == 'left' and trials[state]['correct_shape_position'][trial] == 1 or \
                           response == 'right' and trials[state]['correct_shape_position'][trial] == 0 else 0

            # give feedback
            feedback = visual.TextStim(win, text='+ 100' if correct else '+ 0',
                                       pos=(0, 0), color=(1, 1, 1), height=50, wrapWidth=1000)
            feedback.draw()
            win.flip()
            core.wait(0.5)

            # ITI
            fix.draw()
            win.flip()
            core.wait(0.5)

def generate_trials(max_trials=50):
    """
    Function to generate trials for both pre and post reversal
    returns trials, a dictionary with pre and post reversal trials
    """
    correct_shape_pre = np.random.choice(['circle', 'square'])
    correct_shape_post = 'square' if correct_shape_pre == 'circle' else 'circle'

    half_max_trials = max_trials // 2
    shape_placement = np.concatenate([np.ones(half_max_trials), np.zeros(max_trials-half_max_trials)])
    correct_shape_position_pre = np.random.permutation(shape_placement)
    correct_shape_position_post = np.random.permutation(shape_placement)

    trials = {'pre': {'correct_shape': correct_shape_pre,
                      'correct_shape_position': correct_shape_position_pre},
              'post': {'correct_shape': correct_shape_post,
                       'correct_shape_position': correct_shape_position_post}}

    return trials

if __name__ == '__main__':
    experiment()
