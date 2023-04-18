from seen_commands import SeenCommands

def test_find_previous_similar_command_no_previous_command():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    command_to_find = ["foo"]
    assert seen_commands.find_previous_similar_command(command_to_find) == (None, 0)

def test_find_previous_similar_command_existing_command():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(['foo'])
    command_to_find = ['foo']
    assert seen_commands.find_previous_similar_command(command_to_find) == ('foo', 0)

def test_find_previous_similar_command_another_tab():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(["foo"])

    seen_commands.set_current_tab("2")

    command_to_find = ["foo"]
    previous_command, index = seen_commands.find_previous_similar_command(command_to_find)
    assert previous_command == None
    assert index == 0

def test_start_matches():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(["fooBarety"])

    command_to_find = ["fooBar"]

    assert seen_commands.find_previous_similar_command(command_to_find) == ('fooBarety', 0)

def test_multiple_matches():
    seen_commands = SeenCommands()
    seen_commands.set_current_tab("1")
    seen_commands.add(["foo"])
    seen_commands.add(["barfoo"])
    seen_commands.add(["tennisbarfoo"])

    command_to_find = ["foo"]
    assert seen_commands.find_previous_similar_command(command_to_find) == ('foo', 2)
