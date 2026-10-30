"""Hardware and Compute Resource Inspector for ADAPT-AI Training Pipeline."""

import os
import platform
import multiprocessing
from typing import Dict, Any, Optional
from adapt_ai.models.schemas import HardwareResourceReport
from adapt_ai.security.phi_sanitizer import logger


class ResourceInspector:
    """Inspects local hardware to assess training and inference feasibility."""

    @staticmethod
    def inspect() -> HardwareResourceReport:
        cpu_count = multiprocessing.cpu_count()
        system_os = f"{platform.system()} {platform.release()}"

        # Probe system memory
        ram_total_gb = 16.0
        ram_available_gb = 8.0
        try:
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong)
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                ram_total_gb = round(stat.ullTotalPhys / (1024 ** 3), 2)
                ram_available_gb = round(stat.ullAvailPhys / (1024 ** 3), 2)
        except Exception:
            pass

        # Probe GPU presence
        gpu_available = False
        gpu_name: Optional[str] = None
        vram_total_gb: Optional[float] = None

        try:
            import torch
            if torch.cuda.is_available():
                gpu_available = True
                gpu_name = torch.cuda.get_device_name(0)
                vram_total_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2)
        except ImportError:
            pass

        # Determine compute tier
        if gpu_available and vram_total_gb and vram_total_gb >= 24.0:
            compute_tier = "HIGH_VRAM_SERVER"
        elif gpu_available and vram_total_gb and vram_total_gb >= 8.0:
            compute_tier = "LOW_VRAM_GPU"
        else:
            compute_tier = "CPU_ONLY"

        # Feasibility assessment
        feasibility = {
            "full_parameter_finetune_8b": (
                "Feasible with DeepSpeed ZeRO-3 on 80GB VRAM" if compute_tier == "HIGH_VRAM_SERVER"
                else "NOT FEASIBLE on current hardware (Requires >= 64GB-80GB VRAM GPU)."
            ),
            "qlora_4bit_finetune_8b": (
                "Feasible locally" if compute_tier in ["HIGH_VRAM_SERVER", "LOW_VRAM_GPU"]
                else "NOT FEASIBLE on CPU alone. Local QLoRA requires an NVIDIA GPU with at least 16GB VRAM."
            ),
            "lora_peft_small_model_1b_3b": (
                "Feasible locally" if compute_tier != "CPU_ONLY"
                else "Marginal/Impractical on CPU (Extreme latency, risk of RAM paging)."
            ),
            "hosted_api_finetuning": "FEASIBLE (Inference and training managed remotely via secure cloud endpoints).",
            "rag_vector_search_inference": "FEASIBLE LOCALLY (Fully optimized via NumPy dot-product vector engine)."
        }

        return HardwareResourceReport(
            cpu_count=cpu_count,
            system_os=system_os,
            ram_total_gb=ram_total_gb,
            ram_available_gb=ram_available_gb,
            gpu_available=gpu_available,
            gpu_name=gpu_name,
            vram_total_gb=vram_total_gb,
            compute_tier=compute_tier,
            training_feasibility=feasibility
        )

