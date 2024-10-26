import time
from typing import Optional
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

class ProgressTracker:
    """Tracks progress of long-running operations with detailed logging."""
    
    def __init__(self, total_steps: int, operation_name: str):
        self.total_steps = total_steps
        self.current_step = 0
        self.operation_name = operation_name
        self.start_time = time.time()
        self.last_update = self.start_time
        self.update_interval = 5  # seconds between progress updates
        
    def update(self, step: Optional[int] = None, message: str = ""):
        """Update progress with detailed logging."""
        current_time = time.time()
        
        if step is not None:
            self.current_step = step
        else:
            self.current_step += 1
            
        # Calculate progress percentage
        progress = (self.current_step / self.total_steps) * 100
        
        # Calculate elapsed time
        elapsed = current_time - self.start_time
        elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
        
        # If enough time has passed since last update
        if current_time - self.last_update >= self.update_interval:
            # Estimate remaining time
            if self.current_step > 0:
                time_per_step = elapsed / self.current_step
                remaining_steps = self.total_steps - self.current_step
                remaining_time = remaining_steps * time_per_step
                remaining_str = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
            else:
                remaining_str = "Unknown"
            
            # Log detailed progress
            log_message = (
                f"{self.operation_name}: {progress:.1f}% complete "
                f"({self.current_step}/{self.total_steps})\n"
                f"Elapsed: {elapsed_str}, Estimated remaining: {remaining_str}"
            )
            if message:
                log_message += f"\nCurrent activity: {message}"
                
            logger.info(log_message)
            self.last_update = current_time
    
    def complete(self, message: str = "Operation completed"):
        """Log completion of operation."""
        elapsed = time.time() - self.start_time
        elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
        
        logger.info(
            f"{self.operation_name} completed in {elapsed_str}\n"
            f"Final status: {message}"
        )
