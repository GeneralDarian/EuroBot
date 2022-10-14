# Running the Bot

## Setup

The first thing you should do to run the bot is to ensure you’re in the root
directory of the project.  For example:

```sh
$ pwd
/home/thomas/.../GeneralDarian/EuroBot
```

Once you are in the root directory you want to run the following command to
create a [python virtual environment][1].  This will allow you to run the bot in
an independent environment so that you don’t suffer complications with
dependency versions.  After doing this you should notice that the folders
`bin/`, `include/`, `lib/`, `lib64/`, and the file `pyvenv.cfg` all get created:

```sh
$ python3 -m venv .
$ ls
bin  include  lib  lib64  pyvenv.cfg
```

Now you want to activate the virtual environment.  This will need to be repeated
every time you open new terminal session:

```sh
$ source bin/activate
```

Finally, we can install the dependencies:

```sh
$ python3 -m pip install -r requirements.txt
```

[1]: https://docs.python.org/3/library/venv.html

## Running

With all the setup done, running the bot is extremely simple:

```sh
$ python3 src/main.py
```
