"""
Script to merge manual data with scraped data
"""

import pandas as pd
import sys
from datetime import datetime

def merge_manual_data(scraped_csv_path, output_path=None):
    """Merge manual community fridge data with scraped data"""
    
    # Read scraped data
    print(f"Reading scraped data from: {scraped_csv_path}")
    scraped_df = pd.read_csv(scraped_csv_path)
    print(f"Scraped records: {len(scraped_df)}")
    
    # Read manual data
    manual_csv = "manual_data/community_fridges.csv"
    print(f"\nReading manual data from: {manual_csv}")
    manual_df = pd.read_csv(manual_csv)
    print(f"Manual records: {len(manual_df)}")
    
    # Combine dataframes
    combined_df = pd.concat([scraped_df, manual_df], ignore_index=True)
    
    # Remove duplicates based on name and address
    print(f"\nTotal before deduplication: {len(combined_df)}")
    combined_df['_dedup_key'] = combined_df.apply(
        lambda row: f"{str(row.get('name', '')).lower().strip()}|||{str(row.get('address', '')).lower().strip()}", 
        axis=1
    )
    combined_df = combined_df.drop_duplicates(subset=['_dedup_key'], keep='first')
    combined_df = combined_df.drop(columns=['_dedup_key'])
    print(f"Total after deduplication: {len(combined_df)}")
    
    # Sort by type and name
    combined_df = combined_df.sort_values(['type', 'name'], na_position='last')
    
    # Generate output filename if not provided
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"nyc_food_access_data_complete_{timestamp}.csv"
    
    # Save combined data
    combined_df.to_csv(output_path, index=False)
    print(f"\n✓ Combined data saved to: {output_path}")
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Records: {len(combined_df)}")
    print("\nRecords by Type:")
    type_counts = combined_df['type'].value_counts()
    for data_type, count in type_counts.items():
        print(f"  - {data_type}: {count}")
    
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python merge_manual_data.py <scraped_csv_file> [output_file]")
        print("\nExample:")
        print("  python merge_manual_data.py nyc_food_access_data_20251004_231911.csv")
        sys.exit(1)
    
    scraped_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    merge_manual_data(scraped_file, output_file)
