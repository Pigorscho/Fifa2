class Secrets:
    def __init__(self, name):
        self.name = name
        setup = self.parse_setup()

        self.fifa_user = setup['fifa_user']
        self.fifa_password = setup['fifa_password']

    def parse_setup(self):
        setup = {}

        with open(rf'secrets\secrets_{self.name}.env', 'r', encoding='utf-8') as f:
            content = f.read()

        for line in content.splitlines():
            if not line or line.startswith('#') or '=' not in line:
                continue
            line = line.strip()
            key, val = line.split('=')
            setup[key] = val

        return setup


if __name__ == '__main__':
    import os
    os.chdir(r'../..')

    secrets = Secrets('Pigo')
    for key, val in secrets.__dict__.items():
        print(f'{key}: {val}')
