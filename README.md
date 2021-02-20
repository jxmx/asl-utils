# allstar-arn
Tool for playing Amateur Radio News on Allstarlink Nodes

# Pre-requisites
This script uses standard Python libraries. Allstar.org ASL
should have them all installed by default. For HamVOIP Allstar
the HTTP requests module must be installed with `pacman -S extra/python-requests`.

# Installation

1. cp allstar-play-arn /usr/local/bin
2. cp arn-5m.ul /etc/asterisk/local
3. Add the commands in rpt.conf from this repository into
/etc/asterisk/rpt.conf in the right stanza and restart Allstar
4. Add the crontab entries from crontab.example into root's
contrab - i.e. crontab -e

# Use

Basic use is either immediately from the command line:

	allstar-play-arn --node 1999

or called from a crontab:

	0 8 * * * allstar-play-arn --node 1999

Depending on the processing speed of the device and Internet connectivity, 
the start of playback may take a significant time. If the desire is for 
precision on the start time, use the `--when` command and execute
the `allstar-plan-arn` a few minutes before the desired start time.

The script is silent except on errors. Some useful troubleshooting may
be done with the `--debug` option.

There are not many options to this tool. From /usr/local/bin/allstar-play-arn --help

	usage: allstar-play-arn [-h] --node NODE [--when WHEN] [--debug]
	
	Download and play Amateur Radio Newsline
	
	optional arguments:
	  -h, --help   show this help message and exit
	  --node NODE  Allstar Node # to play audio
	  --when WHEN  When to play in 24 hour format NNNN - not specifying --when
	               will result in the audo playing immediately
	  --debug      enable debug-level logging in syslog

