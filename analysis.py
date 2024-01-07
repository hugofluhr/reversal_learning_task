import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import glob

def load_data(data_dir):
    """
    Load data from CSV files in the specified directory.

    Args:
        data_dir (str): The directory path where the CSV files are located.

    Returns:
        pandas.DataFrame: The combined data from all CSV files, with an additional 'subj_id' column.
    """
    # Get a list of all CSV files in the directory
    file_list = glob.glob(data_dir + '*.csv')

    # empty DataFrame to put the combined data
    data = pd.DataFrame()

    # Iterate over the files and read the data for each subject
    for file in file_list:
        subj_id = file.split('/')[-1].split('.')[0]  # Extract subject name from file path
        subject_data = pd.read_csv(file)

        # Add subject name as a column in the subject data
        subject_data['subj_id'] = subj_id

        # Append the subject data to the combined DataFrame
        data = pd.concat([data, subject_data], ignore_index=True)
    
    return data

def accuracy_barplot(data):
    """
    Generate a bar plot to visualize the accuracy pre and post reversal.

    Args:
        data (DataFrame): The data containing the accuracy values for each phase.

    Returns:
        None
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    sns.barplot(ax=ax, x='phase', y='correct', hue='phase', data=data)
    ax.set_title('Accuracy Pre and Post Reversal')
    ax.set_ylabel('Accuracy')  # Rename the y-axis

    plt.tight_layout()
    fig.savefig('figures/accuracy_barplot.png')

def accuracy_trials_plot(data):
    """
    Plot the accuracy over time.

    Args:
        data (DataFrame): The data containing the accuracy values.

    Returns:
        None
    """
    # Plot accuracy over time
    rolling_avg = data['correct'].rolling(window=10).mean()

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(ax=ax, data=data, x='trial_nr', y=rolling_avg)

    # Add a vertical red line at trial 30
    plt.axvline(x=29, color='red', label='Reversal')

    # Set the title and labels for the plot
    plt.title('Moving average of accuracy, W=10')
    plt.xlabel('Trial number')
    plt.ylabel('Accuracy')
    plt.legend()  # Add legend
    plt.tight_layout()
    fig.savefig('figures/accuracy_trials_plot.png')


def response_time_barplot(data):
    """
    Generate a bar plot of mean response times based on different phases and correctness.

    Args:
        data: DataFrame containing the response time data, with columns 'phase', 'correct', and 'response_time'.

    Returns:
        None
    """
    mean_response_times = data.groupby(['phase', 'correct'])['response_time'].mean().unstack()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(ax=ax, data=data, x='phase', y='response_time', hue='correct')
    plt.xlabel('Phase')
    plt.ylabel('Mean Response Time [s]')
    plt.tight_layout()
    fig.savefig('figures/response_time_barplot.png')

if __name__ == '__main__':
    data = load_data('data/')
    accuracy_barplot(data)
    accuracy_trials_plot(data)
    response_time_barplot(data)
    print('Done!')