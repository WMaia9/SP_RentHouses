import os
import pandas as pd
import zapimoveis_scraper as zap

def scrape_data(localization, num_pages=1, property_types=['casas', 'apartamentos']):
    """
    Scrapes real estate data from Zap Imóveis for a given localization and property type.
    
    Parameters:
    - localization: The location to scrape data for (e.g., 'sp+sao-paulo+zona-oeste').
    - num_pages: Number of pages to scrape (default is 1).
    - property_types: List of property types to scrape (default is ['casas', 'apartamentos']).
    
    Returns:
    - A DataFrame containing the scraped data.
    """
    data = []

    for property_type in property_types:
        print(f"Scraping {property_type} in {localization}...")
        try:
            results = zap.search(localization=localization, num_pages=num_pages, tipo=property_type)
            if not results:
                raise ValueError("No data returned from the server.")
            for result in results:
                data.append({
                    'Address': result.address,
                    'Zone': localization,
                    'Type': property_type,
                    'Total Area': result.total_area_m2,
                    'Bathrooms': result.bathrooms,
                    'Bedrooms': result.bedrooms,
                    'Vacancies': result.vacancies,
                    'Price': result.price,
                    'Description': result.description,
                    'Link': result.link
                })
        except Exception as e:
            print(f"Error scraping {property_type} in {localization}: {e}")
    
    df = pd.DataFrame(data)
    return df

def save_data(df, localization, save_dir='data/raw'):
    """
    Saves the scraped data to a CSV file.
    
    Parameters:
    - df: The DataFrame containing the data to save.
    - localization: The localization used to name the CSV file.
    - save_dir: The directory where the CSV file will be saved (default is 'data/raw').
    """
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f'{localization}.csv')
    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False, header=True, sep=',')
    else:
        df.to_csv(file_path, mode='a', index=False, header=False, sep=',')

    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    localizations = [
        'sp+sao-paulo+zona-oeste',
        'sp+sao-paulo+zona-norte',
        'sp+sao-paulo+zona-sul',
        'sp+sao-paulo+zona-leste',
        'sp+sao-paulo+centro'
    ]

    # Number of pages to scrape (you can hardcode this or take input)
    num_pages = int(input('Number of pages to scrape: '))

    for loc in localizations:
        df = scrape_data(loc, num_pages)
        if not df.empty:
            save_data(df, loc)
        else:
            print(f"No data scraped for {loc}. Check if the URL or parameters are correct.")