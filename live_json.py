import json
import uuid
from pathlib import Path
from typing import Dict, MutableMapping, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class LiveJson(MutableMapping[KT, VT]):
    path = f"{str(uuid.uuid4())[24:]}.json"
    indent = 4

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self._file = Path(self.path).expanduser()

        if not self._file.exists():
            self._file.parent.mkdir(parents=True, exist_ok=True)
            self._file.write_text("{}")

        self.update(dict(*args, **kwargs))

    def _load(self) -> Dict[KT, VT]:
        return json.loads(self._file.read_text())

    def _save(self, dct: Dict[KT, VT]) -> None:
        self._file.write_text(json.dumps(dct, indent=self.indent))

    def update(self, *args, **kwargs) -> None:
        dct = self._load()
        dct.update(dict(*args, **kwargs))
        self._save(dct)

    def __getitem__(self, key: KT) -> VT:
        dct = self._load()
        return dct[key]

    def __setitem__(self, key: KT, value: VT) -> None:
        dct = self._load()
        dct[key] = value
        self._save(dct)

    def __delitem__(self, key: KT) -> None:
        dct = self._load()
        del dct[key]
        self._save(dct)

    def __iter__(self):
        dct = self._load()
        return iter(dct)

    def __len__(self) -> int:
        dct = self._load()
        return len(dct)

    def __str__(self) -> str:
        dct = self._load()
        return str(dct)

    def __repr__(self) -> str:
        dct = self._load()
        return repr(dct)
