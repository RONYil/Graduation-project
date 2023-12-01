import re

with open('Data_deletion_output.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

# Use a regular expression to add two newlines at the end of each data block to ensure that there are three newlines between the data blocks
file_content = re.sub(r'(禁忌[^\n]*)\n', r'\1\n\n\n', file_content)

# Write the modified content back to the file
with open('separator_output.txt', 'w', encoding='utf-8') as file:
    file.write(file_content)