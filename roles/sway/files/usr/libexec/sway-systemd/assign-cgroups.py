#!/usr/bin/python3
"""
Automatically assign a dedicated systemd scope to the GUI applications
launched in the same cgroup as the compositor.
"""
import argparse
import asyncio
import logging
import sys
import os

# Add the local lib directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from sway_systemd.manager import main_async

def main():
    parser = argparse.ArgumentParser(
        description="Assign CGroups to apps in compositors with i3 IPC protocol support"
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        choices=["critical", "error", "warning", "info", "debug"],
        default="info",
        dest="loglevel",
        help="set logging level",
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
