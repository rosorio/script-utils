#! /usr/bin/env python3
"""
    Copyright (c) 2017 Rodrigo Osorio <rodrigo@freebsd.org>
    All rights reserved.
   
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer
       in this position and unchanged.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
   
    THIS SOFTWARE IS PROVIDED BY THE AUTHOR(S) ``AS IS'' AND ANY EXPRESS OR
    IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
    NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
    THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Script to compare the git commits between two branches
    The script was initiated by chatgpt was unusable so we still improving it.
"""
import subprocess
import sys

def get_patch_ids(branch):
    """Returns a sorted list of patch IDs for a given branch."""
    try:
        log_output = subprocess.check_output(["git", "log", "-p", branch], text=True, stderr=subprocess.DEVNULL)
        patch_ids = subprocess.check_output(["git", "patch-id"], input=log_output, text=True)
        patch_ids = [line.split()[0] for line in patch_ids.strip().split('\n')]
        return sorted(patch_ids)
    except subprocess.CalledProcessError:
        print("Error: Could not retrieve patch IDs for branch {}".format(branch))
        sys.exit(1)

def compare_branches(branch1, branch2):
    """Compares two branches based on their patch IDs."""
    patches1 = get_patch_ids(branch1)
    patches2 = get_patch_ids(branch2)

    if patches1 == patches2:
        print("   Branches {} and {} contain the same changes.".format(branch1, branch2))
    else:
        print("   Branches {} and {} have different changes!".format(branch1, branch2))
        print("Differences:")
        diff1 = set(patches1) - set(patches2)
        diff2 = set(patches2) - set(patches1)
        if diff1:
            print("- Commits unique to {}: {}".format(branch1,diff1))
        if diff2:
            print("- Commits unique to {}: {}".format(branch2,diff2))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_git_branches.py <branch1> <branch2>")
        sys.exit(1)
    compare_branches(sys.argv[1], sys.argv[2])

