from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from typing import Dict, Set, List, Any

class EvaluationException(Exception):
    pass

class Sentence(ABC):
    def __init__(self):
        self._cache: Dict[frozenset, bool] = {}
    
    def evaluate(self, model: Dict[str, bool])->bool:
        key = frozenset(model.items())
        if key not in self._cache:
            self._cache[key] = self._evaluate(model)
        return self._cache[key]
    
    @abstractmethod
    def _evaluate(self, model: Dict[str,bool])->bool: raise NotImplementedError
    @abstractmethod
    def formula(self) ->str: raise NotImplementedError
    @abstractmethod
    def symbols(self)->Set[str]: raise NotImplementedError
    
    def __and__(self, other:Sentence)-> And: return And(self, other)
    def __or__(self, other:Sentence) -> Or: return Or(self, other)
    def __invert__(self)->Not: return Not(self)
    
    @classmethod
    def validate(cls, sentence:Any):
        if not isinstance(sentence, Sentence): raise TypeError("must be a logical sentence!")
            
    @classmethod
    def parenthesize(cls, s:str)->str:
        def balance(s):
            count = 0
            for c in s:
                if c =="(" :count += 1
                elif c ==")":
                    if count <= 0: return False
                    count -=1
            return count == 0
        if not len(s) or s.isalpha() or (s[0] == "(" and s[-1] == ")" and balance(s[1:-1])):
            return s
        else:
            return f"({s})"

class Symbol(Sentence):
    def __init__(self, name:str):
        super().__init__()
        self.name = name

    def __eq__(self, other: Any) -> bool: return isinstance(other, Symbol) and self.name == other.name
    def __hash__(self)->int: return hash(("symbol", self.name))
    def __str__(self) -> str: return self.name
    def __repr__(self)->str: return self.name
    
    def _evaluate(self, model: Dict[str, bool])->bool:
        try:
            return model[self.name]
        except KeyError:
            raise EvaluationException(f"variable {self.name} not in model") 

    def formula(self) -> str: return self.name

    def symbols(self)->Set[str]: return {self.name}
    
class Not(Sentence):
    def __init__(self, operand: Sentence):
        super().__init__()
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other: Any) -> bool: return isinstance(other, Not) and self.operand == other.operand
    def __hash__(self)->int: return hash(("not", self.operand))
    def _evaluate(self, model: Dict[str, bool]) -> bool: return not self.operand.evaluate(model)
    def formula(self) -> str: return f"¬{Sentence.parenthesize(self.operand.formula())}"
    def symbols(self) -> Set[str]: return self.operand.symbols()
    
class And(Sentence):
    def __init__(self, *conjuncts: Sentence):
        super().__init__()
        self.conjuncts: List[Sentence] = []
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
            if isinstance(conjunct, And):
                self.conjuncts.extend(conjunct.conjuncts)
            else:
                self.conjuncts.append(conjunct)

    def __eq__(self, other: Any) -> bool: return isinstance(other, And) and set(self.conjuncts) == set(other.conjuncts)    
    def __hash__(self) -> int: return hash(("and", frozenset(self.conjuncts)))
    def _evaluate(self, model: Dict[str, bool]) -> bool: return all(c.evaluate(model) for c in self.conjuncts)
    
    def formula(self) -> str :
        if not self.conjuncts: return "True"
        if len(self.conjuncts) == 1: return self.conjuncts[0].formula()
        conj_formulas = [Sentence.parenthesize(c.formula()) for c in self.conjuncts]
        return " ∧ ".join(conj_formulas)
    
    def symbols(self) -> Set[str]:
        if not self.conjuncts: return set()
        return set.union(*[c.symbols() for c in self.conjuncts])
    
class Or(Sentence):
    def __init__(self, *disjuncts: Sentence):
        super().__init__()
        self.disjuncts: List[Sentence] = []
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
            if isinstance(disjunct, Or):
                self.disjuncts.extend(disjunct.disjuncts)
            else:
                self.disjuncts.append(disjunct)
    
    def __eq__(self, other: Any) -> bool: return isinstance(other, Or) and set(self.disjuncts) == set(other.disjuncts)
    def __hash__(self) -> int: return hash(("or", frozenset(self.disjuncts)))
    def _evaluate(self, model: Dict[str, bool]) -> bool: return any(d.evaluate(model) for d in self.disjuncts)
    
    def formula(self) ->str:
        if not self.disjuncts: return "False"
        if len(self.disjuncts) == 1 : return self.disjuncts[0].formula()
        disj_formulas = [Sentence.parenthesize(d.formula()) for d in self.disjuncts]
        return " ∨ ".join(disj_formulas)
    
    def symbols(self) -> Set[str]:
        if not self.disjuncts: return set()
        return set.union(*[d.symbols() for d in self.disjuncts])

