MIN_RATING = 1
MAX_RATING = 5

SHOW_PER_PAGE = 25

RATING_CHOICES = [(i, i) for i in range(MIN_RATING, MAX_RATING + 1)]

LOGIN_URL = "core:login"
MAIN_PAGE = "books:books"

EXTERNAL_ID_ERROR = "External ID already exists. Please choose a different ID."
