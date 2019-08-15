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
        print("LLL", locals())

        print (Printer.attribute(status, header=["Node", "Used GPUs"]))


        #
        # Required node not available (down, drained or reserved)
        #

        reserved = self.reserved_nodes(user=user)

        def hostnames(host):
            if host == "volta":
                names = Parameter.expand("r-00[5-6]")
            else:
                names = Parameter.expand("r-00[1-4]")

            max_gpus = 8  # this is for now hard coded
            valid = []
            for name in names:
                if name not in reserved and status[name] + gpus <= max_gpus:
                    valid.append(name)
            return valid

        def find_random(host):
            names = hostnames(host)

            if len(names) == 0 or names is None:
                return None
            id = random.randint(0, len(host) - 1)
            return names[id]

        def find_first(host):

            names = hostnames(host)

            if names is None or len(names) == 0:
                return None
            else:
                return names[0]

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

    def reserved_nodes(self, user=None):

        reservation = self.reservations(user=user)

        _reserved_nodes = []
        for r in reservation:
            nodes = Parameter.expand(r["Nodes"])
            _reserved_nodes = _reserved_nodes + nodes

        return _reserved_nodes

    def status(self, user=None):

        reservation = self.reservations(user=user)
        print(Printer.write(reservation))

        reserved = self.reserved_nodes(user=user)

        #
        # BUG check for date
        #

        # print (reserved)

        for host in ["romeo", "volta"]:

            status = self.queue(host=host, user=user)

            print()
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

    def reservations(self, user=None):
        command = f"ssh -o LogLevel=QUIET -t {user}@juliet.futuresystems.org " \
                  f" scontrol -a -d -o show res"
        result = check_output(command, shell=True).decode('ascii').splitlines()
        r = []
        for line in result:
            data = {}
            entry = line.split(" ")
            for element in entry:
                attribute, value = element.split("=")
                data[attribute] = value
            r.append(data)
        return r
