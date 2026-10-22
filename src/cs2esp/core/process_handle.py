from __future__ import annotations

import time
from dataclasses import dataclass

import pymem


@dataclass
class ProcessHandle:
    pm: pymem.Pymem
    module_base: int
    module_name: str

    @classmethod
    def attach(cls, exe: str, module: str) -> "ProcessHandle":
        pm = pymem.Pymem(exe)
        base = pymem.process.module_from_name(pm.process_handle, module).lpBaseOfDll
        return cls(pm=pm, module_base=base, module_name=module)

    def read_int(self, address: int) -> int:
        return self.pm.read_int(address)

    def read_float(self, address: int) -> float:
        return self.pm.read_float(address)

    def read_vec3(self, address: int) -> tuple[float, float, float]:
        return self.pm.read_float(address), self.pm.read_float(address + 4), self.pm.read_float(address + 8)

    def read_matrix(self, address: int) -> list[float]:
        return [self.pm.read_float(address + i * 4) for i in range(16)]

    def close(self) -> None:
        try:
            self.pm.close_process()
        except Exception:  # noqa: BLE001
            pass

    def wait_for_module(self, name: str, timeout_s: float = 10.0) -> int:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            mod = pymem.process.module_from_name(self.pm.process_handle, name)
            if mod:
                return mod.lpBaseOfDll
            time.sleep(0.25)
        raise TimeoutError(f"module {name} not found")