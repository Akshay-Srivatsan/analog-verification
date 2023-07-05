from enum import Enum
from typing import List
from dataclasses import dataclass, field
from core.expr import VarType, Var, VarAssign, Integrate, Accumulate 


class VarKind(Enum):
    Input = "input"
    Output = "output"
    StateVar = "state-var"
    Transient = "trans"
    Time = "time"

@dataclass
class VarInfo:
    name : str
    type : VarType
    kind : VarKind
    variable: Var = None

    def __post_init__(self):
        self.variable = Var(self.name)
        self.variable.type = self.type

    @property 
    def stateful(self):
        return self.kind == VarKind.StateVar

class AMSBlock:

    def __init__(self,name):
        self.name = name
        self._vars = {}
        self._relations = []

    def get_var(self, v):
        return self._vars[v]

    def interval(self,v):
        return self._vars[v.name].intervals

    def _filter_variables(self,k:VarKind):
        return filter(lambda v: v.kind == k, self._vars.values())

    def vars(self):
        return self._vars.values()

    def outputs(self):
        return self._filter_variables(VarKind.Output)

    def inputs(self):
        return self._filter_variables(VarKind.Input)

    def inputs(self):
        return self._filter_variables(VarKind.StateVar)


    def relations(self):
        return self._relations

    def set_intervals(self,v,ivals):
        self._intervals[v.name].add_intervals(ivals)

    def decl_relation(self,eq):
        assert(not eq is None)
        self._relations.append(eq)

    def decl_var(self,name:str,kind:VarKind,type:VarType):
        self._vars[name] = VarInfo(name=name,kind=kind,type=type)
        return self._vars[name].variable

    def __repr__(self):
        stmts = []
        def q(s):
            stmts.append(s)
        for v in self.vars():
            q(str(v))
        q("")
        for r in self.relations():
            q(r.pretty_print())
        return "\n".join(stmts)


def execute_block(blk, args):
    vals = dict(args)
    for rel in blk.relations():
        if isinstance(rel, VarAssign):
            rhs_val = rel.rhs.execute(vals)
            vals[rel.lhs.name] = rel.rhs.type.to_real(rhs_val)
        elif isinstance(rel,Integrate):
            rhs_val = rel.rhs.execute(vals)
            vals[rel.lhs.name] += rel.rhs.type.to_real(rhs_val)
        elif isinstance(rel,Accumulate):
            rhs_val = rel.rhs.execute(vals)
            vals[rel.lhs.name] += rel.rhs.type.to_real(rhs_val)

        else:
            raise Exception("not supported: %s" % rel)
    return vals