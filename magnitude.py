import os
import fnmatch


def count_lines_and_characters(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = sum(1 for _ in f)
        f.seek(0)
        contents = f.read()
        length = len(contents)
    return lines, length


def format_number(num):
    num_str = str(num)
    formatted_num = ''
    for i in range(len(num_str)):
        if i > 0 and (len(num_str) - i) % 3 == 0:
            formatted_num += '.'
        formatted_num += num_str[i]
    return formatted_num


def is_excluded(filename, exclude_list):
    for pattern in exclude_list:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def main(directory_path, exclude_list):
    file_data = []
    total_lines = 0
    total_letters = 0
    total_files = 0
    total_dirs = 0

    for dirpath, dirnames, filenames in os.walk(directory_path):
        if '.git' in dirnames:
            dirnames.remove('.git')
        if '.idea' in dirnames:
            dirnames.remove('.idea')

        total_dirs += len(dirnames)

        for filename in filenames:
            if filename.endswith('.py') and not is_excluded(filename, exclude_list):
                total_files += 1
                filepath = os.path.join(dirpath, filename)
                lines, length = count_lines_and_characters(filepath)
                file_data.append((filename, lines, length))
                total_lines += lines
                total_letters += length

    file_data.sort(key=lambda x: x[2], reverse=True)  # Sort by letter count

    for filename, lines, length in file_data:
        print(f'letters: {format_number(length).zfill(5)}, lines: {format_number(lines).zfill(3)}, filename: {filename}')

    print(f'Total letters in code: {format_number(total_letters)}')
    print(f'Total lines of code: {format_number(total_lines)}')
    print(f'Total number of .py files: {format_number(total_files)}')
    print(f'Total number of directories: {format_number(total_dirs)}')


if __name__ == '__main__':
    path = '.'  # Replace with the directory path you're interested in
    exclude_list = ['androidAutomate*.py',]  # Add filenames or patterns to exclude
    main(path, exclude_list)
