import os
from subprocess import check_output
from cloudmesh.common3.Shell import Shell
from cloudmesh.common.Printer import Printer
from textwrap import indent
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

    def status(self, user=None):

        for host in ["romeo", "volta"]:

            status = self.queue(host=host, user=user)
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