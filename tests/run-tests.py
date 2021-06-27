#!/usr/bin/env python3


from pathlib import Path
from unittest import TestLoader, TextTestRunner


BASE_DIR = Path(__file__).resolve().parent

loader = TestLoader().discover(BASE_DIR)

test_data = TextTestRunner().run(loader)

if not test_data.wasSuccessful():
    exit(44)
