# allstar-arn
Tool for playing Amateur Radio News on Allstarlink Nodes

# Installation

1. cp allstar-play-arn /usr/local/bin
2. cp arn-5m.ul /etc/asterisk/local
3. Add the commands in rpt.conf from this repository into
/etc/asterisk/rpt.conf in the right stanza and restart Allstar
4. Add the crontab entries from crontab.example into root's
contrab - i.e. crontab -e

# Use

There are not many options to this tool. See /usr/local/bin/allstar-play-arn --help

	usage: allstar-play-arn [-h] --node NODE [--when WHEN] [--debug]
	
	Download and play Amateur Radio Newsline
	
	optional arguments:
	  -h, --help   show this help message and exit
	  --node NODE  Allstar Node # to play audio
	  --when WHEN  When to play in 24 hour format NNNN - not specifying --when
	               will result in the audo playing immediately
	  --debug      enable debug-level logging in syslog

