"""
OCR scraper for LUNGS NYC map image
"""

import requests
import pytesseract
from PIL import Image
from io import BytesIO
import re
import pandas as pd
from utils import Geocoder, create_data_record

def download_and_ocr_image(url):
    """Download image and extract text using OCR"""
    print(f"Downloading image from: {url}")
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    print(f"Original image size: {img.size}")
    
    # Resize if too large (for faster OCR)
    max_size = 3000
    if img.size[0] > max_size or img.size[1] > max_size:
        ratio = min(max_size / img.size[0], max_size / img.size[1])
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        print(f"Resized to: {img.size}")
    
    print("Running OCR... (this may take 30-60 seconds)")
    
    # Extract text
    text = pytesseract.image_to_string(img)
    
    return text

def parse_lungs_map_text(text):
    """Parse OCR text to extract garden information"""
    gardens = []
    geocoder = Geocoder()
    
    # Split into lines
    lines = text.split('\n')
    
    # Look for patterns like:
    # - Garden names (usually capitalized)
    # - Addresses (street names, numbers)
    # - Neighborhoods
    
    current_garden = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Look for addresses (contains street indicators)
        if any(indicator in line.lower() for indicator in ['st', 'street', 'ave', 'avenue', 'road', 'rd', 'blvd', 'boulevard']):
            # This might be an address
            if current_garden.get('name'):
                current_garden['address'] = line
                
                # Try to geocode
                coords = geocoder.geocode(line + ", New York, NY")
                if coords:
                    current_garden['lat'], current_garden['lon'] = coords
                
                # Save and start new garden
                if current_garden.get('name') and current_garden.get('address'):
                    gardens.append(current_garden.copy())
                current_garden = {}
        
        # Look for garden names (lines with certain keywords or patterns)
        elif len(line) > 5 and line[0].isupper():
            # Potential garden name
            if 'garden' in line.lower() or 'farm' in line.lower() or 'green' in line.lower():
                current_garden['name'] = line
            elif not current_garden.get('name'):
                current_garden['name'] = line
    
    return gardens

def main():
    """Main function to scrape LUNGS NYC map"""
    
    url = "https://lungsnyc.org/wp-content/uploads/2016/09/LUNGS_map_2017-web.jpg"
    
    # Download and OCR
    text = download_and_ocr_image(url)
    
    # Save raw OCR text for inspection
    with open('lungs_map_ocr_raw.txt', 'w') as f:
        f.write(text)
    print("\n✓ Raw OCR text saved to: lungs_map_ocr_raw.txt")
    
    # Parse text
    print("\nParsing OCR text...")
    gardens = parse_lungs_map_text(text)
    
    print(f"\n✓ Found {len(gardens)} potential gardens")
    
    if gardens:
        # Convert to DataFrame
        records = []
        for garden in gardens:
            record = create_data_record(
                name=garden.get('name'),
                address=garden.get('address'),
                lat=garden.get('lat'),
                lon=garden.get('lon'),
                data_type='community_garden',
                source_url=url
            )
            records.append(record)
        
        df = pd.DataFrame(records)
        df.to_csv('lungs_map_gardens.csv', index=False)
        print(f"✓ Saved to: lungs_map_gardens.csv")
        
        # Show sample
        print("\nSample gardens found:")
        for i, garden in enumerate(gardens[:5]):
            print(f"\n{i+1}. {garden.get('name')}")
            print(f"   Address: {garden.get('address')}")
    else:
        print("\n⚠ No gardens found. Check lungs_map_ocr_raw.txt to see what OCR extracted.")
        print("The map image may need manual transcription.")

if __name__ == "__main__":
    main()
