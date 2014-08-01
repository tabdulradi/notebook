from __future__ import with_statement
from __builtin__ import next
import os
import os.path
from datetime import datetime
from hooks import hooks
from pipeline import Pipeline, set_op


base_path_candidates = [
    os.path.expanduser("~/Documents/notebook"),
    os.path.expanduser("~/documents/notebook"),
    os.path.expanduser("~/Documents/"),
    os.path.expanduser("~/documents/"),
    os.getcwd()
]

base_path = next(p for p in base_path_candidates if os.path.exists(p))


def store(d):
    fn = "%s.%s" % (os.path.join(base_path, d['title']), d.get('format', 'txt'))
    with open(fn, 'a') as f:
        f.write(d['body'])
        f.write('\n')

    # Set modified timestamp
    timestamp = d.get('date')
    if timestamp:
        timestamp = (timestamp - datetime(1970, 1, 1)).total_seconds()
        timestamp = (timestamp, timestamp)

    os.utime(fn, timestamp)

    print "Note stored to %s" % fn
    return d


def set_title(data):
    title = data["body"][:10]  # TODO: this should be smarter!
    return dict(data, title=title)


default_pipeline = Pipeline([  # TODO: plugins should be able to contribute into the default pipeline
    ("set_title", set_title),
    ("store", store)
])


def default_op(arg, args, pl):
    return [], pl.prepend(set_body=set_op(body=" ".join([arg] + args)))


def main(args):
    pl = default_pipeline
    while args:
        key = args.pop(0)
        args, pl = hooks.get(key, default_op)(key, args, pl)

    data = {}
    for op in pl:
        data = op(data)
