from celery import shared_task
from .services.defillama_request_service import defillama_request_service
import logging
from . import config

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def update_cryptocurrency_prices(self):
    response = defillama_request_service.get_cryptocurrency_prices_from_defillama(
        config.TOKEN_ADDRESS_LIST, 90
    )
    # TODO: insert some retry logic here for failed requests.
    # TODO: insert response into DB
    return
