import structlog


def logit(method):
    """ log input/output of methods"""

    def logged(*args, **kw):
        func_name = method.__name__
        structlog.get_logger().info(f'{func_name} start')
        structlog.get_logger().debug(f'with args {args}')
        result = method(*args, **kw)
        structlog.get_logger().info(f'{func_name} end')
        structlog.get_logger().debug(f'with result {result}')
        return result

    return logged
