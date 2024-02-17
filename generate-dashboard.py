"""Helpers to fresh stale GitHub secrets."""
import os
from base64 import b64encode
from pathlib import Path
from typing import Any, Dict
import json
import requests

from requests import Response
import fitbit as fb
import csv
from utilities.gh import (get_repo_key, encrypt, write_secret)

from settings import (github_user,
                      github_repo,
                      github_token,
                      secret_name,
                      api_endpoint,
                      CLIENT_ID,
                      CLIENT_SECRET,
                      FITBIT_TOKEN,
                      fitbit_period)


