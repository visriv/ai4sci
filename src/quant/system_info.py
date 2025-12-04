import subprocess
from ..utils.logger import get_logger

logger = get_logger("SysInfo")

def get_metal_info():
    try:
        out = subprocess.check_output(
            ["system_profiler", "SPDisplaysDataType"]
        ).decode()
        logger.info("[Hardware] Apple GPU info:")
        logger.info(out)
    except Exception as e:
        logger.error(f"[Hardware] Could not read GPU info: {e}")

if __name__ == "__main__":
    get_metal_info()