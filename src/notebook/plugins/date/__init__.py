from datetime import datetime, timedelta
from notebook.pipeline import set_op


def yesterday(arg, args, pipeline):
    date = datetime.now() - timedelta(days=1)
    return args, pipeline.prepend(set_date=set_op(date=date))


hooks = {
    "--yesterday": yesterday,
    # "--date": date, # TODO: implement date parsing
}