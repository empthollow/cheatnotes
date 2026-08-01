# special bash elements
## shebang
```bash
#!/bin/bash 
```
## argument vars
```bash
$0 = script name
$1, $2, $3, ... = individual arguments
$# = count of arguments
$@ = all arguments as an array
$* = all arguments as a single string
```

# error handling
## error safety modes

-e (errexit)
Exits immediately if any command returns a non-zero exit code. Prevents the script from continuing after errors.

-u (nounset)
Treats undefined variables as errors and exits. Catches typos like $BULD_FILE instead of $BUILD_FILE before they cause silent failures.

-o pipefail
If any command in a pipe fails, the whole pipeline fails (default is only the last command's exit code counts). Example:

enable three bash safety modes:
```bash
set -euo pipefail 
```
## Error handling function
```bash
handle_error() {
  echo "Execution error on line $1. Exiting..."
  exit 1
}
```

### Trap errors and call the error handler
```bash
trap 'handle_error $LINENO' ERR
```

# flow statements
## for loop one line
```bash
for i in {1..5}; do COMMAND-HERE; done
```

## for loop script
```bash
for VARIABLE in 1 2 3 4 5 .. N
do
    command1
    command2
    commandN
done

for VARIABLE in file1 file2 file3
do
    command1 on $VARIABLE
    command2
    commandN
done

for OUTPUT in $(Linux-Or-Unix-Command-Here)
do
    command1 on $OUTPUT
    command2 on $OUTPUT
    commandN
done
```

## regex inside an if clause
```bash
if [[ "$string" =~ regex_pattern ]]; then
  # code block to execute if string matches regex pattern
else
  # code block to execute if string does not match regex pattern
fi
```

