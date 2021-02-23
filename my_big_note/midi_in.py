import typing as ty
import abc

import rtmidi
from . import MyBigNoteError


class MidiError(MyBigNoteError):
    ...


class MidiInput(abc.ABC):

    def __init__(
        self,
        api: ty.Optional[int] = None,
        port: ty.Optional[int] = None,
        callback_data: ty.Optional[object] = None,
        name: str = 'MyBigNoteIn',
    ) -> None:
        self._api = api
        self._port = port
        self._apis: ty.Dict[str, int] = {}
        self._in: ty.Optional[rtmidi.MidiIn] = None
        self.callback_data = callback_data
        self.name = name

    def init(self, api: ty.Optional[int] = None, port: int = 0) -> None:
        if self._in:
            self.shutdown()
        if api is not None:
            self._api = api
        self._in = rtmidi.MidiIn(rtapi=self.api, name=self.name)
        self.use_port(port)

    @abc.abstractmethod
    def callback(
        self,
        msg: ty.Tuple[ty.Tuple[int, int, int], float],
        data: ty.Optional[object] = None
    ) -> None:
        ...

    @property
    def apis(self) -> ty.Dict[str, int]:
        if not self._apis:
            self._apis = self._get_apis()
        return self._apis

    def _get_apis(self) -> ty.Dict[str, int]:
        return {
            rtmidi.get_api_name(api): api
            for api in rtmidi.get_compiled_api()
        }

    @property
    def api(self) -> int:
        if not self._api:
            return rtmidi.get_compiled_api()[0]  # type:ignore
        return self._api

    @property
    def ports(self) -> ty.List[str]:
        if not self._in:
            raise MidiError(
                'Midi input is not initialized, use init() method.'
            )
        return self._in.get_ports()  # type:ignore

    def use_port(self, port: int) -> None:
        if not self._in:
            raise MidiError(
                'Midi input is not initialized, use init() method.'
            )
        if self._in.is_port_open():
            self._in.close_port()
        self._in.open_port(port)
        self.callback((0, 0))
        self._in.set_callback(self.callback, self.callback_data)

    def shutdown(self) -> None:
        if not self._in:
            return
        self._in.close_port()
        self._in.delete()
        self._in = None


class SingleNoteInput(MidiInput):

    def __init__(
        self,
        api: ty.Optional[int] = None,
        port: ty.Optional[int] = None,
        callback_data: ty.Optional[object] = None,
        name: str = 'MyBigNoteIn',
    ) -> None:
        super().__init__(
            api=api, port=port, callback_data=callback_data, name=name
        )
        self.note: ty.Optional[int] = None

    def callback(
        self,
        msg: ty.Tuple[ty.Tuple[int, int, int], float],
        data: ty.Optional[object] = None
    ) -> None:
        status = msg[0]
        if isinstance(status, int):
            return None
        if 0x90 <= status[0] < 0xa0:
            self.note = status[1]
            return
        if self.note == status[1] and 0x80 <= status[0] < 0x90:
            self.note = None
            return
