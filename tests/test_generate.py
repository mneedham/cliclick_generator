from generate import to_cliclick, parse_line
from seen_commands import SeenCommands

def test_to_cliclick_select_window():
    parsed_row = parse_line("selectWindow:3")
    expected_result = ['kd:cmd', 'kd:alt', 't:3', 'ku:alt', 'ku:cmd']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_type_slowly():
    parsed_row = parse_line("typeSlowly:hello||100")
    expected_result = ['t:h', 'w:100', 't:e', 'w:100', 't:l', 'w:100', 't:l', 'w:100', 't:o', 'w:100']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_type_slowly_extra_chars():
    parsed_row = parse_line("typeSlowly:hello {}||100")
    expected_result = ['t:h', 'w:100', 't:e', 'w:100', 't:l', 'w:100', 't:l', 'w:100', 't:o', 'w:100', 'kp:space', 'w:100', 't:{', 'w:100', 't:}', 'w:100']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_wait():
    parsed_row = parse_line("wait:500")
    expected_result = ['w:500']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_vsCodeGoToLine():
    parsed_row = parse_line("vsCodeGoToLine:15")
    expected_result = ['kd:ctrl', 't:g', 'ku:ctrl', 't:15', 'w:200', 'kp:enter']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_move_and_click_background():
    parsed_row = parse_line("moveAndClick:background")
    expected_result = ['m:1980,320', 'c:1980,320']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_clear_screen():
    parsed_row = parse_line("clearScreen")
    expected_result = ['kd:ctrl', 't:lu', 'ku:ctrl', 'ku:fn', 'w:500']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_select_all():
    parsed_row = parse_line("selectAll")
    expected_result = ['kd:cmd', 't:a', 'ku:cmd', 'ku:fn']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_raycast_switch_app():
    parsed_row = parse_line("raycastSwitchApp:Telegram")
    expected_result = ['kd:cmd', 'kp:space', 'ku:cmd', 't:Switch', 'kp:enter', 'w:500', 't:Telegram', 'w:500', 'kp:enter', 'w:500']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_vs_code_save():
    parsed_row = parse_line("vsCodeSave")
    expected_result = ['kd:cmd', 't:s', 'ku:cmd']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_vs_code_end_of_file():
    parsed_row = parse_line("vsCodeEndOfFile")
    expected_result = ['kd:cmd', 'kp:arrow-down', 'ku:cmd']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_vs_code_search():
    parsed_row = parse_line("vsCodeSearch:search")
    expected_result = ['kd:cmd', 't:p', 'ku:cmd', 't:search', 'w:200', 'kp:enter']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_vs_code_search_extra_chars():
    parsed_row = parse_line("vsCodeSearch:mark_file.py")
    expected_result = ['kd:cmd', 't:p', 'ku:cmd', 't:mark_file.py', 'w:200', 'kp:enter']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result
