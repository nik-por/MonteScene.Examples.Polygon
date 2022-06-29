from __future__ import annotations
from typing import List

import cv2
import numpy as np

from operator import contains
from cv2 import Mat
from MonteScene.Proposal.Prop import Proposal
from shapely.geometry import Polygon

from MonteScene.constants import NodesTypes

class LabeledPolygonProposal(Proposal):
	new_id = 1
	def __init__(self, polygon: Polygon, label: str):
		super().__init__(str(LabeledPolygonProposal.new_id))
		LabeledPolygonProposal.new_id += 1
		self.polygon = polygon
		self.label = label
	
	def area_of_intersection_with(self, other: LabeledPolygonProposal):
		return self.polygon.intersection(other.polygon).area

	def area_of_union_with(self, other: LabeledPolygonProposal):
		return self.polygon.union(other.polygon).area
	
	def iou(self, other: LabeledPolygonProposal):
		return self.area_of_intersection_with(other) / self.area_of_union_with(other)

	def is_incompatible_with(self, other: LabeledPolygonProposal) -> bool:
		return self.area_of_intersection_with(other) > 0;

	def add_incompatibility(self, incompatible: LabeledPolygonProposal):
		if contains(self.incompatible_proposals_set, incompatible): return
		self.incompatible_proposals_set.append(incompatible)
	
	def draw_to(self, matrix: Mat, color: List[int], fill: bool = True):
		if fill:
			cv2.fillPoly(matrix, [np.array([[int(x), int(y)] for (x, y) in self.polygon.exterior.coords])], color)
		else:
			cv2.polylines(matrix, [np.array([[int(x), int(y)] for (x, y) in self.polygon.exterior.coords])], True, color)
	
	@staticmethod
	def from_json(json) -> LabeledPolygonProposal:
		return LabeledPolygonProposal(Polygon(json["points"]), json["label"])
	
	def to_json(self):
		return {
			"label": self.label,
			"line_color": None,
			"fill_color": None,
			"points": [[x, y] for x, y in self.polygon.exterior.coords],
			"shape_type": "polygon",
			"flags": {}
		}