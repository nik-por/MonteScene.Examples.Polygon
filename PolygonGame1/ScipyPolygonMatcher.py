from __future__ import annotations

from enum import Enum
from scipy import optimize
from typing import List, Tuple

from Matching.BipartiteMatcher import BipartiteMatcher
from Proposals.LabeledPolygonProposal import LabeledPolygonProposal


class OptimizationGoal(Enum):
	MAX = -1
	MIN = 1
class ScipyPolygonMatcher(BipartiteMatcher):
	def __init__(self, left: List[LabeledPolygonProposal], right: List[LabeledPolygonProposal], goal: OptimizationGoal = OptimizationGoal.MAX) -> None:
		super().__init__(left, right)
		self.goal = goal

	def get_best_matching(self) -> List[Tuple[Tuple[int, int], float]]:

		cost_matrix = self.get_cost_matrix()
		if cost_matrix is None: return None;

		left_indices, right_indices = optimize.linear_sum_assignment(cost_matrix)

		matches = list(zip(left_indices, right_indices))
		costs = [self.sign_adjustment() * cost_matrix[l][r] for l, r in matches]
		return list(zip(matches, costs))
	
	def get_cost_matrix(self):
		if self.one_side_is_empty(): return None;

		return [[self.sign_adjustment() * l.iou(r) for r in self.right] for l in self.left]
	
	def sign_adjustment(self):
		return self.goal.value