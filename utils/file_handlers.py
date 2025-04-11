import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import h5py
import numpy as np

class FileHandler:
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """
        Read a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Dictionary containing the JSON data
        """
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def write_json(data: Dict[str, Any], file_path: str):
        """
        Write data to a JSON file.
        
        Args:
            data: Dictionary to write
            file_path: Path to write the JSON file
        """
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        """
        Read a YAML file.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Dictionary containing the YAML data
        """
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def write_yaml(data: Dict[str, Any], file_path: str):
        """
        Write data to a YAML file.
        
        Args:
            data: Dictionary to write
            file_path: Path to write the YAML file
        """
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    
    @staticmethod
    def read_hdf5(file_path: str, dataset_path: str) -> Optional[np.ndarray]:
        """
        Read a dataset from an HDF5 file.
        
        Args:
            file_path: Path to the HDF5 file
            dataset_path: Path to the dataset within the file
            
        Returns:
            Numpy array containing the dataset data
        """
        try:
            with h5py.File(file_path, 'r') as f:
                return np.array(f[dataset_path])
        except Exception as e:
            print(f"Error reading HDF5 file: {str(e)}")
            return None
    
    @staticmethod
    def write_hdf5(data: np.ndarray, file_path: str, dataset_path: str):
        """
        Write data to an HDF5 file.
        
        Args:
            data: Numpy array to write
            file_path: Path to write the HDF5 file
            dataset_path: Path to the dataset within the file
        """
        with h5py.File(file_path, 'a') as f:
            if dataset_path in f:
                del f[dataset_path]
            f.create_dataset(dataset_path, data=data)
    
    @staticmethod
    def ensure_directory(directory: str):
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            directory: Path to the directory
        """
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def clean_directory(directory: str, pattern: str = "*"):
        """
        Remove files matching a pattern from a directory.
        
        Args:
            directory: Path to the directory
            pattern: Glob pattern for files to remove
        """
        for file in Path(directory).glob(pattern):
            file.unlink() 