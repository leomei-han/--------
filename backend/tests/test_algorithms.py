from app.algorithms.compression import HuffmanCodec
from app.algorithms.graph import Graph
from app.algorithms.search import HashIndex, InvertedIndex, TrieIndex
from app.algorithms.topk import TopKSelector, quickselect_top_k


def test_topk_selector_works():
    items = [{"name": "a", "score": 1}, {"name": "b", "score": 3}, {"name": "c", "score": 2}]
    selector = TopKSelector(lambda item: item["score"])
    result = selector.select(items, 2)
    assert [item["name"] for item in result] == ["b", "c"]


def test_quickselect_top_k_works():
    items = [{"name": "a", "score": 1}, {"name": "b", "score": 3}, {"name": "c", "score": 2}]
    result = quickselect_top_k(items, 2, lambda item: item["score"])
    assert [item["name"] for item in result] == ["b", "c"]


def test_hash_trie_inverted_search():
    items = [
        {"source_id": "1", "name": "北京邮电大学", "description": "海淀 校园"},
        {"source_id": "2", "name": "北京动物园", "description": "景区 熊猫"},
    ]
    hash_index = HashIndex()
    hash_index.build(items, "name")
    assert hash_index.get("北京邮电大学")["source_id"] == "1"

    trie = TrieIndex()
    trie.insert("北京邮电大学", "1")
    assert "1" in trie.prefix_search("北京")

    inverted = InvertedIndex()
    inverted.build(items, ["name", "description"], "source_id")
    assert "2" in inverted.search(["熊猫"])


def test_graph_shortest_path():
    graph = Graph()
    graph.add_node("A", 0.0, 0.0)
    graph.add_node("B", 1.0, 1.0)
    graph.add_node("C", 2.0, 2.0)
    graph.add_edge("A", "B", 10, 1.0, {"walk": 1.0}, {"walk"})
    graph.add_edge("B", "C", 5, 1.0, {"walk": 1.0}, {"walk"})
    path, cost = graph.shortest_path("A", "C")
    assert path == ["A", "B", "C"]
    assert cost == 15


def test_huffman_codec_roundtrip():
    codec = HuffmanCodec()
    encoded, codes = codec.encode("travel diary")
    decoded = codec.decode(encoded, codes)
    assert decoded == "travel diary"
