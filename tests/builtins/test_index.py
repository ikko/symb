import pytest
from symb import Symbol
from builtin.index import SymbolIndex

@pytest.fixture
def owner_symb():
    return Symbol("owner_index")

@pytest.fixture
def empty_symb_index(owner_symb):
    return SymbolIndex(owner_symb)

def test_symb_index_instantiation(owner_symb):
    index = SymbolIndex(owner_symb)
    assert index.owner == owner_symb
    assert index.tree.root is None

def test_symb_index_insertion(empty_symb_index):
    s1 = Symbol("sym1")
    s2 = Symbol("sym2")
    s3 = Symbol("sym3")

    empty_symb_index.insert(s2, 50.0) # Root
    empty_symb_index.insert(s1, 25.0) # Left child
    empty_symb_index.insert(s3, 75.0) # Right child

    # In-order traversal should return symbs sorted by weight
    inorder = empty_symb_index.traverse(order="in")
    assert inorder == [s1, s2, s3]

    # Test inserting with callable weight
    s4 = Symbol("sym4")
    def dynamic_weight(sym):
        return len(sym.name) * 2
    empty_symb_index.insert(s4, dynamic_weight)
    # Verify that the symb is in the tree and its weight is correctly evaluated
    assert empty_symb_index.tree.search(dynamic_weight(s4)) is s4

def test_symb_index_traverse_inorder(empty_symb_index):
    s_nodes = [
        (Symbol("sym_d"), 40.0),
        (Symbol("sym_b"), 20.0),
        (Symbol("sym_f"), 60.0),
        (Symbol("sym_a"), 10.0),
        (Symbol("sym_c"), 30.0),
        (Symbol("sym_e"), 50.0),
        (Symbol("sym_g"), 70.0),
    ]
    for sym, weight in s_nodes:
        empty_symb_index.insert(sym, weight)

    expected_inorder = [
        Symbol("sym_a"), Symbol("sym_b"), Symbol("sym_c"), Symbol("sym_d"),
        Symbol("sym_e"), Symbol("sym_f"), Symbol("sym_g")
    ]
    actual_inorder = empty_symb_index.traverse(order="in")
    assert actual_inorder == expected_inorder

def test_symb_index_map_and_filter(empty_symb_index):
    s_nodes = [
        (Symbol("apple"), 10.0),
        (Symbol("banana"), 20.0),
        (Symbol("cherry"), 30.0),
    ]
    for sym, weight in s_nodes:
        empty_symb_index.insert(sym, weight)

    # Test map
    mapped_names = empty_symb_index.map(lambda s: s.name.upper())
    assert mapped_names == ["APPLE", "BANANA", "CHERRY"]

    # Test filter
    filtered_symbs = empty_symb_index.filter(lambda s: "a" in s.name)
    assert filtered_symbs == [Symbol("apple"), Symbol("banana")]

def test_symb_index_ascii_representation(empty_symb_index):
    s_nodes = [
        (Symbol("root"), 50.0),
        (Symbol("left"), 25.0),
        (Symbol("right"), 75.0),
    ]
    for sym, weight in s_nodes:
        empty_symb_index.insert(sym, weight)

    expected_ascii = """  - right (W:75.00, H:1)
- root (W:50.00, H:2)
  - left (W:25.00, H:1)"""
    assert empty_symb_index.ascii() == expected_ascii
    assert empty_symb_index.to_ascii() == expected_ascii

def test_symb_index_rebalance_avl(empty_symb_index):
    s1 = Symbol("A")
    s2 = Symbol("B")
    s3 = Symbol("C")
    s4 = Symbol("D")

    empty_symb_index.insert(s1, 10.0)
    empty_symb_index.insert(s2, 20.0)
    empty_symb_index.insert(s3, 30.0)

    # Tree should be balanced after insertions, so rebalance should not change order
    empty_symb_index.rebalance(strategy='avl')
    inorder = empty_symb_index.traverse(order="in")
    assert inorder == [s1, s2, s3]

    # Test with a more complex rebalancing scenario
    tree = SymbolIndex(Symbol("rebalance_owner"))
    nodes = [
        (Symbol("N1"), 10),
        (Symbol("N2"), 20),
        (Symbol("N3"), 30),
        (Symbol("N4"), 40),
        (Symbol("N5"), 50),
        (Symbol("N6"), 60),
        (Symbol("N7"), 70),
    ]
    for sym, weight in nodes:
        tree.insert(sym, weight)

    tree.rebalance(strategy='avl')
    inorder = tree.traverse(order="in")
    assert inorder == [nodes[0][0], nodes[1][0], nodes[2][0], nodes[3][0], nodes[4][0], nodes[5][0], nodes[6][0]]

