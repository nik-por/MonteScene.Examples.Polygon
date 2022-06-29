from __future__ import annotations

import json
import numpy as np

from MonteScene.MonteCarloTreeSearch.MCTSLogger import MCTSLogger
from MonteScene.Tree.Tree import Tree
import tensorflow as tf
import tensorboard as tb

from .PolygonGame1 import PolygonGame1

class TensorboardLogger1(MCTSLogger):
	def __init__(self, environment: PolygonGame1, export_directory: str):
		super().__init__(environment)
		self.environment: PolygonGame1 = environment

		self.export_directory = export_directory
		self.writer = tf.summary.create_file_writer(export_directory)
		self.writer.set_as_default()

		tb.summary.image("target arrangement", data = np.expand_dims(self.environment.render(self.environment.truth.elements), axis=0), step=0)

	def reset_logger(self):
		pass

	def export_solution(self, best_props_list):
		pass

	def log_final(self, mc_tree: Tree):
		self.writer.flush()

	def log_mcts(self, iter, last_score, last_tree_depth, mc_tree: Tree, is_end=False):

		selection, end_node = mc_tree.get_best_path()
		render = self.environment.render(selection)

		tb.summary.scalar("score", data = last_score, step=iter)
		tb.summary.image("render", data = np.expand_dims(render, axis=0), step=iter)

		self.writer.flush()