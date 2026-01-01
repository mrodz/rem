import logging

FORMAT = "[%(name)s] %(levelname)s - %(message)s"
FORMATTER = logging.Formatter(FORMAT)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(FORMATTER)

def application_logger(name: str):
    l = logging.getLogger(name)
    l.propagate = False
    l.addHandler(console_handler)
    return l
