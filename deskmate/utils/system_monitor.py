"""
系统资源监控 / System resource monitor
轻量级CPU、内存使用率采集，无额外依赖 / Lightweight CPU & memory usage monitor, no extra dependencies
"""

import os
import time
from typing import Optional, Tuple


class SystemMonitor:
    """
    系统资源监控器 / System resource monitor
    跨平台采集CPU和内存使用率 / Cross-platform CPU and memory usage collection
    """

    def __init__(self):
        self._last_cpu_times = None
        self._last_cpu_time = None
        self._cpu_usage = 0.0
        self._memory_usage = 0.0
        self._last_update = 0

    def get_cpu_usage(self) -> float:
        """
        获取CPU使用率(0-100) / Get CPU usage percentage (0-100)
        使用/proc/stat (Linux) 或 psutil 回退 / Uses /proc/stat (Linux) or psutil fallback
        """
        now = time.time()
        if now - self._last_update < 1.0 and self._cpu_usage > 0:
            return self._cpu_usage

        try:
            if os.name == "posix" and os.path.exists("/proc/stat"):
                usage = self._read_linux_cpu()
            else:
                usage = self._read_via_psutil()
            self._cpu_usage = usage
        except Exception:
            self._cpu_usage = 0.0

        self._last_update = now
        return self._cpu_usage

    def _read_linux_cpu(self) -> float:
        """从/proc/stat读取CPU使用率 / Read CPU usage from /proc/stat"""
        with open("/proc/stat", "r") as f:
            line = f.readline()
        parts = line.split()
        # user, nice, system, idle, iowait, irq, softirq, steal
        times = [int(x) for x in parts[1:9]]
        idle = times[3] + times[4]
        total = sum(times)

        if self._last_cpu_times is not None:
            dt = total - self._last_cpu_times[0]
            di = idle - self._last_cpu_times[1]
            if dt > 0:
                usage = (1.0 - di / dt) * 100.0
            else:
                usage = 0.0
        else:
            usage = 0.0

        self._last_cpu_times = (total, idle)
        return max(0.0, min(100.0, usage))

    def _read_via_psutil(self) -> float:
        """通过psutil读取（如果安装了）/ Read via psutil if installed"""
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            return 0.0

    def get_memory_usage(self) -> float:
        """
        获取内存使用率(0-100) / Get memory usage percentage (0-100)
        """
        try:
            if os.name == "posix" and os.path.exists("/proc/meminfo"):
                usage = self._read_linux_memory()
            else:
                usage = self._read_memory_via_psutil()
            self._memory_usage = usage
        except Exception:
            pass
        return self._memory_usage

    def _read_linux_memory(self) -> float:
        """从/proc/meminfo读取内存使用率 / Read memory usage from /proc/meminfo"""
        info = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = int(parts[1].strip().split()[0])
                    info[key] = val

        total = info.get("MemTotal", 1)
        available = info.get("MemAvailable", info.get("MemFree", 0))
        used = total - available
        return (used / total) * 100.0 if total > 0 else 0.0

    def _read_memory_via_psutil(self) -> float:
        """通过psutil读取内存 / Read memory via psutil"""
        try:
            import psutil
            return psutil.virtual_memory().percent
        except ImportError:
            return 0.0

    def get_status_text(self) -> str:
        """获取状态文本 / Get status text"""
        cpu = self.get_cpu_usage()
        mem = self.get_memory_usage()
        return f"CPU {cpu:.0f}% | MEM {mem:.0f}%"

    def get_status_tuple(self) -> Tuple[float, float]:
        """获取(CPU%, 内存%)元组 / Get (CPU%, memory%) tuple"""
        return (self.get_cpu_usage(), self.get_memory_usage())
