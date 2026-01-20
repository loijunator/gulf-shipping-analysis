import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = "5a25cce1ddcc073750ef6a4e67572ff59c4a804e"
# Persian Gulf Bounding Box
BOUNDING_BOX = [[[23.0, 47.0], [31.0, 57.0]]] 

async def connect_ais_stream():
    ship_data = []
    url = "wss://stream.aisstream.io/v0/stream"
    
    sub_msg = {
        "APIKey": API_KEY,
        "BoundingBoxes": BOUNDING_BOX,
        "FilterMessageTypes": ["PositionReport", "ShipStaticData"]
    }

    print("Connecting to AISStream... Collecting messages)")
    
    try:
        async with websockets.connect(url) as ws:
            await ws.send(json.dumps(sub_msg))
            
            count = 0
            while count < 300:
                raw = await ws.recv()
                msg = json.loads(raw)
                
                # Safety check: skip if not a ship message
                if "MessageType" not in msg:
                    continue
                
                res = parse_message(msg)
                if res:
                    ship_data.append(res)
                    count += 1
                    print(f"[{count}] Recv: {res['MMSI']} | Type: {res['ShipType']}")

    except Exception as e:
        print(f"Connection ended: {e}")

    save_data(ship_data)

def parse_message(msg):
    meta = msg.get("MetaData", {})
    mmsi = meta.get("MMSI")
    if not mmsi: return None

    # Default values to ensure columns always exist
    data = {
        "MMSI": mmsi,
        "ShipName": meta.get("ShipName", "Unknown"),
        "Latitude": meta.get("latitude"),
        "Longitude": meta.get("longitude"),
        "Cog": None,
        "TrueHeading": None, 
        "ShipType": None,
        "Draught": None,
        "Length": meta.get("Length"),
    }

    # Extract specific data based on message type
    inner_msg = msg.get("Message", {})
    if "PositionReport" in inner_msg:
        pos = inner_msg["PositionReport"]
        data["Cog"] = pos.get("Cog")
        data["TrueHeading"] = pos.get("TrueHeading")
        data["Status"] = pos.get("NavigationalStatus")
        data["Length"] = pos.get("")
    elif "ShipStaticData" in inner_msg:
        static = inner_msg["ShipStaticData"]
        data["ShipType"] = static.get("Type")
        data["Draught"] = static.get("MaximumStaticDraught")
        data["Dimensions"]
    
    return data

def save_data(data_list):
    if not data_list:
        print("No data to save.")
        return

    df = pd.DataFrame(data_list)
    
    # FIX FOR KEYERROR: Ensure these columns exist even if no data was found
    for col in ['ShipType', 'Draught', 'ShipName', 'Cog', 'TrueHeading']:
        if col not in df.columns:
            df[col] = None

    # Group by MMSI to combine Position and Static data
    df_final = df.groupby('MMSI').first().reset_index()
    
    df_final.to_csv("gulf_ships_BIG.csv", index=False)
    print(f"\nSaved {len(df_final)} unique ships to 'gulf_ships.csv'")
    print(df_final[['MMSI', 'ShipName', 'ShipType', 'Draught']].head())

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())
