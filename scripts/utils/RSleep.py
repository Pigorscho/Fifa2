import random
from time import sleep


class RSleep:
    @staticmethod
    def calculate_time(seconds):
        """Calculate a random time close to the given seconds."""
        tolerance = 0.1

        while True:
            if seconds == 0:
                random_time = 0
            elif seconds <= 1:
                random_time = random.uniform(0.7, 1.3)
            elif seconds <= 2:
                random_time = random.uniform(1.6, 2.4)
            else:
                random_time = random.uniform(seconds - 0.5, seconds + 0.5)

            # Check if the random time is too close to a perfect number
            if abs(random_time - round(random_time)) > tolerance:
                break

        return random_time

    def sleep(self, seconds, test=False):
        """Sleep for a random duration close to the given seconds."""
        random_sleep_time = self.calculate_time(seconds)
        if not test:
            sleep(random_sleep_time)
        return random_sleep_time


if __name__ == '__main__':
    # Testing the class
    rs = RSleep()
    out = ''
    for i in range(1, 11):
        out += f'{i}: '
        for k in range(1, 11):
            test_duration = rs.sleep(i, test=True)
            out += f'{test_duration} '
        out += '\n'
    print(out)
