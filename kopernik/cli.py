#!/usr/bin/env python3.4
import os
import types
import sys

import argh

from kopernik.client import KopernikClient


if __name__ == "__main__":
    argparser = argh.ArghParser()

    host = os.environ.get('KOPERNIK_HOST', 'http://localhost:80/')
    client = KopernikClient(host)

    client_methods=(getattr(client, x) for x in dir(client) if type(getattr(client, x)) == types.MethodType)
    argparser.add_commands(client_methods)

    #if len(sys.argv) < 2:
    #    print("Insufficient arguments.")
    #    sys.exit(2)
    #print("args: {}".format(" ".join(sys.argv[2:])))
    #cli_method = sys.argv[1]
    #cli_args = (x for x in sys.argv[2:] if '=' not in x)
    #kwarg_list = {k[0]: k[1] for k in (x.split('=') for x in sys.argv[2:] if '=' in x)}

    try:
        #print("method: {}, args: {}, kwargs: {}".format(cli_method, ", ".join(cli_args), kwarg_list))
        #result = getattr(client, cli_method)(*cli_args, **kwarg_list)
        #print(result)
        argparser.dispatch()
    except Exception:
        print("Error from {}: {}".format(method, sys.exc_info()[0]))
        sys.exit(1)
