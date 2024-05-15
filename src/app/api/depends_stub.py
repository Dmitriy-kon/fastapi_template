import inspect
from typing import Annotated, Any, Callable, ParamSpec, TypeVar
 
from fastapi import Depends


class Stub:
    """
    This class is used to prevent fastapi from digging into
    real dependencies attributes detecting them as request data

    So instead of
    `interactor: Annotated[Interactor, Depends()]`
    Write
    `interactor: Annotated[Interactor, Depends(Stub(Interactor))]`

    And then you can declare how to create it:
    `app.dependency_overrids[Interactor] = some_real_factory`

    """

    def __init__(self, dependency: Callable, **kwargs):
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self):
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        if isinstance(other, Stub):
            return (
                    self._dependency == other._dependency
                    and self._kwargs == other._kwargs
            )
        else:
            if not self._kwargs:
                return self._dependency == other
            return False

    def __hash__(self):
        if not self._kwargs:
            return hash(self._dependency)
        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)

P = ParamSpec("P")
T = TypeVar("T")
 
 
def wrap_factory(factory: Callable[P, T], **kwargs: Callable[..., Any]) -> Callable[P, T]:
    def provider(*args: P.args, **kwargs: P.kwargs) -> T:
        return factory(*args, **kwargs)
 
    factory_sig = inspect.signature(factory)
    new_params: list[inspect.Parameter] = []
    for param in factory_sig.parameters.values():
        if param.name in kwargs:
            stub = kwargs[param.name]
        else:
            stub = Stub(param.annotation)
        new_params.append(param.replace(annotation=Annotated[param.annotation, Depends(stub)]))
 
    provider_sig = inspect.signature(provider)
    new_sig = provider_sig.replace(parameters=new_params, return_annotation=factory_sig.return_annotation)
    new_hints = {param.name: param.annotation for param in new_params}
    provider.__signature__ = new_sig
    provider.__annotations__ = new_hints
    return provider