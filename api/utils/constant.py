import os


COMPUTE_SINGLE_AMOUNT = "single"
COMPUTE_ALL_AMOUNT = "all"
INCOMES = 2
EXPENSE = 1

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
