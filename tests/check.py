#!/usr/bin/python3

from pathlib import Path
from difflib import unified_diff
from termcolor import colored

import subprocess as sp
import argparse as ap
import json
import os

# Bring back dash in options
def repair_opts(refbin):
    for i in range(1, len(refbin)):
        opt = '-'
        if (len(refbin[i]) > 1):
            opt = '--'
        refbin[i] = opt + refbin[i]

    return refbin

# Run command
def run_shell(args, stdin):
    return sp.run(args, capture_output=True, text=True, input=stdin)

# Diff between ref and student execution
def diff(ref, student):
    ref = ref.splitlines(keepends=True)
    student = student.splitlines(keepends=True)

    return ''.join(unified_diff(ref, student, fromfile="ref", tofile="student"))

# Copy Results in Directories
def write_test_result(student, testcase, types):
    base_dir = os.getcwd().split('/')[-1]
    path_dir = 'tests/Output_Tests'
    if (base_dir == 'tests'):
        path_dir = 'Output_Tests'

    path_cat = path_dir + '/' + (types['name'].replace(' ', '_'))

    # Create dirs
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    if not os.path.exists(path_cat):
        os.mkdir(path_cat)

    result = {
        "desc": testcase.get('desc'),
        "stdin": testcase['stdin'],
        "stdout": student.stdout,
        "stderr": student.stderr,
        "retval": str(student.returncode)
    }
    with open(path_cat + '/' + testcase['name'].replace(' ',  '_') + '.json', "w") as json_res:
        json_res.write(json.dumps(result, indent=4) + '\n\n')

# The main test function
def test(refbin, stdbin, testcase, hide, types):
    stdin = testcase["stdin"].split(' ')

    if stdin == ['']:
        stdin = []

    # Run commands
    ref = run_shell(refbin + stdin, testcase["stdin"])
    student = run_shell(stdbin + stdin, testcase["stdin"])

    # Save results
    write_test_result(ref, student, testcase, types)

    # Print diff if there is
    for check in testcase.get("checks", ["stdout", "retval"]):
        if check == "stdout":
            if not hide:
                assert ref.stdout == student.stdout, \
                        f"{colored('>>>mismatch stdout<<<', 'red')}\n" +\
                        f"{colored('<<<<<<<<<<<<<<<<<<<<<', 'red')}\n" +\
                        f"{colored(diff(ref.stdout, student.stdout), 'red')}\n"
            else:
                assert ref.stdout == student.stdout, \
                        f"{colored('>>>mismatch stdout<<<', 'red')}\n" +\
                        f"{colored('<<<<<<<<<<<<<<<<<<<<<', 'red')}\n"

        elif check == "stderr":
            assert ref.stderr == student.stderr, \
                    f"{colored('>>>mismatch stderr<<<', 'red')}\n" +\
                    f"{colored('<<<<<<<<<<<<<<<<<<<<<', 'red')}\n" +\
                    f"{colored(diff(ref.stderr, student.stderr), 'red')}\n"
        elif check == "retval":
            assert ref.returncode == student.returncode, \
                    f"{colored('>>>mismatch return value<<<', 'red')}\n" +\
                    f"{colored('<<<<<<<<<<<<<<<<<<<<<', 'red')}\n" +\
                    f"{colored(str(ref.returncode) + ' != ' + str(student.returncode), 'red')}\n"
        elif check == "has_stderr":
            assert student.stderr != "", \
                    f"{colored('>>>missing stderr<<<', 'red')}\n" +\
                    f"{colored('>>>>>>>>>>>>>>>>>>>>', 'red')}\n" +\
                    f"{colored('Something was expected on stderr', 'red')}\n"


# Main function
if __name__ == "__main__":

    # Argument parsing
    parser = ap.ArgumentParser(description="42sh Testsuite")
    parser.add_argument('-R', '--refbin', help='Ref binary, One binary to rule them all, one binary to find them, One binary to bring them all and in the darkness bind them', nargs='+')
    parser.add_argument('-S', '--stdbin', help='Student binary, try to be the one binary', nargs=1)
    parser.add_argument('-f', '--testfile', help='path to the test file', nargs='+')
    parser.add_argument('-c', '--category', help='Category to test', nargs='+')
    parser.add_argument('-H', '--hide' , help='hide stdout diff', action='store_false')
    args = parser.parse_args()

    if (not args.refbin or not args.stdbin):
        print(f"{colored('Need bianry, -R and -S options are not mandatory', 'yellow')}")

    else:
        # Load Ref & student binary to tests
        refbin = args.refbin
        stdbin = Path(args.stdbin[0]).absolute()

        # Repair option of ref binary (add - or --)
        refbin = repair_opts(refbin)

        # Load testing files
        testfile_list = args.testfile
        if (args.testfile == None):
            testfile_list = ['tests/tests.json']

        # Loop for all tests files
        for testfile in testfile_list:

            # Try to open and load each JSON files
            try:
                tests_file = open(testfile, "r")
            except:
                print(f"{colored('File ' + testfile + ' does not exist!', 'red')}")
                print()
                continue
            testsuite = json.load(tests_file)

            # If a category is precise in argument
            if args.category != None:
                for types in testsuite["types"]:
                    if types['name'] in args.category:
                        print(f"\t >>> {colored(types['name'], 'blue')} <<<")

                        for testcase in types["tests"]:
                            # Execute each test
                            try:
                                test(refbin, stdbin, testcase, args.hide, types)
                            except AssertionError as err:
                                print(f"{colored('[KO]', 'red')}\t{testcase['name']}")
                                if (testcase.get('desc')):
                                    print('\n\t### ' + testcase['desc'] + '\n')
                                print(err)
                            else:
                                print(f"{colored('[OK]', 'green')}\t{testcase['name']}")
                        print()

            # If no category is precise
            for types in testsuite["types"]:
                print(f"\t >>> {colored(types['name'], 'blue')} <<<")

                for testcase in types["tests"]:
                    # Execute each tests
                    try:
                        test(refbin, stdbin, testcase, args.hide, types)
                    except AssertionError as err:
                        print(f"{colored('[KO]', 'red')}\t{testcase['name']}")
                        if (testcase.get('desc')):
                            print('\n\t### ' + testcase['desc'] + '\n')
                        print(err)
                    else:
                        print(f"{colored('[OK]', 'green')}\t{testcase['name']}")
                print()