class Implication(Sentence):
    def __init__(self, antecedent: Sentence, consequent: Sentence):
        super().__init__()
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other: Any) -> bool: return (isinstance(other, Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent)
    def __hash__(self) -> int: return hash(("implies", self.antecedent, self.consequent))
    def _evaluate(self, model: Dict[str, bool]) -> bool: return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)
    
    def formula(self) -> str:
        ante = Sentence.parenthesize(self.antecedent.formula())
        cons = Sentence.parenthesize(self.consequent.formula())
        return f"{ante} => {cons}"

    def symbols(self) -> Set[str]:
        return self.antecedent.symbols().union(self.consequent.symbols())

class Biconditional(Sentence):
    def __init__(self, left: Sentence, right: Sentence):
        super().__init__()
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other:Any) -> bool: return (isinstance(other, Biconditional) and self.left == other.left and self.right == other.right)
    def __hash__(self) -> int: return hash(("biconditional", self.left, self.right))
    def _evaluate(self, model:Dict[str, bool]) -> bool: return self.left.evaluate(model) == self.right.evaluate(model)
    
    def formula(self) -> str:
        left_f = Sentence.parenthesize(self.left.formula())
        right_f = Sentence.parenthesize(self.right.formula())
        return f"{left_f} <=> {right_f}"
    
    def symbols(self) -> Set[str]:
        return self.left.symbols().union(self.right.symbols())


def model_check(knowledge, query, all_symbols):
    def evaluate_kb(model):
        try:
            return knowledge.evaluate(model)
        except EvaluationException:
            return False
            
    for p in itertools.product([True, False], repeat=len(all_symbols)):
        model = {symbol.name : value for symbol,value in zip(all_symbols, p)}
    
        if evaluate_kb(model) and not query.evaluate(model):
            return False
    return True

herman = Symbol("Dr. herman")
ahmad = Symbol("Col. ahmad")
zhang = Symbol("Prof zhang niu")
characters = [herman, ahmad, zhang]

livingroom = Symbol("livingroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [livingroom, kitchen, library]

knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

all_symbols = characters + rooms + weapons

def exactly_one(symbols):
    at_least_one = Or(*symbols)
    at_most_one = And(*[
        Or(Not(a), Not(b))
        for a in symbols
        for b in symbols
        if a != b
    ])
    return And(at_least_one, at_most_one)

knowledge_points = [
    exactly_one(characters),
    exactly_one(rooms),
    exactly_one(weapons),
]

knowledge_points.append(Not(ahmad))  
knowledge_points.append(Not(knife))   
knowledge_points.append(Not(zhang)) 
knowledge_points.append(Not(wrench))
knowledge_points.append(Not(livingroom))
knowledge_points.append(Not(kitchen))

    

knowledge = And(*knowledge_points)

def check_knowledge(knowledge):
    print("\n--- STATUS PENGETAHUAN ---")

    know_true = []
    know_false = []
    for symbol in all_symbols:
        if model_check(knowledge, symbol, all_symbols):
            print(f"✅ {symbol}: YES")
            know_true.append(symbol)
        elif model_check(knowledge, Not(symbol), all_symbols):
            know_false.append(know_false)
        else:
            print(f"🤔 {symbol}: MAYBE")

    know_char = [s for s in know_true if s in characters]
    know_waepon = [s for s in know_true if s in weapons]
    know_room = [s for s in know_true if s in rooms]

    if len(know_char) == 1 and len(know_room) == 1 and len(know_waepon) == 1:
        char = characters[0]
        weapon = weapons[0]
        room = rooms[0]
        print(f"the killer is {char} using {weapon} in {room}")
    else:
        print("there is no streng evidence ")

check_knowledge(knowledge)
