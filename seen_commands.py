class SeenCommands:
    def __init__(self):
        self.commands = {"1": []}
        self.current_tab = "1"

    def set_current_tab(self, current_tab):
        self.current_tab = current_tab
        if not current_tab in self.commands:
            self.commands[current_tab] = []
    
    def add(self, command):
        self.commands[self.current_tab].append("\n".join(command))

    def find_previous_similar_command(self, command_to_find):
        command_to_find_str = "\n".join(command_to_find)

        needle = command_to_find_str.split(" ")[0]
        matching_commands = []        
        for command in reversed(self.commands[self.current_tab]):            
            if needle in command:
                matching_commands.append(command)

        # print(f"** {matching_commands}")
        for idx, command in enumerate(matching_commands):            
            if command.startswith(needle):
                # print("****" + str(idx))
                return command, idx
        
        return None, 0