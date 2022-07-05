from __future__ import annotations

import json
import cv2
import yaml

from PolygonGame1.TensorboardLogger1 import TensorboardLogger1
from MonteScene.MonteCarloTreeSearch import MonteCarloSceneSearch
from MonteScene.utils import convert_dict2namespace

from .PolygonGame1 import PolygonGame1


def main():
        #directories
        input_path = "input/"
        output_path = "PolygonGame1/output/"
        settings_path = "PolygonGame1/settings.yaml"

        #load data
        with open(f'{input_path}truth.json', "r") as t:
                truth_json = json.load(t)
        with open(f'{input_path}proposals.json', "r") as p:
                proposals_json = json.load(p)

        image: cv2.Mat = cv2.imread(f'{input_path}image.jpg')

        with open(settings_path, 'r') as f:
                settings = yaml.safe_load(f)
        settings = convert_dict2namespace(settings)


        #mcss
        environment = PolygonGame1(truth_json, proposals_json, image)
        logger = TensorboardLogger1(environment, output_path)
        mcss = MonteCarloSceneSearch(environment, mcts_logger=logger, settings=settings)

        mcss.run()


if __name__ == '__main__':
        main()