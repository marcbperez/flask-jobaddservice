from flask import Blueprint


crawler = Blueprint('crawler', __name__)
"""Crawler blueprint."""

from . import stackoverflow  # nopep8
from . import github  # nopep8
from . import diceuk  # nopep8
