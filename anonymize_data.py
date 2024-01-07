# This script anonymizes the data by renaming the files in the data directory.

import os

directory = 'data/'
prefix = 'subj_'

# Get the list of files in the directory
files = os.listdir(directory)

# Sort the files alphabetically
files.sort()

# Rename the files
for i, file in enumerate(files):
    # Generate the new filename
    new_filename = f'{prefix}{i:02d}.csv'

    # Get the full path of the file
    old_path = os.path.join(directory, file)
    new_path = os.path.join(directory, new_filename)

    # Rename the file
    os.rename(old_path, new_path)
