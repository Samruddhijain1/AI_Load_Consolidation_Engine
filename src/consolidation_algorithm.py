import pandas as pd

def consolidate_shipments(df, truck_capacity=1000):

    # Sort shipments by weight (largest first for better packing)
    df = df.sort_values(by="Weight", ascending=False)

    trucks = []
    truck_weights = []

    for index, row in df.iterrows():

        shipment_id = row["Shipment_ID"]
        weight = row["Weight"]

        placed = False

        # Try to place shipment in existing trucks
        for i in range(len(trucks)):
            if truck_weights[i] + weight <= truck_capacity:
                trucks[i].append(shipment_id)
                truck_weights[i] += weight
                placed = True
                break

        # If not placed, create new truck
        if not placed:
            trucks.append([shipment_id])
            truck_weights.append(weight)

    return trucks, truck_weights