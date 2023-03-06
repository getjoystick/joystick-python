import typing as t


class ParamsDict(t.Dict[str, t.Any]):
    def __init__(self, *args: t.Dict[str, t.Any], **kwargs: t.Any) -> None:
        if args:
            if len(args) > 1:
                raise TypeError(
                    "update expected at most 1 arguments, " "got %d" % len(args)
                )
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def __setitem__(self, key: str, value: t.Any) -> None:
        super(ParamsDict, self).__setitem__(key, value)
