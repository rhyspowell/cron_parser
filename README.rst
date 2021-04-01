############
Cron Parser
############

A simple script that takes a cron line and returns when its expected to run and the command that will be called.

It does not accept the extended commands such as @daily

Running
=======

The script is python 3 only but only uses libraries from the stdlib.

Make the file executable and just call it eg.::

    cron_parser.py "* * * * * /usr/bin/find"


The cron command has to be wrapped in " as different shells behave in different ways and the glob (*) will stop the script from running

Testing
=======

If you wish to test the script, simply install pytest and run that from the test directory

ToDo
====

Clearer highlights for errors

Allow the extended time settings

push to the cheese shop
