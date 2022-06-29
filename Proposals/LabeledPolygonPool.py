from __future__ import annotations
from operator import contains

import cv2
import random

from multiprocessing import pool
from typing import Dict, List

from cv2 import Mat
from Proposals.LabeledPolygonProposal import LabeledPolygonProposal

class LabeledPolygonPool:
	def __init__(self) -> None:
		self.elements : List[LabeledPolygonProposal] = []
	
	def insert(self, polygon: LabeledPolygonProposal) -> None:
		for p in self.elements:
			if polygon.is_incompatible_with(p):
				p.add_incompatibility(polygon)
				polygon.add_incompatibility(p)

		self.elements.append(polygon)
	
	def insert_all(self, polygons: List[LabeledPolygonProposal]):
		for p in polygons:
			self.insert(p)
	
	def to_json(self):
		return [poly.to_json() for poly in self.elements]
	
	def draw_to(self, matrix: Mat, label_to_color_map: Dict[str, List[int]] = None, fill: bool = True) -> Dict[str, List[int]]:
		if label_to_color_map is None:
			label_to_color_map = {None: [0, 0, 0]} # exclude 0 (usually background)

		for poly in self.elements:
			color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
			while contains(label_to_color_map.values(), color):
				color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

			if contains(label_to_color_map, poly.label):
				color = label_to_color_map[poly.label]
			else:
				label_to_color_map[poly.label] = color

			poly.draw_to(matrix, color, fill)
		
		return label_to_color_map

	@staticmethod
	def from_json(json) -> LabeledPolygonPool:
		polygon_pool = LabeledPolygonPool()
		for shape_json in json["shapes"]:
			polygon_pool.insert(LabeledPolygonProposal.from_json(shape_json))
		return polygon_pool