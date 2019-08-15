from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand, map_parameters
from cloudmesh.iu.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.variables import Variables
from cloudmesh.common.util import banner
from cloudmesh.common.Printer import Printer

from cloudmesh.configuration.Config import Config
import random

class IuCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_iu(self, args, arguments):
        """
        ::

          Usage:
                iu [--user=USERNAME] [--host=HOST] [--node=NUMBER] [--gpu=GPUS]
                iu status
                iu res

          This command allows you to inteactively log into roeo or volta

          Arguments:
              FILE    a file name
              HOST    the host is either rome or volta [default: romeo]
              NUMBER  is a number that specifies where to login
              GPUS    the number of GPU's to be used


          Example:

              cms iu
                 logs in on the first available node, and uses 1 GPU
                 BUG: some reservation are not detected

              cms iu --node=random
                 logs in on the first available node and uses 1 GPU

              cms iu status
                 lists the status of rome and volta. The output will look like:


                    +-------------+-----------+
                    | romeo       | Used GPUs |
                    +-------------+-----------+
                    | r-001       |           |
                    | r-002       | 7         |
                    | r-003       | 7         |
                    | r-004       | 7         |
                    +-------------+-----------+

                    +-------+-----------+
                    | volta | Used GPUs |
                    +-------+-----------+
                    | r-005 | 5         |
                    | r-006 | 7         |
                    +-------+-----------+

                    Users on romeo

                        user1

                    Users on volta

                        user2
        """

        map_parameters(arguments,
                       "user",
                       "host",
                       "node",
                       "gpu")

        variables = Variables()
        arguments["user"] = Parameter.find("user", arguments, variables)

        if arguments.user is None:
            config = Config()
            arguments.user = config["cloudmesh.iu.user"]

        iu = Manager()


        if arguments.status:

            iu.status(user=arguments.user)

            return ""

        elif arguments.res:

            iu.reservations(user=arguments.user)

            return ""

        else:

            arguments["host"] = Parameter.find("host", arguments, variables,
                                               {"host": "romeo"})
            arguments["node"] = Parameter.find("node", arguments, variables)
            arguments["gpu"] = int(Parameter.find("gpu", arguments, variables,
                                                  {"gpu": "1"}))

            VERBOSE(arguments)

            banner("Login")

            iu.smart_login(user=arguments.user,
                           host=arguments.host,
                           node=arguments.node,
                           gpus=arguments.gpu)

        return ""
