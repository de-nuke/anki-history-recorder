from types import SimpleNamespace

from anki.consts import MODEL_CLOZE, MODEL_STD

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
    'note_type',
    'model_type',
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


CARD_TYPES = SimpleNamespace(NEW="new", LEARNING="learning", DUE="due")


TYPE_MAP = {
    0: CARD_TYPES.NEW,
    1: CARD_TYPES.LEARNING,
    2: CARD_TYPES.DUE,
}

QUEUE_MAP = {
    0: CARD_TYPES.NEW,
    1: CARD_TYPES.LEARNING,
    2: CARD_TYPES.DUE,
}


MODEL_TYPES_MAP = {
    MODEL_CLOZE: "CLOZE",
    MODEL_STD: "STANDARD"
}
