# Order Resolution Psuedocode
```
cut_supports(...):
  for every support:
    if this support is attacked by a convoyed move:
      flag this support as possibly convoy cut
    if this supports a non-move order:
      if there is a move targeting this support:
        determine cut support
      else
        determine non-cut support
    else this supports a move order _m_:
      if the only move targeting this support is from the destination of _m_:
        determine contested support
      if the only move targeting this support is a move _m'_ 
        which requires the fleet _m_ targets to make its attack on this support:
        determine contested support

disrupt_convoys(...):
  for every convoy:
    Assuming constested supports are not cut, determine 
      if this convoy would be disrupted and therefore dislodged.
    If the disruption is dependent on a convoyed move, check to 
      see if that convoy route has any convoy cut supports
    If the removal of some number of those convoy cut supports would 
      change the outcome of disruption, resolve those supports first
    In the case that a loop is formed in resolving convoy cut supports, 
      then all convoys involved are disrupted

    determine whether convoy is disrupted


disrupt_supports(...):
  for every contested support:
    if this supporting unit would be dislodged:
      determine cut support
    otherwise:
      determine non-cut support


resolveMoves(...):
  buildConflicts(...)
  for each move, resolveMove(_m_)

resolveMove(...):
  Compare strength of conflicts to own strength. 
  Pretend conditional conflicts are they strength they would be if real.
  If this move is strongest, determine success
  If a conditional conflict is the strongest or tied, 
    recurse into resolve that one
    check result after this to determine if you are stronger now, 
    if so, determine success
  otherwise, determine failure


buildConflicts(...):
  for each move _m_:
    # Build list of conflicts
    If _m_'s target has a non move in it, add nonmove to conflicts
    If _m_'s target has a move which is targeting _m_, add opposed to conflicts
    If _m_'s target has a move which is not targeting _m_, add chained move to conditional conflicts
    If there is another move _m'_ that shares a target with _m_:
      If _m'_ is opposed add standoff(_m'_) to conditional conflicts
      else add standoff(_m'_) to conflict

resolveOrders(...):
  cut_supports(...)
  disrupt_convoys(...)
  dusrupt_supports(...)
  resolveMoves(...)
```

# Order Resolution Explanation
## Types of Orders
It might be good to further subdivide orders based on their contex:
- Support
  - Support Non-Move
  - Support Move
    - Contested Support (Could be by convoy)

- Moves
  - Opposed Move (_A_ is moving to _B_ and _B_ is moving to _A_)
  - Chained Move (_A_ is moving to _B_, _B_ is moving to _C_)
  - Standoff (_A_ is moving to _B_, _C_ is moving to _B_)
How to resolve moves?
You have to worry about opposed moves, chained moves, standoffs, and their combinations.
An opposed move that is dislodged does not cause a standoff (does not have a claim in destination)

Once supports and convoys are determined, there are only holds and moves (each with a strength) to resolve.

If each hold/move is a vertex in a graph, then whether each pair is in conflict with another is an edge.

Some conflicts are conditional, 
for example, an opposed move is only in conflict with its destination if it is not dislodged.
Similarly a chained move is only in conflict with the move coming into its province if it fails.
    

## 1 Cut Non-Contested and Non-Convoy-Cut Supports

A "Contested Support" is a support of a move _m_ which is only attacked by an enemy move _m'_ in which:
- _m_ is attacking _m'_
- _m_ is attacking a convoy that is necessary?? for move _m'_
A "Convoy Cut Support" is a support that is attacked by a conveyed army (not necessarily cut if the convoy is disrupted)

All other supports are either cut if they are attacked, or left intact if they are not attacked.

## 2 Disrupt Convoys

Unfortunately, convoy paradoxes are slightly possible. 
The state of convoy cut supports is still undetermined, and so we can have cyclical dependencies of these convoy cut supports.
[Can there be branching issues?]

Similarly, if we slightly modify the "Convoyed Attack does not cut certain supports" scenario, we reach a strange scenario.
Here we assume the constested support is not cut and resolve the disruption of the convoy accordingly, then later resolve the disruption of the contested support?
This means it is possible for a support to go through and also be disrupted.
[Can a support not be contested, but instead linked contested? Convoy cut chain that contests? This would always be a cycle! Resolved by cycle rule]

During this stage, for the purpose of disrupting convoys, assume that contested supports are not cut?
(even though there is one very specific case where they may later be dislodged).

If a convoy's disruption is affected by a move that is supported by a convoy cut support, resolve that convoy cut support first.
If the recurse into conditional convoy cut supports forms a cycle, all of the convoys fail, and none of the convoy cut supports are cut.

## 3 Disrupt Supports

Contested supports could be dislodged by a move. The only valid move into a contested support now comes from either the unit a support is attacking, or is convoyed from the unit a support is attacking.
Convoys have been decided as disrupted or not disrupted, so now we have enough information to tell if the contested support was dislodged. All other supports have either been cut or weren't attacked.
Check all contested supports to see if they will be dislodged. If they will be dislodged, cut them.

## 4 Resolve Moves

For each move, determine how it conflicts with other orders (moves and non-moves).
Other orders can conflict with move _m_ in the following ways:
- Nonmove. If _m_'s target province has a non-moving unit in it (support, convoy, or hold), that order conficts with _m_.
- Opposed move. If _m_'s target province has a unit moving into _m_'s province, that move conflicts with _m_ unless one of the moves are convoyed.
- Chained move. If _m_'s target province has a unit moving somewhere other than _m_'s province, that move conditionally conflicts with _m_. If that move succeeds, there is no conflict.
- Standoff. If another move has the same destination province as _m_, that move conflicts with _m_.
  - If the other move is opposed, the move conditionally conflicts with _m_. If the other unit is dislodged, there is no conflict, otherwise there is.

Determine conflicts (claims that would prevent a move from succeeding) and conditional conflicts (moves that could fail, creating a conflict).
Resolve each move by comparing its strength to that of other conflicts, resolving conditional conflicts __if necessary__

Standoff Conditional Conflict: 
A standoff conditional conflict cannot be dependent on any other conditional conflicts, as the order it is dependent on is an opposed move. 
An opposed move can't have a chained move it is dependent on, and there can only be one standoff conditional conflict per destination province.

Chained Conditional Conflict:
It can be the case that a chained conditional conflict is dependent on another conditional conflict. 
These conflicts must be traveled to recursively to resolve the lowest dependency before resolving the original move.
It is possible that a cycle of chained conditional conflicts can form. When this happens, all moves in the cycle succeed.
(A 2-cycle is simply found as an opposed move, and is not a chained conditional conflict)

# Pure Conditionals Logic
(I wasn't able to finish this, Chris)

Chris has proposed using "conditionals" to resolve game logic. 

This involves looking at every order and either:

- Immediately resolve that order
- Add one or more properties as _conditionals_ which must be resolved before this order is resolved

By defining an ordering of these conditionals, we can know what loops will be able to form, and resolve those loops when they appear.

## What are conditionals for each order type?

### Hold
Supporting orders are conditionals.
Attacking moves are conditionals?

### Move
Supporting orders are conditionals.
An opposing move (swapped src and dest) is a conditional.
A standoff move or hold (same destination) is a conditional.
If move is convoyed, all conveyors are conditionals.

### Support (Non-move)
Immediately resolvable (cut if attacked)

### Support (Move)
Immediately resolvable if not contested support, or if not attacked
Otherwise, this is a contested support:
An attacking move is a conditional (support is cut if dislodged).

### Convoy
An attacking move is a conditional (convoy is disrupted if dislodged).

When a move is resolved, its conditionals are decided one by one, 