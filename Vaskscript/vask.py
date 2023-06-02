import sys
import os


class VaskInterpreter:
    def __init__(self):
        self.variables = {}

    def run(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line and not line.startswith("//"):
                self.execute(line)

    def execute(self, line):
        parts = line.split(" ")
        command = parts[0]

        if command == "PRINT":
            if len(parts) > 1:
                value = " ".join(parts[1:])
                self.print(value)
            else:
                self.line_break()
        elif command == "READ":
            self.read()
        elif command == "CLEAR":
            self.clear()
        elif command == "RUN":
            if len(parts) > 1:
                script = " ".join(parts[1:])
                self.run_script(script)
            else:
                print("Invalid command: RUN requires a script or program argument")
        elif command == "VAR":
            if len(parts) >= 3:
                var_name = parts[1]
                var_value = " ".join(parts[2:])
                self.set_variable(var_name, var_value)
            else:
                print("Invalid command: VAR requires a variable name and value")
        elif command == "INPUT":
            if len(parts) > 1:
                var_name = parts[1]
                self.input(var_name)
            else:
                print("Invalid command: INPUT requires a variable name")
        else:
            print(f"Invalid command: {command}")

    def print(self, value):
        evaluated_value = self.evaluate_variables(value)
        print(evaluated_value.strip())

    def line_break(self):
        print()

    def read(self):
        input("Press Enter to continue...")

    def clear(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def run_script(self, script):
        if os.name == 'nt':
            os.system('start ' + script)
        else:
            os.system('xdg-open ' + script)

    def set_variable(self, var_name, var_value):
        self.variables[var_name] = var_value

    def evaluate_variables(self, value):
        for var_name in self.variables:
            var_placeholder = "$" + var_name
            if var_placeholder in value:
                var_value = self.variables[var_name]
                value = value.replace(var_placeholder, var_value)
        return value

    def input(self, var_name):
        user_input = input("> ")
        self.set_variable(var_name, user_input)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python vask.py <script_file>")
    elif sys.argv[1] == "--help":
        help_file = "cmds/help.vs"
        if os.path.exists(help_file):
            interpreter = VaskInterpreter()
            interpreter.run(help_file)
        else:
            print("Error: Help file not found.")
    else:
        script_file = sys.argv[1]
        interpreter = VaskInterpreter()
        interpreter.run(script_file)
