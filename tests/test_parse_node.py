from generate import parse_node, to_cliclick, parse_line
from seen_commands import SeenCommands

class MockNode:
    def __init__(self, t, literal, info):
        self.t = t
        self.literal = literal
        self.info = info

# Test case for the 'singleLine' scenario
def test_parse_node_single_line():
    node = MockNode("code_block", "example line\n", "singleLine")
    seen_commands = SeenCommands()
    expected_result = ['t:example line', 'kp:enter']
    assert parse_node(node, seen_commands) == expected_result

def test_parse_node_web():
    query = """
select *
from foo
"""

    node = MockNode(
        t="code_block", 
        literal=query.strip('\n'), 
        info="web")
    seen_commands = SeenCommands()
    expected_result = [
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn', 't:select *',
        'kp:enter',
        't:from foo'
    ]
    assert parse_node(node, seen_commands) == expected_result

def test_parse_node_jupyter_simple():
    query = """%%sql
select *
from foo
"""

    node = MockNode(
        t="code_block", 
        literal=query.strip('\n'), 
        info="jupyter")
    seen_commands = SeenCommands()
    expected_result = [
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn',
        't:%%sql', 'kp:enter',
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn',
        't:select *', 'kp:enter',
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn',
        't:from foo'
    ]
    assert parse_node(node, seen_commands) == expected_result


def test_parse_node_jupyter_multi_line():
    query = """%%sql
SELECT station_name,
       date_trunc('DAY', ts) AS day
FROM bikeStations
"""

    node = MockNode(
        t="code_block", 
        literal=query.strip('\n'), 
        info="jupyter")
    seen_commands = SeenCommands()
    expected_result = [
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn',
        't:%%sql', 'kp:enter',
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn',
        't:SELECT station_name,', 'kp:enter',
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn',
        'kp:space','kp:space','kp:space','kp:space','kp:space','kp:space','kp:space',"t:date_trunc('DAY', ts) AS day", 'kp:enter',
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn',
        't:FROM bikeStations'
    ]
    assert parse_node(node, seen_commands) == expected_result


def test_parse_node_web_indentation():
    query = """
select a, b
       c, d
from foo
"""

    node = MockNode(
        t="code_block", 
        literal=query.strip('\n'), 
        info="web")
    seen_commands = SeenCommands()
    expected_result = [
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn', 't:select a, b', 
        'kp:enter',
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn', 'kp:space', 'kp:space', 'kp:space', 'kp:space', 'kp:space', 'kp:space', 'kp:space', 't:c, d',
        'kp:enter',
        'kd:cmd', 'kd:shift', 'kp:arrow-left', 'ku:shift', 'ku:cmd', 'ku:fn', 't:from foo'
    ]
    assert parse_node(node, seen_commands) == expected_result


def test_reuse_existing_command():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(["foo"])
    seen_commands.add(["barfoo"])
    seen_commands.add(["tennisbarfoo"])

    node = MockNode(t="code_block", literal="foo", info="")
    seen_commands = seen_commands
    expected_result = [
     'kd:ctrl', 't:r', 'ku:ctrl', 'ku:fn', 
     't:foo', 
     'kd:ctrl', 't:r', 'ku:ctrl', 'ku:fn', 'kd:ctrl', 
     't:r', 
     'ku:ctrl', 'ku:fn', 
     'kd:ctrl', 't:e', 'ku:ctrl', 'ku:fn', 
     'kp:enter'   
    ]
    assert parse_node(node, seen_commands) == expected_result

def test_reuse_partial_existing_command():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(["foobar"])

    node = MockNode(t="code_block", literal="foo", info="")
    seen_commands = seen_commands
    expected_result = [
     'kd:ctrl', 't:r', 'ku:ctrl', 'ku:fn', 
     't:foo', 
     'kd:ctrl', 't:e', 'ku:ctrl', 'ku:fn', 
     'kp:delete','kp:delete','kp:delete',
     'kp:enter'   
    ]
    assert parse_node(node, seen_commands) == expected_result

def test_schema_table_config_delete_by_char():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(["pygmentize -O style=github-dark config/schema.json"])

    node = MockNode(t="code_block", literal="pygmentize -O style=github-dark config/table.json | less", info="")
    seen_commands = seen_commands
    expected_result = [
     'kd:ctrl', 't:r', 'ku:ctrl', 'ku:fn', 
     't:pygmentize', 
     'kd:ctrl', 't:e', 'ku:ctrl', 'ku:fn', 
     'kp:delete','kp:delete','kp:delete','kp:delete','kp:delete','kp:delete','kp:delete','kp:delete','kp:delete','kp:delete','kp:delete',
     't:table.json | less',
     'kp:enter'
    ]
    assert parse_node(node, seen_commands, char_delete=True) == expected_result

def test_schema_table_config():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(["pygmentize -O style=github-dark config/schema.json"])

    node = MockNode(t="code_block", literal="pygmentize -O style=github-dark config/table.json | less", info="")
    seen_commands = seen_commands
    expected_result = [
     'kd:ctrl', 't:r', 'ku:ctrl', 'ku:fn', 
     't:pygmentize', 
     'kd:ctrl', 't:e', 'ku:ctrl', 'ku:fn', 
     'kd:ctrl', 't:w', 't:w', 'ku:ctrl', 'ku:fn',
     't:table.json | less',
     'kp:enter'
    ]
    assert parse_node(node, seen_commands, char_delete=False) == expected_result

def test_schema_table_config_properties():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(["pygmentize -O style=github-dark config/schema.json"])
    seen_commands.add(["pygmentize -O style=github-dark config/table.json | less"])

    node = MockNode(t="code_block", literal="pygmentize -l properties -O style=github-dark config/controller-conf.conf", info="")
    seen_commands = seen_commands
    expected_result = [
     'kd:ctrl', 't:r', 'ku:ctrl', 'ku:fn', 
     't:pygmentize', 
     'kd:ctrl', 't:e', 'ku:ctrl', 'ku:fn', 
     'kd:ctrl', 't:w', 't:w', 't:w', 't:w', 't:w', 't:w', 't:w', 't:w', 'ku:ctrl', 'ku:fn',
     't:l properties -O style=github-dark config/controller-conf.conf',
     'kp:enter'
    ]
    assert parse_node(node, seen_commands, char_delete=False) == expected_result