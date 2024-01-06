import argparse
from experiment import experiment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--participant", help="Name of the participant")
    args = parser.parse_args()
    participant_name = args.participant

    if not participant_name:
        parser.error("Participant name is required.")

    experiment(participant_name)

