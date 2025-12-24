from typing import Callable, Dict, List, Any

class MessageBus:
    """Système simple de publication/abonnement"""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event_type: str, data: Any = None):
        if event_type in self._subscribers:
            results = []
            for handler in self._subscribers[event_type]:
                # Assuming handlers can be async or sync, simplistic handling here
                try:
                    import inspect
                    if inspect.iscoroutinefunction(handler):
                        res = await handler(data)
                        results.append(res)
                    else:
                        res = handler(data)
                        results.append(res)
                except Exception as e:
                    print(f"Error handling event {event_type}: {e}")
            return results
        return []

# Instance globale
message_bus = MessageBus()
