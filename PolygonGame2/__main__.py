from __future__ import annotations

import json
import cv2
import yaml

from Proposals.LabeledPolygonPool import LabeledPolygonPool
from PolygonGame2.TensorboardLogger2 import TensorboardLogger2
from MonteScene.MonteCarloTreeSearch import MonteCarloSceneSearch
from MonteScene.utils import convert_dict2namespace

from PolygonGame2.PolygonGame2 import PolygonGame2


def main():
        #directories
        input_path = "input/"
        output_path = "PolygonGame2/output/"
        settings_path = "PolygonGame1/settings.yaml"

        #load data
        with open(f'{input_path}truth.json', "r") as t:
                truth_json = json.load(t)
        with open(f'{input_path}proposals.json', "r") as p:
                proposals_json = json.load(p)

        image: cv2.Mat = cv2.imread(f'{input_path}image.jpg')
        segmentation = image
        segmentation[:] = 0
        label_to_color_map = LabeledPolygonPool.from_json(truth_json).draw_to(segmentation, { None : [0, 0, 0] }) #generate semantic segmentation

        with open(settings_path, 'r') as f:
                settings = yaml.safe_load(f)
        settings = convert_dict2namespace(settings)


        #mcss
        environment = PolygonGame2(segmentation, label_to_color_map, proposals_json)
        logger = TensorboardLogger2(environment, output_path)
        mcss = MonteCarloSceneSearch(environment, mcts_logger=logger, settings=settings)

        mcss.run()


if __name__ == '__main__':
        main()