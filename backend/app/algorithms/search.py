from __future__ import annotations

from collections import defaultdict


class HashIndex:
    def __init__(self) -> None:
        self._data: dict[str, dict] = {}

    def build(self, items: list[dict], key_field: str) -> None:
        self._data = {str(item[key_field]).lower(): item for item in items}

    def get(self, key: str) -> dict | None:
        return self._data.get(key.lower())


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.item_ids: set[str] = set()
        self.is_end = False


class TrieIndex:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str, item_id: str) -> None:
        node = self.root
        for ch in word.lower():
            node = node.children.setdefault(ch, TrieNode())
            node.item_ids.add(item_id)
        node.is_end = True

    def prefix_search(self, prefix: str) -> set[str]:
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return set()
            node = node.children[ch]
        return node.item_ids.copy()


class InvertedIndex:
    def __init__(self) -> None:
        self._index: dict[str, set[str]] = defaultdict(set)

    def build(self, items: list[dict], fields: list[str], id_field: str) -> None:
        for item in items:
            item_id = str(item[id_field])
            for field in fields:
                for token in self.tokenize(str(item.get(field, ""))):
                    self._index[token].add(item_id)

    def search(self, keywords: list[str]) -> set[str]:
        if not keywords:
            return set()
        tokens = [token for keyword in keywords for token in self.tokenize(keyword)]
        if not tokens:
            return set()
        result = self._index.get(tokens[0], set()).copy()
        for token in tokens[1:]:
            result &= self._index.get(token, set())
        return result

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return [token for token in text.lower().replace(",", " ").replace("，", " ").split() if token]
