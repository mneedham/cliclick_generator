import click
import os
import pyparsing as pp
import commonmark
import frontmatter
import difflib
from seen_commands import SeenCommands

command = (
    (pp.Literal("cliclick") + pp.Suppress(":") + pp.Word(pp.alphanums+"-") + pp.Literal(":") + pp.Word(pp.alphanums+"-"+" ") + pp.Suppress(",") + pp.Word(pp.nums)) | 
    (pp.Literal("cliclick2") + pp.Suppress(":") +  pp.Word(pp.alphanums+"-") + pp.Literal(":") + ( pp.Word(pp.alphanums+"-,}{+ ") ) + pp.Suppress("||") + pp.Word(pp.nums)) | 
    (pp.Literal("selectWindow") + pp.Literal(":") + pp.Word(pp.nums)) | 
    (pp.Literal("scrollDown") + pp.Literal(":") + pp.Word(pp.nums)) | 
    (pp.Literal("selectTab") + pp.Literal(":") + pp.Word(pp.nums)) |
    (pp.Literal("delete") + pp.Suppress(":") + pp.Word(pp.nums)) |
    (pp.Literal("wait") + pp.Literal(":") + pp.Word(pp.nums)) |    
    (pp.Literal("changeApp") + pp.Literal(":") + pp.Word(pp.alphas)) |
    (pp.Literal("raycastSwitchApp") + pp.Suppress(":") + pp.Word(pp.alphanums+"-,}{+ ")) |
    (pp.Literal("chromeUrlBar") + pp.Suppress(":") + pp.Word(pp.alphanums + ":")) |
    (pp.Literal("typeSlowly") + pp.Suppress(":") + pp.Word(pp.alphanums + ":" + " ") + pp.Suppress("||") + pp.Word(pp.nums)) |
    (pp.Literal("vsCodeGoToLine") + pp.Suppress(":") + pp.Word(pp.nums)) |
    (pp.Literal("vsCodeSearch") + pp.Suppress(":") + pp.Word(pp.alphanums + ".")) |
    (pp.Literal("click") + pp.Suppress(":") + pp.Word(pp.alphas)) |
    (pp.Literal("moveAndClick") + pp.Suppress(":") + pp.Word(pp.alphas)) |
    (pp.Literal("movePage") + pp.Suppress(":") + pp.Word(pp.alphas) + pp.Suppress(",") + pp.Word(pp.nums)) |    
    (pp.Literal("//") + pp.Word(pp.alphanums + " -{}/.")) |
    (pp.Literal("```") + pp.QuotedString(pp.alphas+" ", multiline=True) + pp.Literal("```")) |
    pp.Literal("vsCodeSave") | pp.Literal("vsCodeEndOfFile") | pp.Literal("clearScreen") | pp.Literal("scrollToEnd") | pp.Literal("quitLess") | pp.Literal("selectAll") | pp.Literal("refreshScreen")
)

def parse_line(line):
    return command.parse_string(line)

page_keys = {
    "down": "page-down",
    "up": "page-up"
}

