#!/usr/bin/python

import random
import sys
import subprocess
import pickle
import shlex
import os


def grab_videos(directory):
    cmd = "find %s -type f -exec file -N -i -- {} + " % directory
    find_videos = subprocess.Popen(shlex.split(cmd),
                              stdout=subprocess.PIPE)
    grep = subprocess.Popen(shlex.split("grep video"),
                            stdin=find_videos.stdout,
                            stdout=subprocess.PIPE)
    output = grep.stdout
    videos = []
    print "Building database..."
    for line in output:
        v = line.split(":")[0]
        # print v
        videos.append(v)
    # not_seen[directory] = vid eos
    return videos


not_seen_file = "random_episode.pickle"
directory = os.path.abspath(sys.argv[1])

try:
    not_seen = pickle.load(open(not_seen_file, "rb"))
except IOError:
    not_seen = {}

if directory in not_seen:
    videos = not_seen[directory]
else:
    videos = grab_videos(directory)
    not_seen[directory] = videos

if videos == []:
    print "You've seen them all, let's start again!"
    videos = grab_videos(directory)
    not_seen[directory] = videos

v = random.choice(videos)
videos.remove(v)
pickle.dump(not_seen, open(not_seen_file, "wb"))

print "{} episodes remaining".format(len(videos))
print "Let's watch {}".format(v)
subprocess.Popen(shlex.split("vlc \"{}\"".format(v)))
