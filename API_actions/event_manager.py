# ./API_actions/event_manager.py

class EventManager:
    def __init__(self):
        # Initialize a dictionary to store event listeners
        self.listeners = {}

    def register(self, event_name, callback):
        # Register a callback function for a specific event
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def unregister(self, event_name, callback):
        # Unregister a callback function for a specific event
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)
            if not self.listeners[event_name]:
                del self.listeners[event_name]

    def notify(self, event_name, *args, **kwargs):
        # Notify all listeners of an event with the given arguments
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(*args, **kwargs)
