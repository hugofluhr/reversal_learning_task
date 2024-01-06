import argparse
from experiment import experiment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--participant", help="Name of the participant")
    parser.add_argument("-o", "--output_dir", help="Directory where the log file will be created (default is 'data/')", default='data/')
    parser.add_argument("-n", "--num_trials", help="Number of trials per phase (default is 30)", default=30)
    parser.add_argument("-pc", "--p_correct", help="Probability of a correct response (default is 0.8)", default=0.8)
    parser.add_argument("-pi", "--p_incorrect", help="Probability of an incorrect response (default is 0.2)", default=0.2)

    args = parser.parse_args()
    participant_name = args.participant
    output_dir = args.output_dir
    num_trials = int(args.num_trials)
    p_correct = float(args.p_correct)
    p_incorrect = float(args.p_incorrect)

    if not participant_name:
        parser.error("Participant name is required.")

    experiment(participant_name, output_dir, num_trials, p_correct, p_incorrect)

