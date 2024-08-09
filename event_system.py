# ./event_system.py

import logging

class EventSystem:
    def __init__(self):
        self.listeners = {}
        logging.info("> Event system initialized")

    def on(self, event_name, listener):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
            logging.info(f"> Registered new event: {event_name}")
        self.listeners[event_name].append(listener)
        logging.info(f"> Added listener to event: {event_name}")

    def emit(self, event_name, *args, **kwargs):
        if event_name in self.listeners:
            total_listeners = len(self.listeners[event_name])
            logging.info(f"> Emitting event: {event_name} to {total_listeners} listener(s) with args: {args}, kwargs: {kwargs}")
            for listener in self.listeners[event_name]:
                try:
                    listener(*args, **kwargs)
                    logging.debug(f"> Listener {listener.__name__} handled event: {event_name} successfully")
                except Exception as e:
                    logging.error(f"> Error in listener {listener.__name__} for event: {event_name}: {str(e)}")
        else:
            logging.warning(f"> No listeners for event: {event_name}")

event_system = EventSystem()
