from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from Proposals.LabeledPolygonProposal import LabeledPolygonProposal


class BipartiteMatcher(ABC):
	def __init__(self, left: List[LabeledPolygonProposal], right: List[LabeledPolygonProposal]) -> None:
		assert left is not None
		assert right is not None

		self.left = left
		self.right = right

	@abstractmethod
	def get_best_matching(self) -> List[Tuple[Tuple[int, int], float]]:
		raise NotImplementedError()

	def get_best_score(self) -> float:

		matching = self.get_best_matching()
		if matching is None: return 0;

		return sum([cost for _, cost in matching])

	def one_side_is_empty(self) -> bool:
		if len(self.left) <= 0: return True
		if len(self.right) <= 0: return True
		return False