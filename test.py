# import pyautogui
#
# pyautogui.screenshot('screen.png')
# import os
# # os.system('adb shell input keyevent 56')
# os.system('adb shell input text "@"')

#
# def f(x):
#     return x ** x
#
#
# def foo(x):
#     return f(x)
#
# def bar(x):
#     return foo(x)
#
# def foobar(x):
#     return bar(x)
#
# print(foobar(2))


# import pyautogui
#
# def locate_all_occurrences(needle, haystack):
#     matches = pyautogui.locateAll(needleImage=needle, haystackImage=haystack, confidence=0.95, grayscale=True, region=(30, 800, 950, 700))
#     return [match for match in matches]
#
# # Example usage:
# needle_image_path = r'.\pics\all_entered_player_name.png'
# haystack_image_path = r'.\pics\screen-5554.png'
# all_matches = locate_all_occurrences(needle_image_path, haystack_image_path)
#
# for match in all_matches:
#     print(f"Match found at {match.left}, {match.top} with width {match.width} and height {match.height}")



import subprocess

def get_cursor_position():
    try:
        adb_output = subprocess.check_output(["adb", "shell", "dumpsys", "input"])
        adb_output = adb_output.decode("utf-8")

        # Extract relevant lines
        lines = adb_output.split("\n")
        relevant_lines = [line.strip() for line in lines if "SurfaceWidth" in line or "SurfaceHeight" in line or "X:" in line or "Y:" in line]

        # TODO: Parse these lines to get the actual X, Y positions
        # This is device and Android version specific

        return relevant_lines

    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    position_info = get_cursor_position()
    print(position_info)
