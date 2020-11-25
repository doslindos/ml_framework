from .. import Path, jsonload
from ..util.data_fetching import load_with_tfds_load, mysqldb_fetch, spotify_api_fetch
from ..util.preprocessing import normalize_image, preprocess_spotify_features, preprocess_billboard
from random import sample as rndsample

from third_party.sklearn.sklearn_functions import split_dataset, label_encoding as sk_label_encoding, one_hot_encoding as sk_one_hot
from tensorflow import data as tfdata
