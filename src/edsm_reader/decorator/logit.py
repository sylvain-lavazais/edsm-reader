import structlog


def logit(method):
    """ log input/output of methods"""

    def logged(*args, **kw):
        func_name = method.__name__
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kw.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        structlog.get_logger().debug(f'{func_name} start')
        structlog.get_logger().debug(f'with args {signature}')
        result = method(*args, **kw)
        structlog.get_logger().debug(f'{func_name} end')
        structlog.get_logger().debug(f'with result {result}')
        return result

    return logged
