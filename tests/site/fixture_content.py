"""Keep unit and browser fixtures independent of production research growth."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def copy_fixture_content(destination):
    shutil.copytree(ROOT / 'content', destination, ignore=shutil.ignore_patterns(
        'research-problem-*', 'research-to-reality.json', 'research-foundations.json',
        'scientific-ai.json', 'systems-to-physical-ai.json'))
