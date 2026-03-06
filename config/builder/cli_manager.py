
import argparser

def register_arguments(parser, arglist: list):
    for opt in arglist:
        parser.add_argument(opt, default=None)


