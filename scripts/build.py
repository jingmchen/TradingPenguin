import py_compile
import shutil
from pathlib import Path

SRC_DIR = Path("src") / "tradingpenguin"
BUILD_DIR = Path("build") / "tradingpenguin"

# -- Remove old build folder
if BUILD_DIR.exists():
    shutil.rmtree(BUILD_DIR)

# -- Make new build folder
BUILD_DIR.mkdir(parents=True, exist_ok=True)

# -- Compile all .py to build
for src_file in SRC_DIR.rglob("*.py"):
    rel_path = src_file.relative_to(SRC_DIR)
    dst_file = BUILD_DIR / rel_path.with_suffix(".pyc") # Get path for .pyc
    dst_file.parent.mkdir(parents=True, exist_ok=True) # Make dir in build fldr
    py_compile.compile(src_file, cfile=dst_file, optimize=2)

print(f"Build completed. Compiled files are in {BUILD_DIR}.")