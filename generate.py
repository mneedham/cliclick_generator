import click
import os
import pyparsing as pp
import commonmark
import frontmatter
import difflib

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

        for command in reversed(self.commands[self.current_tab]):
            if command.startswith(command_to_find_str.split(" ")[0]):
                return command

command = (
    (pp.Literal("selectWindow") + pp.Literal(":") + pp.Word(pp.nums)) | 
    (pp.Literal("scrollDown") + pp.Literal(":") + pp.Word(pp.nums)) | 
    (pp.Literal("selectTab") + pp.Literal(":") + pp.Word(pp.nums)) |
    (pp.Literal("delete") + pp.Suppress(":") + pp.Word(pp.nums)) |
    (pp.Literal("wait") + pp.Literal(":") + pp.Word(pp.nums)) |
    (pp.Literal("changeApp") + pp.Literal(":") + pp.Word(pp.alphas)) |
    (pp.Literal("click") + pp.Suppress(":") + pp.Word(pp.alphas)) |
    (pp.Literal("movePage") + pp.Suppress(":") + pp.Word(pp.alphas) + pp.Suppress(",") + pp.Word(pp.nums)) |
    pp.Literal("clearScreen") | pp.Literal("quitLess") | pp.Literal("selectAll") |
    (pp.Literal("#") + (pp.Word(pp.alphas)| pp.Literal(" "))) |
    (pp.Literal("```") + pp.QuotedString(pp.alphas+" ", multiline=True) + pp.Literal("```"))
)

def parse_line(line):
    return command.parse_string(line)

page_keys = {
    "down": "page-down",
    "up": "page-up"
}

def to_cliclick(parsed_row, seen_commands):
    if parsed_row[0] == "selectWindow":
        print("kd:alt")
        print(f"t:{parsed_row[2]}")
        print("ku:alt")

    if parsed_row[0] == "wait":
        print(f"w:{parsed_row[2]}")

    if parsed_row[0] == "scrollDown":
        print(f"kd:ctrl")
        for _ in range(0, int(parsed_row[2])):
            print("t:d")
            print('w:500')
        print(f"ku:ctrl") 
        print(f"ku:fn")            
            

    if parsed_row[0] == "selectTab":
        print("kd:cmd")
        print(f"t:{parsed_row[2]}")
        print("ku:cmd")
        seen_commands.set_current_tab(parsed_row[2])

    if parsed_row[0] == "quitLess":        
        print("t:q")

    if parsed_row[0] == "changeApp":        
        print("kd:cmd")
        print("kp:space")
        print("ku:cmd")
        print(f"t:{parsed_row[2]}")
        print("kp:enter")
        
    if parsed_row[0] == "click":
        if parsed_row[1] == "background":
            print("m:1980,320")
            print("c:1980,320")
        if parsed_row[1] == "runQuery":
            print("m:3597,757")
            print("c:3597,757")
        if parsed_row[1] == "queryEditor":
            print("m:1650,550")
            print("c:1650,550")

    if parsed_row[0] == "movePage":
        for i in range(0, int(parsed_row[2])):
            print(f"kp:{page_keys[parsed_row[1]]}")

    if parsed_row[0] == "delete":
        for i in range(0, int(parsed_row[1])):
            print("kp:delete")

    if parsed_row[0] == "clearScreen":
        print("kd:ctrl")
        print("t:lu")        
        print("ku:ctrl")
        print("ku:fn")
        print("w:500")

    if parsed_row[0] == "selectAll":
        print("kd:cmd")
        print("t:a")        
        print("ku:cmd")
        print("ku:fn")

    if parsed_row[0] == "#":
        print(f"# {parsed_row[1]}")

def parse_node(node, seen_commands):
    if node.t  == "code_block":
        lines = [line for line in node.literal.split("\n") if line != ""]

        previous_command = seen_commands.find_previous_similar_command(lines)        
        if previous_command and len(lines) == 1:
            our_command = "\n".join(lines)
            matching_index = difflib.SequenceMatcher(None, our_command, previous_command).find_longest_match().size
            bit_to_delete = previous_command[matching_index:]

            print("kd:ctrl")
            print("t:r")
            print("ku:ctrl")
            print("ku:fn")
            print(f"t:{our_command.split(' ')[0]}")
            print("kd:ctrl")
            print("t:e")
            print("ku:ctrl")
            print("ku:fn")

            for i in range(0, len(bit_to_delete) ):
                print("kp:delete")
            print(f"t:{our_command[matching_index:]}")
            print("kp:enter")

        else:
            for idx,line in enumerate(lines):
                if node.info == "web":
                    print("kd:cmd")
                    print("kd:shift")
                    print("kp:arrow-left")
                    print("ku:shift")
                    print("ku:cmd")
                    print("ku:fn")
                    leading_spaces = len(line) - len(line.lstrip())
                    for i in range(0, leading_spaces):
                        print("kp:space")
                    print(f"t:{line.lstrip()}")
                    if idx != len(lines)-1:                        
                        print("kp:enter")
                else:
                    print(f"t:{line.lstrip()}")
                    print("kp:enter")
        
        seen_commands.add(lines)

    elif node.t == "text":
        if node.literal:
            to_cliclick(parse_line(node.literal), seen_commands)
    elif node.t == "code":
        for item in node.literal.split(" "):
            arr = item.split("_")
            if len(arr) > 1:
                repeat = arr[-1]
                for i in range(0, int(repeat)):
                    print(f"{arr[0]}")
            else:
                print(f"{item}")

@click.command()
@click.option('--file-name', required=True, default=None, help='File path')
def generate(file_name):
    parser = commonmark.Parser()
    seen_commands = SeenCommands()

    if not os.path.isfile(file_name):
        ctx = click.get_current_context()        
        click.echo(click.style(f"Invalid --file-namae provided: {file_name}\n", fg="red"),  err=True)
        click.echo(ctx.get_help())        
        ctx.exit()        
    else:
        with click.open_file(file_name) as file:
            post = frontmatter.load(file)
            ast = parser.parse(post.content)
            all_nodes = [node[0] for node in ast.walker()]
            for node in all_nodes:
                parse_node(node, seen_commands)

if __name__ == "__main__":
    generate()