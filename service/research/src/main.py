import logging
from datetime import datetime
from pathlib import Path

import settings
from core.datagenerate import model_generator
from db.baseinterface import DbInterface
from schemas.dbschema import db_list

logfile = Path(__file__).parents[0].joinpath('results.txt')


def main():

    with open(logfile, 'w'):
        pass
    logging.basicConfig(
        filename=logfile,
        format='%(asctime)s - %(message)s',
        level=logging.INFO,
        encoding='utf-8',
    )
    logging.info('------------------<( начало )')

    def timecheck(dt: datetime) -> None:
        difference = datetime.now() - dt
        logging.info(f'Потрачено времени (сек): {difference.total_seconds()}')

    for interface_item in db_list:

        dataforread = []

        mm: DbInterface = interface_item()
        dt = datetime.now()
        logging.info(f'--- запись в {mm.INTERFACE_NAME}:')
        modelgenerator = model_generator()
        for model_class, model_data in modelgenerator:
            dataforread.append(mm.write(model_class, model_data))
        timecheck(dt)

        dt = datetime.now()
        logging.info(f'--- чтение {mm.INTERFACE_NAME}:')
        for dataitem in dataforread:
            mm.read(dataitem)
        timecheck(dt)

    logging.info('------------------<( конец )')


if __name__ == '__main__':

    logfile = Path(__file__).parents[1].joinpath('results.txt')
    settings.program_settings.mongo_host = '127.0.0.1'
    settings.program_settings.postgres_host = '127.0.0.1'
    settings.program_settings.postgres_port = settings.program_settings.postgres_local_port
    settings.program_settings.mongo_port = settings.program_settings.mongo_local_port
    main()
