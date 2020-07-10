import os
from types import SimpleNamespace

from anki.consts import MODEL_CLOZE, MODEL_STD, CARD_TYPE_NEW, CARD_TYPE_LRN, \
    CARD_TYPE_RELEARNING, CARD_TYPE_REV, QUEUE_TYPE_PREVIEW, \
    QUEUE_TYPE_SIBLING_BURIED, QUEUE_TYPE_MANUALLY_BURIED, \
    QUEUE_TYPE_SUSPENDED, QUEUE_TYPE_LRN, QUEUE_TYPE_NEW, QUEUE_TYPE_REV, \
    QUEUE_TYPE_DAY_LEARN_RELEARN

AUDIO_FORMATS = {
    "3gp", "aa", "aac", "aax", "act", "aiff", "alac", "amr", "ape", "au",
    "awb", "dct", "dss", "dvf", "flac", "gsm", "iklax", "ivs", "m4a", "m4b",
    "m4p", "mmf", "mp3", "mpc", "msv", "nmf", "nsf", "ogg", "oga", "mogg",
    "opus", "ra", "rm", "raw", "rf64", "sln", "tta", "voc", "vox", "wav",
    "wma", "wv", "webm", "8svx", "cda"
}

VIDEO_FORMATS = {
    "webm", "mkv", "flv", "flv", "vob", "ogv, ogg", "drc", "gif", "gifv",
    "mng", "avi", "MTS, M2TS, TS", "mov, qt", "wmv", "yuv", "rm", "rmvb",
    "asf", "amv", "mp4, m4p (with DRM), m4v", "mpg", "mp2", "mpeg", "mpe",
    "mpv", "mpg, mpeg, m2v", "m4v", "svi", "3gp", "3g2", "mxf", "roq", "nsv",
    "flv", "f4v", "f4p", "f4a", "f4b"
}

HEADERS = [
    'uid',
    'sid',
    'timestamp',
    'card_id',
    'deck_id',
    'deck_name',
    'question',
    'answer',
    'question_fields',
    'answer_fields',
    'note_type',
    'model_type',
    'question_has_cloze',
    'question_has_type_in',
    'question_has_type_in_cloze',
    'question_has_sound',
    'answer_has_sound',
    'question_has_video',
    'answer_has_video',
    'question_has_image',
    'answer_has_image',
    'ease',
    'type',
    'new_type',
    'queue',
    'new_queue',
    'due',
    'reps',
    'last_interval',
    'answered_at',
    'time_taken',
    'grade_time',
    'total_study_time',
    'ESTIMATED_INTERVAL'
]


TYPE_MAP = {
    CARD_TYPE_NEW: "new",
    CARD_TYPE_LRN: "learning",
    CARD_TYPE_REV: "review",
    CARD_TYPE_RELEARNING: "relearning"
}

QUEUE_MAP = {
    QUEUE_TYPE_MANUALLY_BURIED: "manually_burried",
    QUEUE_TYPE_SIBLING_BURIED: "sibling_buried",
    QUEUE_TYPE_SUSPENDED: "suspended",
    QUEUE_TYPE_NEW: "new",
    QUEUE_TYPE_LRN: "learning",
    QUEUE_TYPE_REV: "review",
    QUEUE_TYPE_DAY_LEARN_RELEARN: "day_learn_relearn",
    QUEUE_TYPE_PREVIEW: "preview",
}


MODEL_TYPES_MAP = {
    MODEL_CLOZE: "CLOZE",
    MODEL_STD: "STANDARD"
}

UPLOAD_HOST = 'history-recorder-storage-app.herokuapp.com'
UPLOAD_PATH = '/form-upload'
FIELD_NAME = 'file'
BASE_DIR = os.path.dirname(__file__)
USER_FILES_DIR = os.path.join(BASE_DIR, 'user_files')