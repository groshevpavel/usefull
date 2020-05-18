import functools
import logging
import time

from account_search.app.config import config

logger = logging.getLogger(config.APP_NAME)


def run_time_log(warning_limit_secs=30):
    def decorator(f):
        @functools.wraps(f)
        async def async_wrapper(*args, **kwargs):
            started_at = time.monotonic()
            result = await f(*args, **kwargs)
            process_time = time.monotonic() - started_at

            log_msg = f'{f.__name__}: process time: {process_time:.2f} secs'
            if process_time >= warning_limit_secs:
                kwargs = {k: v if not isinstance(v, (list, tuple, set, dict,)) else 'ЧТО-ТО БОЛЬШОЕ!' for k, v in kwargs.items()}
                log_msg += f'\nARGS:\n{args}' if args else ''
                log_msg += f'\nKWARGS:\n{kwargs}' if kwargs else ''
                logger.warning(log_msg)
            else:
                logger.info(log_msg)

            return result
        return async_wrapper
    return decorator

