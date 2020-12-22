# Decorator that may call as with params(log_level, log_result) or without any params
#
#@log_function
#def func_to_decorate():
#    pass
#
#@log_function(log_result=True)
#def func_to_decorate():
#    pass
#

def log_function(original_func=None, log_level=logging.DEBUG, log_result=False):

    def decorator(func):
        logger = get_logger()
        display_name = func.__name__

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            logger.log(log_level, f'Function "{display_name}" started with,\nargs: {args}\nkwargs: {kwargs}')

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'Function "{display_name}" threw exception:\n{e}')
                raise e

            if log_result and result:
                format_result = repr(result)
                logger.log(log_level, f'Function "{display_name}" resulted with type {type(result)},\n{format_result}')

            return result
        return _wrapper

    if original_func:
        return decorator(original_func)
    return decorator
