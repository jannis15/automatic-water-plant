from gpio_handler import GPIOHandler
import db_models
from db_session import engine

db_models.Base.metadata.create_all(bind=engine)
handler = GPIOHandler()
handler.do_routine()
del handler