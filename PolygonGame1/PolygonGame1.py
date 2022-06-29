from __future__ import annotations

import json

from typing import Dict, List
from cv2 import Mat
from ordered_set import OrderedSet

from MonteScene.ProposalGame.ProposalGame import ProposalGame
from Proposals.LabeledPolygonProposal import LabeledPolygonProposal
from Proposals.LabeledPolygonPool import LabeledPolygonPool
from PolygonGame1.ScipyPolygonMatcher import ScipyPolygonMatcher


class PolygonGame1(ProposalGame):
	def __init__(self, truth_json: Dict[str, List[int]], proposals_json: Dict[str, List[int]], image: Mat):
		"""
        :param truth_json: The ground truth.
        :param proposals_json: A json object, representing the proposals for this game.
        :param image: The original image.
		"""
		super().__init__([truth_json, proposals_json, image])

	def initialize_game(self, truth_json: Dict[str, List[int]], proposals_json: Dict[str, List[int]], image: Mat):
		"""
		Initializes the polygon game. This method is called by the constructor.

		The proposal polygons provided in the arguments are inserted into a LabeledPolygonPool,
		which takes care of identifying incompatibilities between the proposal.
		"""
		self.pool_json = proposals_json
		self.truth = LabeledPolygonPool.from_json(truth_json)
		self.proposals = LabeledPolygonPool.from_json(self.pool_json)
		self.image = image

	def generate_proposals(self):
		return OrderedSet(self.proposals.elements)

	def render(self, prop_seq) -> Mat:
		selection = LabeledPolygonPool()
		selection.insert_all(prop_seq.copy())
		
		render = self.image.copy()
		render[:] = 0
		selection.draw_to(render)
		return render

	def calc_score_from_proposals(self, prop_seq=None, props_optimizer=None):
		"""
		Calculates a score for the selected subset of proposals (prop_seq).
		
		For this the score for the best matching found by the ScipyPolygonMatcher is used.

		It calculates this score by first computing a cost matrix depending on IOU between all polygons
		and then using scipy to obtain an optimal matching.
		"""
		if(prop_seq == None):
			prop_seq = self.prop_seq

		matcher = ScipyPolygonMatcher(self.truth.elements, prop_seq)
		return matcher.get_best_score() / len(self.truth.elements)
	
	def export_result_json(self, results: List[LabeledPolygonProposal]):
		pool = LabeledPolygonPool()
		pool.insert_all(results)

		result = self.pool_json
		result["shapes"] = pool.to_json()

		return result
	
	def calc_loss_from_proposals(self, prop_seq=None):
		return super().calc_loss_from_proposals(prop_seq)

	def convert_loss_to_score(self, loss):
		return super().convert_loss_to_score(loss)