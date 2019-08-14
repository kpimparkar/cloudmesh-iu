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

          This command does some useful things.

          Arguments:
              FILE   a file name
              HOST   the host is either rome or volta [default: romeo]

          Options:
              -f      specify the file

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





        arguments["host"] = Parameter.find("host", arguments, variables,
                                           {"host": "romeo"})
        arguments["node"] = Parameter.find("node", arguments, variables)
        arguments["gpu"] = int(Parameter.find("gpu", arguments, variables,
                                          {"gpu": "1"}))


        if arguments.node is None:

            if arguments.host == "volta":
                random.randint(1, 2) + 4

            else:
                number = random.randint(1, 4)
            arguments.node = f"r-00{number}"


        VERBOSE(arguments)

        banner("Login")


        iu.smart_login(user=arguments.user,
                 host=arguments.host,
                 node=arguments.node,
                 gpus=arguments.gpu)

        return ""
