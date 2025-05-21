import shutil
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def archive_good_enough_files(source_dir: Path, archive_subdir: str = "historicalGoodEnoughData") -> int:
    """
    Archive goodEnough CSV files to a historical storage folder with timestamps.
    
    Args:
        source_dir: Directory containing the goodEnough files
        archive_subdir: Subdirectory name for the archived files
        
    Returns:
        int: Number of files archived
    """
    # Create archive directory if it doesn't exist
    archive_dir = source_dir / archive_subdir
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Current timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Find all goodEnough files
    archived_count = 0
    for source_file in source_dir.glob("goodEnough_*.csv"):
        # Extract timeframe from filename (e.g., "goodEnough_1D.csv" → "1D")
        timeframe = source_file.stem.split("_")[1]
        
        # Create destination filename with timestamp
        dest_filename = f"goodEnough_{timeframe}_{timestamp}.csv"
        dest_file = archive_dir / dest_filename
        
        # Copy the file
        try:
            shutil.copy2(source_file, dest_file)
            archived_count += 1
            logger.info(f"Archived {source_file.name} to {dest_file.name}")
        except Exception as e:
            logger.error(f"Error archiving {source_file.name}: {str(e)}")
    
    return archived_count