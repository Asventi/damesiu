class EventHandler(object):
    """
    Un event handler classique
    """
    callbacks = None

    def on(self, eh_name, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if eh_name not in self.callbacks:
            self.callbacks[eh_name] = [callback]
        else:
            self.callbacks[eh_name].append(callback)

    def trigger(self, eh_name, **kwargs):
        if self.callbacks is not None and eh_name in self.callbacks:
            for callback in self.callbacks[eh_name]:
                callback(**kwargs)