def to_cliclick(parsed_row, seen_commands):
    cliclick_commands = []
    if parsed_row[0] == "cliclick" or parsed_row[0] == "cliclick2":
        for i in range(0, int(parsed_row[4])):
            cliclick_commands.append("".join(parsed_row[1:4]))


    if parsed_row[0] == "selectWindow":
        cliclick_commands.append("kd:cmd")
        cliclick_commands.append("kd:alt")
        cliclick_commands.append(f"t:{parsed_row[2]}")
        cliclick_commands.append("ku:alt")
        cliclick_commands.append("ku:cmd")

    if parsed_row[0] == "typeSlowly":
        word = parsed_row[1]
        pause_time = int(parsed_row[2])
        for char in word:
            if char == " ":
                cliclick_commands.append(f"kp:space")
            else:
                cliclick_commands.append(f"t:{char}")
            cliclick_commands.append(f"w:{pause_time}")

    if parsed_row[0] == "wait":
        cliclick_commands.append(f"w:{parsed_row[2]}")

    if parsed_row[0] == "vsCodeGoToLine":
        cliclick_commands.append(f"kd:ctrl")
        cliclick_commands.append(f"t:g")
        cliclick_commands.append(f"ku:ctrl")
        cliclick_commands.append(f"t:{parsed_row[1]}")
        cliclick_commands.append(f"w:200")
        cliclick_commands.append(f"kp:enter")

    if parsed_row[0] == "vsCodeSave":
        cliclick_commands.append(f"kd:cmd")
        cliclick_commands.append(f"t:s")
        cliclick_commands.append(f"ku:cmd")

    if parsed_row[0] == "vsCodeEndOfFile":
        cliclick_commands.append(f"kd:cmd")
        cliclick_commands.append(f"kp:arrow-down")
        cliclick_commands.append(f"ku:cmd")


    if parsed_row[0] == "vsCodeSearch":
        cliclick_commands.append(f"kd:cmd")
        cliclick_commands.append(f"t:p")
        cliclick_commands.append(f"ku:cmd")
        cliclick_commands.append(f"t:{parsed_row[1]}")
        cliclick_commands.append(f"w:200")
        cliclick_commands.append(f"kp:enter")

    if parsed_row[0] == "scrollDown":
        cliclick_commands.append(f"kd:ctrl")
        for _ in range(0, int(parsed_row[2])):
            cliclick_commands.append("t:d")
            cliclick_commands.append('w:500')
        cliclick_commands.append(f"ku:ctrl") 
        cliclick_commands.append(f"ku:fn")            
            

    if parsed_row[0] == "selectTab":
        cliclick_commands.append("kd:cmd")
        cliclick_commands.append(f"t:{parsed_row[2]}")
        cliclick_commands.append("ku:cmd")
        seen_commands.set_current_tab(parsed_row[2])

    if parsed_row[0] == "quitLess":        
        cliclick_commands.append("t:q")

    if parsed_row[0] == "changeApp":        
        cliclick_commands.append("kd:cmd")
        cliclick_commands.append("kp:space")
        cliclick_commands.append("ku:cmd")
        cliclick_commands.append(f"t:{parsed_row[2]}")
        cliclick_commands.append("kp:enter")

    if parsed_row[0] == "raycastSwitchApp":
        cliclick_commands.append("kd:cmd")
        cliclick_commands.append("kp:space")
        cliclick_commands.append("ku:cmd")
        cliclick_commands.append("t:Switch")
        cliclick_commands.append("kp:enter")
        cliclick_commands.append("w:500")
        cliclick_commands.append(f"t:{parsed_row[1]}")        
        cliclick_commands.append("w:500")
        cliclick_commands.append("kp:enter")
        cliclick_commands.append("w:500")

    if parsed_row[0] == "chromeUrlBar":        
        cliclick_commands.append("kd:cmd")
        cliclick_commands.append("t:l")
        cliclick_commands.append("ku:cmd")
        cliclick_commands.append(f"t:{parsed_row[1]}")
        cliclick_commands.append("kp:enter")
        
    if parsed_row[0] == "moveAndClick":
        if parsed_row[1] == "background":
            cliclick_commands.append("m:1980,320")
            cliclick_commands.append("c:1980,320")
        if parsed_row[1] == "runQuery":
            cliclick_commands.append("m:3597,757")
            cliclick_commands.append("c:3597,757")
        if parsed_row[1] == "queryEditor":
            cliclick_commands.append("m:2441,503")
            cliclick_commands.append("c:2441,503")

    if parsed_row[0] == "click":
        if parsed_row[1] == "background":
            cliclick_commands.append("c:1980,320")
        if parsed_row[1] == "runQuery":
            cliclick_commands.append("c:3597,757")
        if parsed_row[1] == "queryEditor":
            cliclick_commands.append("c:2421,519")

    if parsed_row[0] == "movePage":
        for i in range(0, int(parsed_row[2])):
            cliclick_commands.append(f"kp:{page_keys[parsed_row[1]]}")

    if parsed_row[0] == "delete":
        for i in range(0, int(parsed_row[1])):
            cliclick_commands.append("kp:delete")

    if parsed_row[0] == "clearScreen":
        cliclick_commands.append("kd:ctrl")
        cliclick_commands.append("t:lu")        
        cliclick_commands.append("ku:ctrl")
        cliclick_commands.append("ku:fn")
        cliclick_commands.append("w:500")

    if parsed_row[0] == "selectAll":
        cliclick_commands.append("kd:cmd")
        cliclick_commands.append("t:a")        
        cliclick_commands.append("ku:cmd")
        cliclick_commands.append("ku:fn")

    if parsed_row[0] == "refreshScreen":
        cliclick_commands.append("kd:cmd")
        cliclick_commands.append("t:r")        
        cliclick_commands.append("ku:cmd")
        cliclick_commands.append("ku:fn")

    if parsed_row[0] == "scrollToEnd":
        cliclick_commands.append("kd:shift")
        cliclick_commands.append("t:g")        
        cliclick_commands.append("ku:shift")
        cliclick_commands.append("ku:fn")

    if parsed_row[0] == "//":
        cliclick_commands.append(f"# {parsed_row[1]}")
    return cliclick_commands

