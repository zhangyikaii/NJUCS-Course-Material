
from utils import *
from ants import *
from ants_strategies import start_with_strategy

@main
def run(*args):
    Insect.reduce_armor = class_method_wrapper(Insect.reduce_armor,
            pre=print_expired_insects)
    start_with_strategy(args, interactive_strategy)