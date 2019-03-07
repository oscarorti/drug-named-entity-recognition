from pathlib import Path

PROJECT_PATH = Path(__file__).parent

DRUGBANK_TRAIN = str(PROJECT_PATH.joinpath('data/Train/DrugBank'))
MEDLINE_TRAIN = str(PROJECT_PATH.joinpath('data/Train/MedLine'))
DRUGBANK_TEST = str(PROJECT_PATH.joinpath('data/Test-NER/DrugBank'))
MEDLINE_TEST = str(PROJECT_PATH.joinpath('data/Test-NER/MedLine'))
