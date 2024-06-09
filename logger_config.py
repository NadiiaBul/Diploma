import logging
import logging.handlers
import queue

log_queue = queue.Queue()
queue_handler = logging.handlers.QueueHandler(log_queue)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('example.log', mode='w')
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(queue_handler)

logging.getLogger('matplotlib').setLevel(logging.WARNING)

queue_listener = logging.handlers.QueueListener(log_queue, file_handler)
queue_listener.start()
