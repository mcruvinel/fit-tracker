from datetime import datetime
import fitparse
from typing import Dict, Any, List, Optional
import logging
import json

class FITParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.essential_fields = {
            'session': ['sport', 'start_time', 'total_distance', 'total_elapsed_time',
                      'avg_heart_rate', 'max_heart_rate', 'total_calories'],
            'record': ['timestamp', 'position_lat', 'position_long', 'altitude',
                      'heart_rate', 'cadence', 'speed', 'power'],
            'lap': ['start_time', 'end_time', 'total_distance', 'total_elapsed_time']
        }
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse a FIT file and return structured data with enhanced validation."""
        try:
            fitfile = fitparse.FitFile(file_path)
            
            # Enable data caching for better performance
            fitfile.parse()
            
            return {
                'metadata': self._process_session(fitfile),
                'records': self._process_records(fitfile),
                'laps': self._process_laps(fitfile),
                'device_info': self._process_device_info(fitfile)
            }
            
        except Exception as e:
            self.logger.exception(f"FATAL: Failed to parse FIT file {file_path}")
            raise ValueError(f"Falha na análise do arquivo FIT: {str(e)}") from e

    def _process_records(self, fitfile) -> List[Dict[str, Any]]:
        """Enhanced record processing with data validation."""
        records = []
        valid_records = 0
        
        for record in fitfile.get_messages("record"):
            try:
                record_data = self._process_message(record)
                
                if self._is_valid_record(record_data):
                    records.append(record_data)
                    valid_records += 1
                    
            except Exception as e:
                self.logger.warning(f"Record skipped: {str(e)}")
                continue
                
        self.logger.info(f"Processed {valid_records} valid records")
        return records

    def _process_session(self, fitfile) -> Dict[str, Any]:
        """Session data with complete workout summary."""
        session_data = {}
        for session in fitfile.get_messages("session"):
            session_data.update(self._process_message(session))
        
        # Convert and enhance session data
        session_data = self._enhance_session_data(session_data)
        return session_data

    def _process_laps(self, fitfile) -> List[Dict[str, Any]]:
        """Lap processing with additional metrics."""
        return [self._process_message(lap) for lap in fitfile.get_messages("lap")]

    def _process_device_info(self, fitfile) -> Optional[Dict[str, Any]]:
        """Extract device information if available."""
        for device in fitfile.get_messages("device_info"):
            return self._process_message(device)
        return None

    def _process_message(self, message) -> Dict[str, Any]:
        """Generic message processing with type conversion."""
        return {
            field.name: self._convert_field(field)
            for field in message
            if field.value is not None
        }

    def _convert_field(self, field) -> Any:
        """Smart field conversion with special handling for FIT data types."""
        value = field.value
        
        # Handle special cases
        if field.name in ['position_lat', 'position_long'] and value:
            return self._convert_semicircles_to_degrees(value)
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, (list, dict)):
            return json.dumps(value)
        
        return value

    def _is_valid_record(self, record_data: Dict[str, Any]) -> bool:
        """Validate essential record fields."""
        return any(key in record_data for key in ['timestamp', 'position_lat', 'heart_rate'])

    def _enhance_session_data(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add derived metrics and ensure data completeness."""
        # Calculate pace if available
        if 'speed' in session_data and session_data['speed']:
            session_data['avg_pace'] = self._calculate_pace(session_data['speed'])
        
        # Ensure all essential fields exist
        for field in self.essential_fields['session']:
            if field not in session_data:
                session_data[field] = None
                
        return session_data

    @staticmethod
    def _convert_semicircles_to_degrees(semicircles: int) -> float:
        """Convert FIT's semicircle units to decimal degrees."""
        return semicircles * (180 / 2**31)

    @staticmethod
    def _calculate_pace(speed_mps: float) -> str:
        """Convert m/s to min/km pace."""
        if speed_mps <= 0:
            return None
            
        pace_sec_per_km = 1000 / speed_mps
        minutes = int(pace_sec_per_km // 60)
        seconds = int(pace_sec_per_km % 60)
        return f"{minutes}:{seconds:02d} min/km"