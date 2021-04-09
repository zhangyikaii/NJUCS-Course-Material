from enum import Enum
from typing import List, Union, Dict, Tuple, TYPE_CHECKING

from datamodel import Expression, ValueHolder, Pair, Nil, Symbol, Undefined, Promise, NilType, UndefinedType
import evaluate_apply
from helper import pair_to_list
from log_utils import get_id
from scheme_exceptions import OperandDeduceError

if TYPE_CHECKING:
    import graphics

OP_LIMIT = 25000


class HolderState(Enum):
    UNEVALUATED = 1
    EVALUATING = 2
    EVALUATED = 3
    APPLYING = 4


class FakeObj:
    def __getattr__(self, item):
        return fake_obj

    def __getitem__(self, item):
        return fake_obj

    def __call__(self, *args, **kwargs):
        return fake_obj


fake_obj = FakeObj()


class VisualExpression:
    def __init__(self, base_expr: Expression = None, true_base_expr: Expression = None):
        self.display_value = base_expr
        self.base_expr = base_expr if true_base_expr is None else true_base_expr
        self.value: Expression = None
        self.children: List[Holder] = []
        self.id = get_id()

        if logger.op_count >= OP_LIMIT:
            self.children = fake_obj
            return

        if base_expr is None:
            return
        if isinstance(base_expr, ValueHolder) \
                or isinstance(base_expr, evaluate_apply.Callable) \
                or isinstance(base_expr, Promise) \
                or base_expr == Nil \
                or base_expr == Undefined:
            self.value = base_expr
        elif isinstance(base_expr, Pair):
            try:
                self.set_entries(pair_to_list(base_expr))
            except OperandDeduceError:
                self.set_entries([base_expr.first, base_expr.rest])
        else:
            raise NotImplementedError(base_expr, type(base_expr))

    def set_entries(self, expressions: Union[List[Expression], List['VisualExpression']]):
        self.value = None
        self.children = [Holder(expression, self) for expression in expressions]
        if expressions and isinstance(expressions[0], VisualExpression):
            if self.id in logger.node_cache:
                if logger.node_cache[self.id].transitions:
                    curr_transition = HolderState[logger.node_cache[self.id].transitions[-1][-1]]
                else:
                    return self
                logger.node_cache[self.id].modify(self, curr_transition)
        return self

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        return str(self.display_value)


class Holder:
    def __init__(self, expr: Expression, parent: VisualExpression):
        self.expression: VisualExpression = VisualExpression(expr) if isinstance(expr, Expression) else expr
        self.state = HolderState.UNEVALUATED
        self.parent = parent

    def evaluate(self):
        self.state = HolderState.EVALUATING
        announce("Evaluating", self, Root.root)

    def apply(self):
        self.state = HolderState.APPLYING
        announce("Applying", self, Root.root)

    def complete(self):
        self.state = HolderState.EVALUATED
        announce("Completed", self, Root.root)

    def __repr__(self):
        return repr(self.expression)


class Root:
    root: Holder
    set: bool = False

    @classmethod
    def setroot(cls, root: Holder):
        cls.root = root


def limited(f):
    def g(*args, **kwargs):
        if not logger.log_op() and not kwargs.get("force", False):
            return
        if "force" in kwargs:
            del kwargs["force"]
        return f(*args, **kwargs)
    return g


class Logger:
    def __init__(self):
        self._out = [[]]  # text printed to console

        self.i = 0  # number of "steps" in the substitution tree
        self.start = 0  # the step of the current expr

        self.f_delta = 0  # the index of the first frame to generate
        self.frame_lookup: Dict[int, StoredFrame] = {}  # lookup of all previous frames TODO: use weakrefs or something
        self.active_frames: List[StoredFrame] = []  # new frames to be added to the js frame store
        self.frame_updates = []  # when the env diagram is updated
        self.global_frame: StoredFrame = None

        self.dotted = False  # Whether dotted lists are allowed (i.e. fa18 vs sp19 Scheme)
        self.strict_mode = False  # legacy - used for okpy testing of the interpreter
        self.fragile = False  # flag for if new assignments prohibited, like in previewing

        self.autodraw = True

        self.show_thunks = True

        self.node_cache: Dict[str, Node] = {}  # a cache of visual expressions
        self.export_states = []  # all the nodes generated in the current evaluation, in exported form
        self.roots = []  # the root node of each expr we are currently evaluating

        self.eval_stack = []  # the eval stack for use in tracebacks

        self.heap: Heap = Heap()  # heap of all non-atomic objects

        self.graphics_lookup = {}
        self.graphics_open = False

        self.op_count = 0

    def new_expr(self):
        self._out.append([])
        if Root.set and self.start != self.i:
            self.export_states.append((self.start, self.i, {i: v.export() for i, v in self.node_cache.items()}))
            self.roots.append(Root.root.expression.id)
        self.start = self.i
        self.node_cache = {}
        Root.set = True
        self.eval_stack = []

    def new_query(self, global_frame: 'StoredFrame'=None, curr_i=0, curr_f=0):
        self.node_cache = {}
        self.i = curr_i
        self.f_delta = curr_f
        self.start = curr_i
        self._out = []
        self.active_frames = []
        self.roots = []
        self.export_states = []
        self.frame_updates = []
        self.global_frame = global_frame
        self.graphics_open = False
        self.op_count = 0

    def get_canvas(self) -> 'graphics.Canvas':
        self.graphics_open = True
        return self.graphics_lookup[id(self.global_frame.base)]

    def preview_mode(self, val):
        self.fragile = val

    def visualize_tail_calls(self, val):
        self.show_thunks = not val

    @limited
    def log(self, message: str, local: Holder, root: Holder):
        self.new_node(local.expression, local.state)
        self.i += 1

    def export(self):
        return {
            "success": True,
            "roots": self.roots,
            "states": self.export_states,
            "out": ["".join(["".join(x) for x in self._out])],
            "active_frames": [id(f.base) for f in self.active_frames],
            "frame_lookup": {id(f.base): self.frame_lookup[id(f.base)].export()
                             for f in [self.global_frame] + self.active_frames},
            "graphics_open": self.graphics_open,
            "graphics": self.get_canvas().export(),
            "globalFrameID": id(self.active_frames[0].base) if self.active_frames else -1,
            "heap": self.heap.export(),
            "frameUpdates": sorted(set(self.frame_updates))
        }

    def out(self, val, end="\n"):
        self.raw_out(repr(val) + end)

    def raw_out(self, val):
        if self._out:
            self._out[-1].append(val)
        else:
            self._out = [[val]]

    @limited
    def frame_create(self, frame: 'evaluate_apply.Frame'):
        self.frame_lookup[id(frame)] = stored = StoredFrame(len(self.active_frames), frame)
        self.active_frames.append(stored)
        frame.id = stored.name

    @limited
    def frame_store(self, frame: 'evaluate_apply.Frame', name: str, value: Expression):
        self.frame_lookup[id(frame)].bind(name, value)

    def new_node(self, expr: VisualExpression, transition_type: HolderState):
        if expr.id in self.node_cache:
            return self.node_cache[expr.id].modify(expr, transition_type, force=True)
        node = Node(expr, transition_type)
        self.node_cache[node.id] = node
        return node.id

    def log_op(self):
        self.op_count += 1
        # print(self.op_count)
        return self.op_count < OP_LIMIT


