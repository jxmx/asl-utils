#!/usr/bin/python3

from asyncio.windows_events import NULL
from glob import escape
from typing import List
import argparse
import json
import logging
import logging.handlers
import os
import re
import requests
import sys
import urllib3

#
# recursively traverse each linked node to find the target
#
def walkNode(nodeID, targetID):
    log.debug("walkNode: " + nodeID + "?" + targetID)

    if( nodeID == targetID):
            log.debug("walkNode: returning found in node: " + nodeID)
            return nodeID

    if nodeID in nodes_considered:
        log.debug("walkNode: return false -- already considered " + nodeID)
        return False
    else:
        log.debug("walkNode: append nodes_considered: " + nodeID)
        nodes_considered.append(nodeID)

    try:
        response = requests.get("https://stats.allstarlink.org/api/stats/" + nodeID)
        node_info = json.loads(response.text)
    except Exception as e:
        log.error(str(e))
        sys.exit(1) 

    try:    
        if not "linkedNodes" in node_info["stats"]["data"]:
            log.debug("walkNode: No links out of " + nodeID)
            return False      
    except:
        log.debug("walkNode: Does not have a [stats][data] segment so it's a special case (e.g. Echolink, Broadcastify)")
        return False

    for n in node_info["stats"]["data"]["linkedNodes"]:
        log.debug("walkNode: found linked node " + n["name"])
        if( n["name"] == targetID):
            log.debug("walkNode: returning found in node: " + nodeID)
            return nodeID
        elif(re.search("^[0-9]{4,6}$", n["name"])):
            if walkNode(n["name"], targetID):
                return nodeID
        else:
            return False

def hunt():
    #
    ## Do the query on the initial --me node
    #
    nodes_to_consider = []
    try:
        response = requests.get("https://stats.allstarlink.org/api/stats/" + args.me)
        node_info = json.loads(response.text)
    except Exception as e:
        log.error(str(e))
        sys.exit(1)

    # If this is empty or does not exist, there are no linked nodes
    # Assuming this isn't being tried on a special-type node like Echolink/Broadcastify
    try:
        for ln in node_info["stats"]["data"]["linkedNodes"]:
            nodes_to_consider.append(ln["name"])
    except:
        log.info("No linked nodes to " + args.me)
        sys.exit(0)

    if len(nodes_to_consider) == 0:
        log.info("No linked nodes to " + args.me)
        sys.exit(0)

    ## Iterate over all peer nodes of the --me node to look for the target
    log.debug("main: nodes_to_consider: " + str(nodes_to_consider))
    for n in nodes_to_consider:
        res = walkNode(n, args.target)
        if res != False:
            return(res)
    
    ## If we got here, the node wasn't found
    return False

def snipe(thisNode, targetNode):
    cmd = "asterisk -rx 'rpt fun {} *1{}".format(thisNode, targetNode)
    log.debug("snipe: " + cmd)
    return os.system(cmd)

if __name__ == "__main__":
    
    nodes_considered = []

    ## Args & "Help"
    ap = argparse.ArgumentParser(description = "Find where an Allstar node is linked through and snipe the link out")
    ap.add_argument("--debug", help="Enable debug logging", action="store_true")
    ap.add_argument("--me", help="The node where this script is running", required=True)
    ap.add_argument("--target", help="The node being targeted", required=True)
    args = ap.parse_args()
  
    if not re.search("^[0-9]{4,6}$", args.me): 
        print("--me is required must be a 4 to 6 digit number", file=sys.stderr)
        sys.exit(1)
    nodes_considered.append(args.me)

    if not re.search("^[0-9]{4,6}$", args.target): 
        print("--target is required must be a 4 to 6 digit number", file=sys.stderr)
        sys.exit(1)
    
    ## Logging
    log = logging.getLogger("asl-sniper")
    lh = logging.StreamHandler(sys.stdout)
    lf = logging.Formatter(fmt='%(name)s: %(levelname)s: %(message)s')
    lh.setFormatter(lf)
    log.addHandler(lh)

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.ERROR)
   

    acquired = hunt()
    log.debug("Sniping at " + acquired)
    rv = snipe(args.me, acquired)
    if rv == 0:
        log.info("Snipped " + acquired)
        sys.exit(0)
    else:
        log.error("Snipe failed for " + args.me + " -> " + acquired)
        sys.exit(1)

