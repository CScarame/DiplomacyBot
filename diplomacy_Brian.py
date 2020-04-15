
from typing import List, Union, Optional, Tuple, NewType
from enum import Enum, auto

class DiplomacyError(Exception):
    pass

class OrderException(Exception):
    pass

class UnitType(Enum):
    ARMY = auto()
    FLEET = auto()

Nation = NewType("Nation", str)

class Unit:
    # Constructor: Unit(kind,nation,province)
    kind:UnitType
    nation:Nation
    province:'Province'
    order:'Order' = None
    is_dislodged:bool = False

    def get_str(self) -> int:
        sups = [s for s in self.order.supports if not s.is_cut]
        return len(sups) + 1

    def test_dislodge(self) -> bool:

        claims : List[Move] = self.province.claims
        claim_strengths : List[Tuple[Move,int]] = [(c,c.unit.get_str()) for c in claims]
        max_strength : int = max([c[1] for c in claim_strengths])

        # In the case that the hold is successful...
        if max_strength <= self.get_str():
            return False
        
        winners = [c for (c,cs) in claim_strengths if cs == max_strength]

        if len(winners) > 1:
            # Standoff!
            return False
        elif len(winners) == 1:
            # This unit will be dislodged
            return True

    def relocate(self, other_province:'Province'):
        # TODO: make sure other province is valid for this unit
        self.province.unit = None
        self.province = other_province
        self.province.unit = self

class Province:
    name:str
    abbr:str
    army_adj:List['Province']
    water_adj:List['Province']
    claims:List['Move']
    unit:Optional[Unit]
    retreat:Optional[Unit]

    def resolve(self):
        """ Resolve the claims, if any, on this province """
        if len(self.claims) == 0:
            # Nothing
            return
        claim_strengths : List[Tuple[Move,int]] = [(c,c.unit.get_str()) for c in self.claims]
        max_strength : int = max([c[1] for c in claim_strengths])

        winners = [(c,cs) for (c,cs) in claim_strengths if cs == max_strength]

        if len(winners) > 1:
            # Standoff
            return
        elif len(winners) == 1:
            winner = winners[0]
            if self.unit == None:
                # Take empty prov
                winner[0].relocate(self)
                return
            elif self.unit.get_str() < winner[1]:
                # Dislodge unit and take
                self.unit.is_dislodged = True
                winner[0].relocate(self)
            else:
                # Successful defense
                return

class Supply_Center(Province):
    nation:Nation

class Order:
    def __init__(self, unit:Optional[Unit]=None, province:Optional[Province]=None):
        self.unit:Unit
        if not unit == None: # Unit was declared, use it
            self.unit = unit
        elif not province == None: # Province was declared, try it
            if not province.unit == None: # As long
                self.unit = province.unit
            else:
                raise OrderException("No unit at that province!")
        else:
            raise DiplomacyError("Order specified without Unit or Province")
        self.unit.order = self
        self.supports:List['Support'] = []


class Hold(Order):
    def __init__(self, unit:Union[Unit,Province]):
        super().__init__(unit)

class Move(Order):
    def __init__(self, unit:Union[Unit,Province], target:Province):
        super().__init__(unit)
        self.target:Province = target
        self.convoys:List['Convoy'] = []
        self.conflictsList[Union[Order, Unit]] = []
        self.gathered_conflicts = False
        self.conditional_conflict = None

    def gather_conflicts(self) -> bool:
        if self.gathered_conflicts:
            return False
        
        self.conflicts += [mov for mov in self.target.claims]
        enemy = self.target.unit
        if enemy != None:
            if isinstance(enemy.order, Move) and enemy.order.target == self.unit.province:
                self.conditional_conflict = enemy.order
            else:
                self.conflicts += [enemy]
        self.gathered_conflicts = True
        return True

    def resolve(self) -> bool:
        """ Move unit to target if move successful and dislodge any target """

class Support(Order):
    def __init__(self, unit:Union[Unit,Province], order:Order):
        super().__init__(unit)
        self.order:Order = order
        self.order.supports.append(self)
        self.is_cut:bool = False

    def cut_initial(self) -> bool:
        """ Cut supports that are attacked unless that attack is convoyed by a convoy that is attacked.
        return: If the support is cut in this function
        """
        if self.is_cut:
            return False
        
        province = self.unit.province
        claims = province.claims

        for claim in claims:
            should_cut:bool = True
            if claim.unit.nation == self.unit.nation:
                self.should_cut = False
            else:
                for convoy in claim.convoys:
                    if not len(convoy.unit.province.claims) == 0:
                        should_cut = False
            if should_cut:
                self.is_cut = True
                return True
        return False

    def cut(self) -> bool:
        """ Cut supports that are attacked """
        if self.is_cut:
            return False

        # Get all claims that are not from this nation
        claims = [c for c in self.unit.province.claims if c.unit.nation != self.unit.nation]
        if len(claims) > 0:
            self.is_cut = True
            return True
        return False

class Convoy(Order):
    def __init__(self, unit:Union[Unit,Province], move:Move):
        super().__init__(unit)
        self.move:Move = move
        self.move.convoys.append(self)
        self.is_disrupted:bool = False

    def disrupt(self) -> bool:
        """ Disrupt convoys that are dislodged """
        if self.is_disrupted:
            return False

        if self.unit.test_dislodge():
            self.is_disrupted = True
            return True

    # TODO: Convoy validations

def get_order_strings() -> List[str]:
    return []

def parse_and_build_orders(order_str:List[str]) -> List[Order]:
    return []


def main_loop():

    order_str : List[str] = get_order_strings()

    orders :List[Order] = parse_and_build_orders(order_str)

    initial_cuts : List[Tuple[Support,bool]] = [(sup,sup.cut_initial()) for sup in orders if isinstance(sup,Support)]

    convoy_disrupts : List[Tuple[Convoy,bool]] = [(conv, conv.disrupt()) for conv in orders if isinstance(conv, Convoy))]

    second_cuts : List[Tuple[Support,bool]] = [(sup,sup.cut()) for sup in orders if isinstance(sup,Support) and not sup.is_cut]

    move_resolutions : List[Tuple[Move,bool]] = [(mov,mov.resolve()) for mov in orders if isinstance(mov,Move)]

    




