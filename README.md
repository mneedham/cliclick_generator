# cliclick Generator

This is a DSL that generates a list of commands for [cliclick](https://github.com/BlueM/cliclick).

## Usage

Create a file that contains some DSL commands, like `examples/example1.txt`:

examples/example1.txt

```
#select window
selectWindow:2

#select tab
selectTab:2

#datagen
clearScreen
```

Call the generate command

```
python generate.py --file-name examples/example1.txt
```

Output

```
# select
kd:alt
t:2
ku:alt
# select
kd:cmd
t:2
ku:cmd
# datagen
kd:ctrl
t:lu
ku:ctrl
ku:fn
w:500
```


Look into this markdown parser:
https://github.com/executablebooks/markdown-it-py