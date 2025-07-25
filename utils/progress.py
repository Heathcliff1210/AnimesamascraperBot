"""
Progress tracking utilities for downloads
"""

import sys
import time

class ProgressTracker:
    def __init__(self, total, description="Progress"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.last_update = 0
        
    def update(self, current=None):
        """
        Update the progress tracker.
        
        Args:
            current (int): Current progress value. If None, increments by 1.
        """
        if current is not None:
            self.current = current
        else:
            self.current += 1
        
        # Only update display every 0.1 seconds to avoid spam
        now = time.time()
        if now - self.last_update < 0.1 and self.current < self.total:
            return
        
        self.last_update = now
        self._display_progress()
    
    def _display_progress(self):
        """Display the current progress."""
        if self.total == 0:
            return
        
        percent = (self.current / self.total) * 100
        elapsed = time.time() - self.start_time
        
        # Calculate ETA
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = self._format_time(eta)
        else:
            eta_str = "??:??"
        
        # Create progress bar
        bar_length = 30
        filled_length = int(bar_length * self.current // self.total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # Display progress
        elapsed_str = self._format_time(elapsed)
        progress_line = f"\r{self.description}: |{bar}| {self.current}/{self.total} ({percent:.1f}%) - {elapsed_str} elapsed, ETA: {eta_str}"
        
        sys.stdout.write(progress_line)
        sys.stdout.flush()
    
    def finish(self):
        """Mark progress as complete."""
        self.current = self.total
        self._display_progress()
        elapsed = time.time() - self.start_time
        elapsed_str = self._format_time(elapsed)
        print(f"\n✅ {self.description} completed in {elapsed_str}")
    
    def _format_time(self, seconds):
        """
        Format seconds into MM:SS format.
        
        Args:
            seconds (float): Time in seconds
            
        Returns:
            str: Formatted time string
        """
        if seconds < 0:
            return "00:00"
        
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

class SimpleSpinner:
    """A simple spinning progress indicator."""
    
    def __init__(self, message="Working"):
        self.message = message
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current = 0
        self.running = False
    
    def start(self):
        """Start the spinner."""
        self.running = True
        self._spin()
    
    def stop(self, final_message=None):
        """Stop the spinner."""
        self.running = False
        if final_message:
            sys.stdout.write(f"\r{final_message}\n")
        else:
            sys.stdout.write(f"\r{' ' * (len(self.message) + 10)}\r")
        sys.stdout.flush()
    
    def _spin(self):
        """Display the spinning animation."""
        if self.running:
            char = self.spinner_chars[self.current % len(self.spinner_chars)]
            sys.stdout.write(f"\r{char} {self.message}...")
            sys.stdout.flush()
            self.current += 1
