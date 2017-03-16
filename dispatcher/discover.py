import os


def discover_receivers(path, base_path):
    path = os.path.abspath(path)
    base_path = os.path.abspath(base_path)
    receiver_paths = discover_receiver_paths(path, base_path)
    for p in receiver_paths:
        module_path = p[len(base_path):].replace('/', '.')
        module = os.path.splitext(module_path)[0].strip('.')
        __import__(module, globals(), locals(), [], -1)


def discover_receiver_paths(path, base_path):
    if not path.startswith(base_path):
        raise Exception('path must startswith base_path')

    receiver_paths = set()
    for dirpath, dirnames, filenames in os.walk(path, followlinks=True):
        for filename in filenames:
            if not filename.endswith('receiver.py'):
                continue

            path = os.path.join(dirpath, filename)
            if not is_receiver_file(path):
                continue

            receiver_paths.add(path)
    return receiver_paths


def is_receiver_file(path):
    return True
