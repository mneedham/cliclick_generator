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

def test_to_cliclick_move_and_click_run_query():
    parsed_row = parse_line("moveAndClick:runQuery")
    expected_result = ['m:3597,757', 'c:3597,757']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_move_and_click_query_editor():
    parsed_row = parse_line("moveAndClick:queryEditor")
    expected_result = ['m:2441,503', 'c:2441,503']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_click_background():
    parsed_row = parse_line("click:background")
    expected_result = ['c:1980,320']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_click_run_query():
    parsed_row = parse_line("click:runQuery")
    expected_result = ['c:3597,757']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_click_query_editor():
    parsed_row = parse_line("click:queryEditor")
    expected_result = ['c:2421,519']
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

def test_to_cliclick_raycast_switch_app_multi_word():
    parsed_row = parse_line("raycastSwitchApp:Chrome Person 1")
    expected_result = ['kd:cmd', 'kp:space', 'ku:cmd', 't:Switch', 'kp:enter', 'w:500', 't:Chrome Person 1', 'w:500', 'kp:enter', 'w:500']
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

def test_to_cliclick_cliclick2_single_click():
    parsed_row = parse_line("cliclick2:c:100,200||1")
    expected_result = ['c:100,200']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_cliclick2_multiple_clicks():
    parsed_row = parse_line("cliclick2:c:100,200||3")
    expected_result = ['c:100,200', 'c:100,200', 'c:100,200']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_cliclick2_different_positions():
    parsed_row = parse_line("cliclick2:m:50,50||1")
    expected_result = ['m:50,50']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_scroll_down_single():
    parsed_row = parse_line("scrollDown:1")
    expected_result = ['kd:ctrl', 't:d', 'w:500', 'ku:ctrl', 'ku:fn']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_scroll_down_multiple():
    parsed_row = parse_line("scrollDown:3")
    expected_result = ['kd:ctrl', 't:d', 'w:500', 't:d', 'w:500', 't:d', 'w:500', 'ku:ctrl', 'ku:fn']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_comment_single_word():
    parsed_row = parse_line("//comment")
    expected_result = ['# comment']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_comment_multiple_words():
    parsed_row = parse_line("//This is a comment")
    expected_result = ['# This is a comment']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_comment_with_special_characters():
    parsed_row = parse_line("//Comment with special chars: !@#$%^&*()")
    expected_result = ['# Comment with special chars: !@#$%^&*()']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_comment_out_another_command():
    parsed_row = parse_line("//typeSlowly:hello||100")
    expected_result = ['# typeSlowly:hello||100']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_refresh_screen():
    parsed_row = parse_line("refreshScreen")
    expected_result = ['kd:cmd', 't:r', 'ku:cmd', 'ku:fn']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_scroll_to_end():
    parsed_row = parse_line("scrollToEnd")
    expected_result = ['kd:shift', 't:g', 'ku:shift', 'ku:fn']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_delete():
    parsed_row = parse_line("delete:5")
    expected_result = ['kp:delete', 'kp:delete', 'kp:delete', 'kp:delete', 'kp:delete']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_chrome_url_bar():
    parsed_row = parse_line("chromeUrlBar:example.com")
    expected_result = ['kd:cmd', 't:l', 'ku:cmd', 't:example.com', 'kp:enter']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_chrome_url_bar_complex():
    parsed_row = parse_line("chromeUrlBar:http://localhost:8888/login?next=%2Fnotebooks%2Fnotebooks%2FDuckDB%2520SQL%2520Window%2520Functions.ipynb?token=cddefbcc53de984b40c575e2aaf0c47fd03329c1e8f1a4da")
    expected_result = ['kd:cmd', 't:l', 'ku:cmd', 't:http://localhost:8888/login?next=%2Fnotebooks%2Fnotebooks%2FDuckDB%2520SQL%2520Window%2520Functions.ipynb?token=cddefbcc53de984b40c575e2aaf0c47fd03329c1e8f1a4da', 'kp:enter']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_select_tab():
    seen_commands = SeenCommands()
    parsed_row = parse_line("selectTab:2")
    expected_result = ['kd:cmd', 't:2', 'ku:cmd']
    assert to_cliclick(parsed_row, seen_commands) == expected_result
    assert seen_commands.current_tab == '2'

def test_to_cliclick_quit_less():
    parsed_row = parse_line("quitLess")
    expected_result = ['t:q']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_jupyter_cell_below():
    parsed_row = parse_line("jupyter::notebook::command::b")
    expected_result = ['kp:esc', "t:b"]
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_jupyter_enter():
    parsed_row = parse_line("jupyter::notebook::command::enter")
    expected_result = ['kp:esc', "kp:enter"]
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_jupyter_run_query():
    parsed_row = parse_line("jupyter::notebook::edit::cmd+enter")
    expected_result = ["kd:cmd", 'kp:enter', 'ku:cmd', 'ku:fn']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_jupyter_save_notebook():
    parsed_row = parse_line("jupyter::notebook::command::cmd+s")
    expected_result = ['kp:esc', "kd:cmd", 't:s', 'ku:cmd', 'ku:fn']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result


def test_to_cliclick_jupyter_merge_cells():
    parsed_row = parse_line("jupyter::notebook::command::shift+m")
    expected_result = ['kp:esc',"kd:shift", 't:m', 'ku:shift', 'ku:fn']
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result

def test_to_cliclick_jupyter_delete_cell():
    parsed_row = parse_line("jupyter::notebook::command::d,d")
    expected_result = ['kp:esc', "t:d", "t:d"]
    assert to_cliclick(parsed_row, SeenCommands()) == expected_result