"""
CBZ file creation utilities
"""

import os
import zipfile
import tempfile
from pathlib import Path

class CBZConverter:
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def create_cbz(self, images_dir, output_path):
        """
        Create a CBZ file from a directory of images.
        
        Args:
            images_dir (str): Directory containing image files
            output_path (str): Path for the output CBZ file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(images_dir):
                print(f"❌ Images directory does not exist: {images_dir}")
                return False
            
            # Get all image files and sort them
            image_files = self._get_image_files(images_dir)
            if not image_files:
                print(f"❌ No image files found in: {images_dir}")
                return False
            
            # Sort files to ensure correct page order
            image_files.sort()
            
            if self.verbose:
                print(f"📦 Creating CBZ with {len(image_files)} images")
                print(f"   Output: {output_path}")
            
            # Create the CBZ file (which is just a ZIP file)
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as cbz_file:
                for image_file in image_files:
                    image_path = os.path.join(images_dir, image_file)
                    
                    # Add the image to the CBZ with just the filename (no directory structure)
                    cbz_file.write(image_path, image_file)
                    
                    if self.verbose:
                        print(f"   ✅ Added: {image_file}")
            
            # Verify the CBZ was created successfully
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                file_size = os.path.getsize(output_path)
                if self.verbose:
                    print(f"✅ CBZ created successfully: {output_path} ({file_size} bytes)")
                return True
            else:
                print(f"❌ Failed to create CBZ file: {output_path}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating CBZ file: {str(e)}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
    
    def _get_image_files(self, directory):
        """
        Get all image files from a directory.
        
        Args:
            directory (str): Directory to scan
            
        Returns:
            list: List of image filenames
        """
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        image_files = []
        
        try:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in image_extensions:
                        image_files.append(filename)
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Warning: Error scanning directory {directory}: {str(e)}")
        
        return image_files
    
    def verify_cbz(self, cbz_path):
        """
        Verify that a CBZ file is valid and contains images.
        
        Args:
            cbz_path (str): Path to the CBZ file
            
        Returns:
            bool: True if CBZ is valid, False otherwise
        """
        try:
            if not os.path.exists(cbz_path):
                return False
            
            with zipfile.ZipFile(cbz_path, 'r') as cbz_file:
                file_list = cbz_file.namelist()
                
                # Check if there are any files
                if not file_list:
                    return False
                
                # Check if files have image extensions
                image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
                image_count = 0
                
                for filename in file_list:
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in image_extensions:
                        image_count += 1
                
                return image_count > 0
                
        except Exception:
            return False
    
    def list_cbz_contents(self, cbz_path):
        """
        List the contents of a CBZ file.
        
        Args:
            cbz_path (str): Path to the CBZ file
            
        Returns:
            list: List of filenames in the CBZ, or empty list if error
        """
        try:
            with zipfile.ZipFile(cbz_path, 'r') as cbz_file:
                return sorted(cbz_file.namelist())
        except Exception:
            return []
