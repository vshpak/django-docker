from logging import getLogger


logger = getLogger(__name__)


class StatisticClient:
    def increment_access_counter(self, model_name, object_id):
        # todo: network access
        logger.info('Performing an internet call...')
        raise NotImplementedError()


def increment_access_counter(model_name, object_id):
    return True
