"""Exercise the actual sketch with host-side serial/register substitutes."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class FirmwareCommands(unittest.TestCase):
    @unittest.skipUnless(shutil.which('g++'), 'Host C++ compiler required')
    def test_command_framing_and_enable_state(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = str(Path(directory) / 'firmware_commands')
            subprocess.run(['g++', '-std=c++11', '-I', str(ROOT/'tests/firmware_stubs'),
                            str(ROOT/'tests/firmware_commands.cpp'), '-o', binary], check=True)
            subprocess.run([binary], check=True)