class Node:
    def __init__(self, expr: VisualExpression, transition_type: HolderState):
        self.transitions = []
        self.str = []
        self.base_str = []
        self.children = []
        self.id = expr.id
        self.modify(expr, transition_type)

    @limited
    def modify(self, expr: VisualExpression, transition_type: HolderState):
        if not self.transitions or self.transitions[-1][1] != transition_type.name:
            self.transitions.append((logger.i, transition_type.name))
        if not self.str or self.str[-1][1] != repr(expr):
            self.str.append((logger.i, repr(expr)))

        while self.children and self.children[-1][0] == logger.i:
            self.children.pop()

        if expr.value is None:
            self.children.append(
                (logger.i,
                 [logger.new_node(child.expression, child.state) for child in expr.children]))
        else:
            self.children.append((logger.i, []))

        new_base_str = repr(expr.base_expr)

        if not self.base_str or self.base_str[-1][1] != new_base_str:
            self.base_str.append((logger.i, new_base_str))

        return self.id

    def export(self):
        return {
            "transitions": self.transitions,
            "strs": self.str,
            "parent_strs": self.base_str,
            "children": [(i, [x for x in y]) for i, y in self.children]
        }


class StoredFrame:
    def __init__(self, i, base: 'evaluate_apply.Frame'):
        i += logger.f_delta
        if i == -1:
            name = "Builtins"
        elif i == 0:
            name = "Global"
        else:
            name = f"f{i}"
        self.name = name
        self.label = base.name
        self.parent = base.parent
        self.bindings = []
        self.base = base
        self.return_value = None

    @limited
    def bind(self, name: str, value: Expression):
        value_key = logger.heap.record(value)
        data = (logger.i, (name, str(value)), value_key)
        self.bindings.append(data)
        self.add_index(logger.i)

    @staticmethod
    def add_index(i):
        if not logger.frame_updates or logger.frame_updates[-1] != i:
            logger.frame_updates.append(i)

    def export(self):
        if id(self.parent) not in logger.frame_lookup:
            return None
        return {"name": self.name,
                "label": self.label,
                "parent": logger.frame_lookup[id(self.parent)].name,
                "bindings": self.bindings}


class Heap:
    HeapKey = Tuple[bool, Union[int, str]]  # the bool means that I'm NOT a pointer!
    HeapObject = Union[List['HeapObject'], HeapKey]

    def __init__(self):
        self.prev: Dict[str, Heap.HeapObject] = {}
        self.curr: Dict[str, Heap.HeapObject] = {}

    def export(self):
        out = self.curr
        self.prev.update(self.curr)
        self.curr = {}
        return out

    @limited
    def modify(self, id):
        if id in self.prev:
            self.curr[id] = self.prev[id]
        logger.frame_updates.append(logger.i)

    def record(self, expr: Expression) -> 'Heap.HeapKey':
        if isinstance(expr, evaluate_apply.Thunk):
            return False, "thunk"
        if expr.id is None:
            expr.id = get_id()
        if expr.id not in self.prev and expr.id not in self.curr:
            if isinstance(expr, ValueHolder):
                return False, repr(expr)
            elif isinstance(expr, Pair):
                val = [self.record(expr.first), self.record(expr.rest)]
            elif isinstance(expr, Promise):
                val = expr.bind()
            elif isinstance(expr, NilType):
                return False, "nil"
            elif isinstance(expr, UndefinedType):
                return False, "undefined"
            else:
                # assume the repr method is good enough
                val = [(False, repr(expr))]
            self.curr[expr.id] = val
        return True, expr.id


return_symbol = Symbol("Return Value")

logger = Logger()
announce = logger.log