def search_command():
    return [
        "kd:ctrl",
        "t:r",
        "ku:ctrl",
        "ku:fn"
    ]

def end_of_line_command():
    return [
        "kd:ctrl",
        "t:e",
        "ku:ctrl",
        "ku:fn"
    ]

def parse_node(node, seen_commands):    
    if node.t  == "code_block":     
        cliclick_commands = []
        lines = [line for line in node.literal.split("\n") if line != ""]

        previous_command, index = seen_commands.find_previous_similar_command(lines)        
        if previous_command and len(lines) == 1 and len(lines[0]) > 30 and (not " =" in lines[0][:20]) and not(node.info == "web") and not(node.info == "singleLine"):
            our_command = "\n".join(lines)
            matching_index = difflib.SequenceMatcher(None, our_command, previous_command).find_longest_match().size
            bit_to_delete = previous_command[matching_index:]

            cliclick_commands += search_command()
            cliclick_commands.append(f"t:{our_command.split(' ')[0]}")
            for _ in range(0, index):
                cliclick_commands += search_command()
            cliclick_commands += end_of_line_command()

            for i in range(0, len(bit_to_delete) ):
                cliclick_commands.append("kp:delete")
            cliclick_commands.append(f"t:{our_command[matching_index:]}")
            cliclick_commands.append("kp:enter")

        else:
            previous_leading_spaces = -1
            for idx,line in enumerate(lines):
                if node.info == "singleLine":
                    cliclick_commands.append(f"t:{line}")
                    cliclick_commands.append("kp:enter")
                elif node.info == "web":
                    leading_spaces = len(line) - len(line.lstrip())
                    if leading_spaces == previous_leading_spaces:
                        cliclick_commands.append(f"t:{line.lstrip()}")
                    else:
                        cliclick_commands.append("kd:cmd")
                        cliclick_commands.append("kd:shift")
                        cliclick_commands.append("kp:arrow-left")
                        cliclick_commands.append("ku:shift")
                        cliclick_commands.append("ku:cmd")
                        cliclick_commands.append("ku:fn")                    
                        for i in range(0, leading_spaces):
                            cliclick_commands.append("kp:space")
                        cliclick_commands.append(f"t:{line.lstrip()}")
                    if idx != len(lines)-1:                        
                        cliclick_commands.append("kp:enter")
                    previous_leading_spaces = leading_spaces
                else:
                    leading_spaces = len(line) - len(line.lstrip())
                    for i in range(0, leading_spaces):
                        cliclick_commands.append("kp:space")
                    cliclick_commands.append(f"t:{line.lstrip()}")
                    cliclick_commands.append("kp:enter")
        
        # print(f"add lines: {lines}")
        seen_commands.add(lines)
        return cliclick_commands

    elif node.t == "text":
        if node.literal:
            return to_cliclick(parse_line(node.literal), seen_commands)
    else:
        return []

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
                for command in parse_node(node, seen_commands):
                    print(command)

if __name__ == "__main__":
    generate()