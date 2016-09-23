import unittest
from collections import deque
from ...config import Config
from ...sbb import SBB

TEST_CONFIG = {
    'task': 'classification',
    'classification_parameters': { 
        'dataset': 'iris',
        'working_path': "SBB/datasets/",
    },
    'training_parameters': {
        'runs_total': 1,
        'generations_total': 30,
        'validate_after_each_generation': 30,
        'populations': {
            'teams': 20,
            'points': 40,
        },
        'replacement_rate': {
            'teams': 0.5,
            'points': 0.2,
        },
        'mutation': {
            'team': {
                'remove_program': 0.7,
                'add_program': 0.8,
                'mutate_program': 0.2,
            },
            'program': {
                'remove_instruction': 0.7,
                'add_instruction': 0.8,
                'change_instruction': 0.8,
                'swap_instructions': 0.8,
                'change_action': 0.1,
            },
        },
        'team_size': {
            'min': 2,
            'max': 5,
        },
        'program_size': {
            'min': 2,
            'max': 20,
        },
    },

    'advanced_training_parameters': {
        'seed': 1,
        'use_pareto_for_point_population_selection': False,
        'use_operations': ['+', '-', '*', '/', 'if_lesser_than', 'if_equal_or_higher_than'],
        'extra_registers': 1,
        'diversity': {
            'use_and_show': [],
            'only_show': [],
            'k': 8,
        },
        "novelty": {
            "enabled": False,
            "dont_use_fitness": False,
        },
        'run_initialization_step2': False,
        'use_weighted_probability_selection': False,
        'use_agressive_mutations': False,
        'second_layer': {
            'enabled': False,
            'path': None,
        },
    },

    "debug": {
        "enabled": False,
        "output_path": "logs/",
    },
}

class ClassificationTests(unittest.TestCase):
    def setUp(self):
        Config.RESTRICTIONS['write_output_files'] = False
        Config.RESTRICTIONS['novelty_archive']['samples'] = deque(maxlen=int(TEST_CONFIG['training_parameters']['populations']['teams']*1.0))
        
        config = dict(TEST_CONFIG)
        config['advanced_training_parameters']['use_pareto_for_point_population_selection'] = False
        config['advanced_training_parameters']['diversity']['use_and_show'] = []
        config['advanced_training_parameters']['diversity']['only_show'] = []
        config['classification_parameters']['dataset'] = 'iris'
        config['training_parameters']['runs_total'] = 1
        config['advanced_training_parameters']['run_initialization_step2'] = False
        Config.USER = config

    def test_classification_for_iris(self):
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_classification_for_iris_for_three_runs(self):
        Config.USER['training_parameters']['runs_total'] = 3
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 3
        self.assertEqual(expected, result)

    def test_classification_for_iris_with_pareto(self):
        Config.USER['advanced_training_parameters']['use_pareto_for_point_population_selection'] = True
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_classification_for_iris_with_step2(self):
        Config.USER['advanced_training_parameters']['run_initialization_step2'] = True
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_classification_for_iris_with_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['genotype', 'fitness_sharing']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_classification_for_thyroid(self):
        Config.USER['classification_parameters']['dataset'] = 'thyroid'
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()