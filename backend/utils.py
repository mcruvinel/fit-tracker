from datetime import datetime, timedelta
import hashlib
import os
from typing import Dict, Any
import json

def generate_file_hash(file_path: str) -> str:
    """Gera hash SHA256 do arquivo"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def format_timedelta(delta: timedelta) -> str:
    """Formata timedelta para string HH:MM:SS"""
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def save_processed_data(file_path: str, data: Dict[str, Any]):
    """Salva dados processados em arquivo JSON"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def clean_workout_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove dados sensíveis e prepara para armazenamento"""
    cleaned = raw_data.copy()
    cleaned.pop('raw_data', None)
    return cleaned