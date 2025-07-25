#!/usr/bin/env python3
"""
Anime-Sama Manga Scraper
A command-line tool to download manga chapters from anime-sama.fr and convert them to CBZ format.

Usage:
    python main.py "manga name" chapter_number
    
Example:
    python main.py "blue lock" 311
    python main.py "lookism" 1
"""

import sys
import os
import argparse
from scraper.anime_sama_scraper import AnimeSamaScraper

def main():
    parser = argparse.ArgumentParser(
        description='Download manga chapters from anime-sama.fr and convert to CBZ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "blue lock" 311
  python main.py "lookism" 1
  python main.py "one piece" 1095
        """
    )
    
    parser.add_argument('manga_name', help='Name of the manga (e.g., "blue lock")')
    parser.add_argument('chapter', type=int, help='Chapter number to download')
    parser.add_argument('--output', '-o', default='./downloads', 
                       help='Output directory for CBZ files (default: ./downloads)')
    parser.add_argument('--temp', '-t', default='./temp',
                       help='Temporary directory for images (default: ./temp)')
    parser.add_argument('--keep-temp', action='store_true',
                       help='Keep temporary files after conversion')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    try:
        scraper = AnimeSamaScraper(
            output_dir=args.output,
            temp_dir=args.temp,
            verbose=args.verbose
        )
        
        print(f"🔍 Starting download of '{args.manga_name}' chapter {args.chapter}")
        success = scraper.download_chapter(args.manga_name, args.chapter)
        
        if success:
            print("✅ Download and conversion completed successfully!")
            if not args.keep_temp:
                scraper.cleanup_temp()
        else:
            print("❌ Download failed. Check the manga name and chapter number.")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  Download interrupted by user.")
        return 1
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
