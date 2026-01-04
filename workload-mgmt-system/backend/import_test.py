import importlib, traceback

try:
    m = importlib.import_module('app.schemas.task')
    print('Imported app.schemas.task OK')
    print('Attributes:', [n for n in dir(m) if not n.startswith('_')])
except Exception:
    traceback.print_exc()
