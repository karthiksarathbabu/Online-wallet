from threading import Thread
from uuid import uuid4
from wallet.models import Transactions, Wallet


def postpone(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.start()
    return decorator


def reference_id_gernerator():

    sample = uuid4()
    print("sample______",sample)
    while Transactions.objects.filter(reference_id=sample).exists():
        sample = reference_id_gernerator()
    return sample

