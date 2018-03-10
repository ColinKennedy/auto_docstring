from . import environment
from .styles import google

environment.register_code_style(
    name='google',
    obj=google.GoogleStyle,
)
