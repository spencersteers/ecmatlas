from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import json
import requests
import datetime
import re

from experiments.models import Experiment, Dataset, DatasetItem, RelativeConcentration
from atlas.models import Tissue, Family, FunctionalGroup, Protein, ProteinExternalReference

from dataloader.tasks import parse_dataset

def process_dataset(dataset_id):
    parse_dataset.delay(dataset_id)
