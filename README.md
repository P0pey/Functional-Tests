# Functional TestSuite

## Testsuite

Testsuite for functional tests. And try to write a portable script in python (python 3)

### Man Page
```
usage: check.py [-h] [-R REFBIN [REFBIN ...]] [-S STDBIN] [-f TESTFILE [TESTFILE ...]] [-c CATEGORY [CATEGORY ...]] [-H]

Functional TestSuite

optional arguments:
  -h, --help            show this help message and exit
  -R REFBIN [REFBIN ...], --refbin REFBIN [REFBIN ...]
                        Ref binary, One binary to rule them all, one binary to find them, One binary to bring them all and in the darkness bind them
  -S STDBIN, --stdbin STDBIN
                        Student binary, try to be the one binary
  -f TESTFILE [TESTFILE ...], --testfile TESTFILE [TESTFILE ...]
                        path to the test file
  -c CATEGORY [CATEGORY ...], --category CATEGORY [CATEGORY ...]
                        Category to test
  -H, --hide            hide stdout diff
```

### Options
```
-R: not mandatory!!! Can take more than 1 param and don't put dash for options, there will be back later
-S: not mandatory!!!
-f: Take 'tests/tests.json' by default but can take more than 1 file to tests
-c: If not precise test all categories. Else test just what you passed in args
-H: False by default. Mean that we will print diff of stdout if there is
```

### Usage
```
./tests/checks.py -R bash posix -S ./bin
```

Specify one or more files (Always JSON files)
```
./tests/checks.py -R bash posix -S ./bin -f tests/tests.json
./tests/checks.py -R bash posix -S ./bin -f tests/tests_lexer.json tests/tests_parser.json
```

Specify one or more category (Exact same name and no whitespace)
```
./tests/checks.py -R bash posix -S ./bin -c Basic Print Builtin
```

### Test File Format

The file format is JSON and the structure is the following example:
```json=
{
    "types": [
        {
            "name": <category>,
            "tests": [
                {
                    "name": <name of the test>,
                    "desc": <description of the test>,
                    "stdin": <stdin to test>,
                    "checks": <List of output to tests (Optional param)>
                },
                {
                    ...
                }
            ]
        },
        {
            ...
        }
    ]
}
```

List of checks param
```json=
{
    "checks": ["stdout", "retval", "stderr", "has_stderr"]
}
```
