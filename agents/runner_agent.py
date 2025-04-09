import subprocess
import time
from typing import Dict, Any, Optional
from pathlib import Path

class RunnerAgent:
    def __init__(self):
        self.process = None
        self.output_file = "openmc_output.txt"
    
    def run_openmc(self, work_dir: str = ".") -> bool:
        """
        Run OpenMC simulation and monitor its progress.
        
        Args:
            work_dir: Directory containing input files
            
        Returns:
            bool: True if simulation completed successfully, False otherwise
        """
        try:
            # Change to working directory
            original_dir = Path.cwd()
            work_path = Path(work_dir)
            work_path.mkdir(parents=True, exist_ok=True)
            
            # Run OpenMC
            with open(self.output_file, 'w') as f:
                self.process = subprocess.Popen(
                    ['openmc'],
                    cwd=work_dir,
                    stdout=f,
                    stderr=subprocess.STDOUT
                )
            
            # Monitor process
            while self.process.poll() is None:
                time.sleep(1)
                # TODO: Add progress monitoring logic
                # This could include:
                # 1. Parsing output file for progress
                # 2. Checking for errors
                # 3. Implementing timeout
            
            return self.process.returncode == 0
            
        except Exception as e:
            print(f"Error running OpenMC: {str(e)}")
            return False
        finally:
            # Restore original directory
            os.chdir(original_dir)
    
    def get_output(self) -> Optional[str]:
        """
        Get the simulation output.
        
        Returns:
            str: Contents of the output file if it exists, None otherwise
        """
        try:
            with open(self.output_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def cleanup(self):
        """Clean up temporary files."""
        if Path(self.output_file).exists():
            Path(self.output_file).unlink() 