# Authors: DevL0rd
import uuid


class Events:
    """A generic asynchrounous event system."""

    events = {
        "event": {},
        "unhandledEvent": {}
    }

    def on(self, eventName, callBack):
        """Register a callback function for a particular event. And returns a callbackID (GUID) of the event for unregistering later.

        Keyword Arguments:
        eventName -- Name of the event. This event does not have to be registered at the time of calling this.
        callBack -- function to callback to, returns a dict with event relevant data.

        Description:
            The event does not have to be registered at the time of calling this.
            If a event fires without registering, the 'unhandledEvent' event will fire.

        """
        if not eventName in self.events:
            self.events[eventName] = {}
        newUUID = str(uuid.uuid4())
        self.events[eventName][newUUID] = callBack
        return newUUID

    def removeListener(self, eventName, callbackID):
        """Remove a event listender by it's callbackID (GUID)

        Keyword Arguments:
        eventName -- Name of the event.
        callbackID -- callBackID returned by regstering a callback with self.on.
        """
        if not eventName in self.events:
            return
        eventCallbacks = self.events[eventName]
        if not callbackID in eventCallbacks:
            return
        del eventCallbacks[callbackID]

    def trigger(self, eventName, data={}):
        """Trigger a event synchronously with event name and optional data.

        Keyword Arguments:
        eventName -- Name of the event.
        data -- Data associated with event. Defaults to {}.

        Description:
        Fires the event synchronously, and if the event is not handled, it fires "unhandledEvent"
        """
        for eventCallbackId in self.events["event"]:
            # Emit a genereal event event to pass all events to something.
            eventCallback = self.events["event"][eventCallbackId]
            eventCallback(eventName, data)

        if eventName in self.events:
            for eventCallbackId in self.events[eventName]:
                eventCallback = self.events[eventName][eventCallbackId]
                if eventCallback(data):
                    return  # if the event returns true, stop processing events as it was handled

        for eventCallbackId in self.events["unhandledEvent"]:
            # If it was unhandled emit a unhandled event
            eventCallback = self.events["event"][eventCallbackId]
            eventCallback(eventName, data)
