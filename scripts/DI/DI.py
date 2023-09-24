from scripts.utils.RSleep import RSleep
from scripts.utils.Pics import Pics
from scripts.utils.PILRegs import PILRegs


class DI:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.dependencies = {}
        self.dependency_map = {
            'rs': RSleep,
            'pics': Pics,
            'pilregs': PILRegs,
        }

    def get(self, dependency_name):
        if dependency_name in self.dependencies:
            if self.verbose:
                print(f'returning object {dependency_name}')
            dependency = self.dependencies[dependency_name]
        else:
            if self.verbose:
                print(f'creating object {dependency_name}')
            dependency = self.dependency_map[dependency_name]()
            self.dependencies[dependency_name] = dependency

        return dependency


di = DI()


if __name__ == '__main__':
    di = DI(verbose=True)
    for i in range(1, 6):
        dur = di.get('rs').sleep(i, test=True)
        print(dur)
