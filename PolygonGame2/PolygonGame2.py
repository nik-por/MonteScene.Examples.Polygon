from __future__ import annotations

from typing import Dict, List
from cv2 import Mat
from ordered_set import OrderedSet

from MonteScene.ProposalGame.ProposalGame import ProposalGame
from Proposals.LabeledPolygonProposal import LabeledPolygonProposal
from Proposals.LabeledPolygonPool import LabeledPolygonPool


class PolygonGame2(ProposalGame):
	def __init__(self, segmentation: Mat, label_to_segment_color_map: Dict[str, List[int]], proposals_json: Dict[str, object]):
		"""
        :param segmentation: The segmentation of an image.
        :param label_to_segment_color_map: A dictionary that maps each proposal label to the corresponding color in the segmentation.
        :param proposals_json: A json object, representing the proposals for this game.
		"""
		super().__init__([segmentation, label_to_segment_color_map, proposals_json])

	def initialize_game(self, segmentation: Mat, label_to_segment_color_map: Dict[str, List[int]], proposals_json: Dict[str, object]):
		"""
		Initializes the polygon game. This method is called by the constructor.

		The proposal polygons provided in the arguments are inserted into a LabeledPolygonPool,
		which takes care of identifying incompatibilities between the proposal.
		"""

		self.proposals_json = proposals_json
		self.proposals = LabeledPolygonPool.from_json(self.proposals_json)
		self.label_to_segment_color_map = label_to_segment_color_map
		self.segment_color_to_label_map = {(v[0], v[1], v[2]): k for k, v in self.label_to_segment_color_map.items()} #invert for efficiency
		self.segmentation = segmentation

	def generate_proposals(self):
		return OrderedSet(self.proposals.elements)
	
	def render(self, prop_seq) -> Mat:
		selection = LabeledPolygonPool()
		selection.insert_all(prop_seq.copy())
		
		render = self.segmentation.copy()
		render[:] = 0
		selection.draw_to(render, self.label_to_segment_color_map)
		return render


	def calc_score_from_proposals(self, prop_seq=None, props_optimizer=None):
		"""
		Calculates a score for the selected subset of proposals (prop_seq).
		
		This is done by first rendering an image from the selected proposals, that corresponds
		to the image segmentation that would result form this selection.

		A score is then obtained by comparing the rendered image to the segmentation image,
		this game is trying to match with its proposal selection.

		The measure employed is simply the percentage of equal pixels.
		"""

		if(prop_seq == None):
			prop_seq = self.prop_seq

		render = self.render(prop_seq)

		background = self.segmentation.copy()
		background[:] = (0, 0, 0)


		equalities: Mat = (render == self.segmentation) & (render != background)
		return equalities.sum() / (self.segmentation.shape[0] * self.segmentation.shape[1])
	
	@staticmethod
	def same(a: List, b: List):
		if len(a) != len(b): return False
		for (aa, bb) in zip(a, b):
			if aa != bb: return False
		return True

	def export_result_json(self, results: List[LabeledPolygonProposal]):
		pool = LabeledPolygonPool()
		pool.insert_all(results)

		result = self.proposals_json
		result["shapes"] = pool.to_json()

		return result
	
	def calc_loss_from_proposals(self, prop_seq=None):
		return super().calc_loss_from_proposals(prop_seq)

	def convert_loss_to_score(self, loss):
		return super().convert_loss_to_score(loss)