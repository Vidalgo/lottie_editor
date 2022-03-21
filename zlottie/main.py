from zlottie.objects import Animation
from pathlib import Path
import json

_lotties_path = Path(__file__).parent / 'data/lotties'

if __name__ == '__main__':
    with open(r'C:\dev\vidalgo\code\lottie_editor\zlottie\tests\data\lotties\68965-pepperoni-pizza.json') as f:
        raw = json.load(f)