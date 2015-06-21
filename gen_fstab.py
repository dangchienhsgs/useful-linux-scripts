import subprocess
from collections import *


def analyze_line(input_line):
    raw_arguments = input_line.split()
    name = raw_arguments[0].replace(":", "").strip()
    label = raw_arguments[1].replace("LABEL=", "").replace("\"", "")
    uuid = raw_arguments[2].replace("UUID=", "").replace("\"", "")
    disk_type = raw_arguments[3].replace("TYPE=", "").replace("\"", "")

    a = defaultdict()
    a["name"] = name
    a["label"] = label
    a["uuid"] = uuid
    a["disk_type"] = disk_type

    return a

out_screen = subprocess.Popen(
    'blkid',
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

f = open("/etc/fstab", "a")
for line in out_screen.stdout.readlines():
    line = line.replace("Giai Tri", "")
    line = line.replace("Setup", "")

    attrs = analyze_line(line)
    if attrs["name"] == "/dev/sda4":
        f.write("UUID={uuid}  /mnt/Data  {type}  defaults  0   0 \n".format(
            uuid=attrs["uuid"], type=attrs["disk_type"]))
    elif attrs["name"] == "/dev/sda5":
        f.write("UUID={uuid}  /mnt/Setup  {type}  defaults  0   0 \n".format(
            uuid=attrs["uuid"], type=attrs["disk_type"]))

f.close()

