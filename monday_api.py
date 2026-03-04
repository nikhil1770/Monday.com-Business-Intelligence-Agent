"""
Monday.com API Integration
Functions to query Deals and Work Orders boards
"""

import requests
from config import MONDAY_API_TOKEN, DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID

def query_monday(query):
    """Base function to query Monday.com API"""
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": MONDAY_API_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"query": query}, headers=headers)
    return response.json()


def get_deals(sector=None, status=None, limit=500):
    """
    Get deals from Monday.com Deals board
    
    Args:
        sector: Filter by Sector/service (e.g., 'Renewables', 'Mining')
        status: Filter by Deal Status (e.g., 'Won', 'Open', 'Dead')
        limit: Max number of deals to retrieve
    
    Returns:
        List of deal dictionaries
    """
    query = f'''
    {{
      boards(ids: {DEALS_BOARD_ID}) {{
        name
        items_page(limit: {limit}) {{
          items {{
            name
            column_values {{
              id
              text
              value
              column {{
                title
              }}
            }}
          }}
        }}
      }}
    }}
    '''
    
    try:
        data = query_monday(query)
        
        if 'errors' in data:
            return {"error": data['errors'][0]['message']}
        
        deals = data['data']['boards'][0]['items_page']['items']
        
        # Convert to easier format
        formatted_deals = []
        for deal in deals:
            deal_dict = {"Deal Name": deal['name']}
            for col in deal['column_values']:
                col_title = col['column']['title']
                col_value = col['text'] or col['value']
                deal_dict[col_title] = col_value
            formatted_deals.append(deal_dict)
        
        # Apply filters
        if sector:
            formatted_deals = [d for d in formatted_deals 
                             if d.get('Sector/service') == sector]
        if status:
            formatted_deals = [d for d in formatted_deals 
                             if d.get('Deal Status') == status]
        
        return formatted_deals
    
    except Exception as e:
        return {"error": str(e)}


def get_work_orders(sector=None, status=None, limit=500):
    """
    Get work orders from Monday.com Work Orders board
    
    Args:
        sector: Filter by Sector
        status: Filter by Execution Status
        limit: Max number of work orders to retrieve
    
    Returns:
        List of work order dictionaries
    """
    query = f'''
    {{
      boards(ids: {WORK_ORDERS_BOARD_ID}) {{
        name
        items_page(limit: {limit}) {{
          items {{
            name
            column_values {{
              id
              text
              value
              column {{
                title
              }}
            }}
          }}
        }}
      }}
    }}
    '''
    
    try:
        data = query_monday(query)
        
        if 'errors' in data:
            return {"error": data['errors'][0]['message']}
        
        work_orders = data['data']['boards'][0]['items_page']['items']
        
        # Convert to easier format
        formatted_wos = []
        for wo in work_orders:
            wo_dict = {"Name": wo['name']}
            for col in wo['column_values']:
                col_title = col['column']['title']
                col_value = col['text'] or col['value']
                wo_dict[col_title] = col_value
            formatted_wos.append(wo_dict)
        
        # Apply filters
        if sector:
            formatted_wos = [w for w in formatted_wos 
                           if w.get('Sector') == sector]
        if status:
            formatted_wos = [w for w in formatted_wos 
                           if w.get('Execution Status') == status]
        
        return formatted_wos
    
    except Exception as e:
        return {"error": str(e)}


def calculate_total_value(deals, value_column='Masked Deal value'):
    """
    Calculate total deal value, handling missing values
    
    Returns:
        dict with total, count, and warning about missing values
    """
    total = 0
    count = 0
    missing = 0
    
    for deal in deals:
        value = deal.get(value_column)
        if value and value != '':
            try:
                total += float(value)
                count += 1
            except (ValueError, TypeError):
                missing += 1
        else:
            missing += 1
    
    result = {
        "total": total,
        "count": count,
        "missing": missing
    }
    
    if missing > 0:
        result["warning"] = f"⚠️ {missing} deals excluded due to missing values"
    
    return result


if __name__ == "__main__":
    # Test the functions
    print("Testing Monday.com API connection...")
    
    print("\n1. Fetching deals...")
    deals = get_deals(limit=5)
    if isinstance(deals, list):
        print(f"✅ Retrieved {len(deals)} deals")
        if deals:
            print(f"Sample deal: {deals[0].get('Deal Name')}")
    else:
        print(f"❌ Error: {deals}")
    
    print("\n2. Fetching work orders...")
    wos = get_work_orders(limit=5)
    if isinstance(wos, list):
        print(f"✅ Retrieved {len(wos)} work orders")
    else:
        print(f"❌ Error: {wos}")