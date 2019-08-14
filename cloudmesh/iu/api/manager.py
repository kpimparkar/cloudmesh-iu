import os
from subprocess import check_output
from cloudmesh.common3.Shell import Shell
from cloudmesh.common.Printer import Printer
from textwrap import indent
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.console import Console

import random
class Manager(object):

    """
    PARTITION  AVAIL  TIMELIMIT  NODES   GRES  STATE NODELIST
    romeo         up   infinite      4  gpu:8    mix r-[001-004]
    volta         up   infinite      2  gpu:8    mix r-[005-006]
    """
    def __init__(self):
        print("init {name}".format(name=self.__class__.__name__))

    def list(self, parameter):
        print("list", parameter)

    def login(self,
              user=None,
              host="romeo",
              node=1,
              gpus=1):

        command = f"ssh -t {user}@juliet.futuresystems.org " \
                  f" srun -p {host}" \
                  f" -w {node} --gres gpu:{gpus} --pty bash"

        os.system(command)

    def smart_login(self,
              user=None,
              host="romeo",
              node=1,
              gpus=1):
        status = self.queue(host=host, user=user)
        print (Printer.attribute(status, header=["Node", "Used GPUs"]))


        #
        # Required node not available (down, drained or reserved)
        #

        def find_random(host):
            if host == "volta":
                random.randint(1, 2) + 4
            else:
                number = random.randint(1, 4)
            node = f"r-00{number}"
            return node

        def find_first(host):
            node=None
            max_gpus = 8 # this is for now hard coded
            for node in status:
                used = status[node]
                if used + gpus < max_gpus:
                    break
            return node

        if node is None or node=="first":
            node = find_first(host)

        if node is None or node=="random":
            node = find_random(host)

        if node is not None:
            Console.ok(f"Login on node {host}: {node}")

            self.login(
                 user=user,
                 host=host,
                 node=node,
                 gpus=gpus)
        else:
            Console.error(f"not enough GPUs available: {host}: {node}")

    def status(self, user=None):

        for host in ["romeo", "volta"]:

            status = self.queue(host=host, user=user)
            print (status)
            print(Printer.attribute(status, header=[host, "Used GPUs"]))

        for host in ["romeo", "volta"]:
            users = self.users(host=host, user=user)
            print()
            print (f"Users on {host}")
            print()
            print (indent("\n".join(users), "    "))
        print()


    def users(self, host=None, user=None):
        command = f"ssh -o LogLevel=QUIET -t {user}@juliet.futuresystems.org " \
                  f" squeue -p {host} -o \"%u\""
        r = check_output(command, shell=True).decode('ascii').split()[1:]
        r = sorted(set(r))
        return r

    def queue(self, host=None, user=None):
        command = f"ssh -o LogLevel=QUIET -t {user}@juliet.futuresystems.org " \
                  f" squeue -p {host}"
        # print(command)

        lines = check_output(command, shell=True).decode('ascii') \
                    .splitlines()[1:]

        used = {}

        for line in lines:
            attributes = line.split()
            gpus = attributes[7]
            try:
                gpus = int(gpus.split(":")[1])
            except:
                gpus = 0
            host = attributes[8]
            if "Unavailable" in host:
                continue
            if host not in used:
                used[host] = 0
            used[host] += gpus
            # print (attributes)


        return used