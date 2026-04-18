from __future__ import annotations

import heapq
from collections import Counter
from dataclasses import dataclass, field


@dataclass(order=True)
class HuffmanNode:
    weight: int
    char: str | None = field(compare=False, default=None)
    left: "HuffmanNode | None" = field(compare=False, default=None)
    right: "HuffmanNode | None" = field(compare=False, default=None)


class HuffmanCodec:
    def build_tree(self, text: str) -> HuffmanNode | None:
        if not text:
            return None
        queue = [HuffmanNode(weight, char=char) for char, weight in Counter(text).items()]
        heapq.heapify(queue)
        while len(queue) > 1:
            left = heapq.heappop(queue)
            right = heapq.heappop(queue)
            heapq.heappush(queue, HuffmanNode(left.weight + right.weight, left=left, right=right))
        return queue[0]

    def build_codes(self, root: HuffmanNode | None) -> dict[str, str]:
        if root is None:
            return {}
        codes: dict[str, str] = {}

        def dfs(node: HuffmanNode, prefix: str) -> None:
            if node.char is not None:
                codes[node.char] = prefix or "0"
                return
            dfs(node.left, prefix + "0")
            dfs(node.right, prefix + "1")

        dfs(root, "")
        return codes

    def encode(self, text: str) -> tuple[str, dict[str, str]]:
        tree = self.build_tree(text)
        codes = self.build_codes(tree)
        encoded = "".join(codes[ch] for ch in text)
        return encoded, codes

    def decode(self, encoded: str, codes: dict[str, str]) -> str:
        reverse = {value: key for key, value in codes.items()}
        cursor = ""
        output = []
        for bit in encoded:
            cursor += bit
            if cursor in reverse:
                output.append(reverse[cursor])
                cursor = ""
        return "".join(output)
