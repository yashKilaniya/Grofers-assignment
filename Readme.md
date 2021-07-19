## Databases
1. **Orders** Stores the details of orders. Schema is as follows.<br>
order_id - **Primary key**<br>
vid - **Foreign Key**(reference vid column of Vehicle table) <br>
weight<br>
slot<br>
is_scheduled<br>
    

2. **Vehicles**<br>
    vid- **Primary key**<br>
    vtype<br>
    capacity<br>
    partner_name<br>
    orders_attached<br>

## APIs

<b>1. Health Check API</b><br>
<b>Type: GET</b><br>
<b>Response:</b> <br> 
```
"Health OK."
```


<b>2. Order Creation API</b><br>
<b>Type: POST</b><br>
<b>INPUT: <br>
```json
{
    "weight": 50,
    "slot": 4
}
```
<b>OUTPUT:</b> <br>
```json
{
    "msg": "Order created successfully.",
    "success": true
}
```

<b>3. Vehicle Creation API<b>
<b>Type: POST</b><br>
<br>INPUT: </b><br>
```json
{
    "name": "YK Logistics",
    "vehicle_id": "Truck5",
    "type": "Truck"
}
```
<b>OUTPUT: </b><br>
```json
{
    "msg": "Vehicle created successfully.",
    "success": true
}
```

<b>4. Order Scheduling API</b><br>
<b>Type: PATCH</b><br>
<b>OUTPUT:</b><br>
```json
{
    "success": true,
    "msg": "Order scheduled successfully.",
    "data": {
        "slot1_details": [
            {
                "vehicle_type": "scooter",
                "delivery_partner_name": "YK Logistics",
                "list_order_ids_assigned": [
                    "a419a97e-4874-4e06-bf1a-93588afb53fc",
                    "6f115332-d56b-4c80-b785-12e90fa52c43",
                    "e2b3c721-20da-4e2f-b692-0fd172d59747"
                ]
            }
        ],
        "slot2_details": [
            {
                "vehicle_type": "truck",
                "delivery_partner_name": "YK Logistics",
                "list_order_ids_assigned": [
                    "e568f5ca-e1bf-4bd3-860c-04621d4b5fdc",
                    "1eca5f53-9f0f-4dfd-8eaa-6de7c7e299fb",
                    "c32420e3-e8b5-462d-9c1c-27ab75c96d32"
                ]
            }
        ],
        "slot3_details": [
            {
                "vehicle_type": "scooter",
                "delivery_partner_name": "YK Logistics",
                "list_order_ids_assigned": [
                    "93566ea7-1e70-4f25-b529-3e5fb69802bf"
                ]
            },
            {
                "vehicle_type": "bike",
                "delivery_partner_name": "YK Logistics",
                "list_order_ids_assigned": [
                    "4b8b9d6b-bb09-4550-b6d3-3b5358fff946",
                    "fae326b8-8bda-4a77-a406-c79da327ded4"
                ]
            }
        ],
        "slot4_details": [
            {
                "vehicle_type": "truck",
                "delivery_partner_name": "YK Logistics",
                "list_order_ids_assigned": [
                    "1ca5f910-69e3-4a3b-a9e3-ce308b934f85",
                    "e27cd0ad-36da-4492-be26-ea15f67f7a50"
                ]
            }
        ]
    }
}
```

## Deployment
**Heroku URL: https://grofers-order-app.herokuapp.com/**

<br>
<br>

## Logic for assigning orders:
**For slot 1 :**
1. For slot1 we have only bikes and scooters available so, first we will sum the amount of weights<br>
of the orders in the first slot and will assign the vehicles as follows:<br>
```
    if 0 < total_amount <= 30:   1 BIKE
    elif 30 < total_amount <= 50: 1 Scooter
    elif 50 < total_amount <= 60: 2 BIKES
    elif 60 < total_amount <= 80: 1 BIKE 1 SCOOTER
    elif 80 < total_amount <= 100: 2 SCOOTER
```
   
**For slot 2 and slot 3 :**
1. For slot2 and slot3 we have truck,  bikes and scooters available so, first we will sum the amount of weights<br>
of the orders in the first slot and will assign the vehicles as follows:<br>
```
    if 0 < total_amount <= 30: 1 BIKE
    elif 30 < total_amount <= 50: 1 Scooter
    elif 50 < total_amount <= 60: 2 BIKES
    elif 60 < total_amount <= 80: 1 BIKE 1 SCOOTER
    elif 80 < total_amount <= 100: 1 Truck
```

**For slot 4 :**
1. For slot4, we only have trucks available so, all the orders within slot4 have to be delivered via Trucks.
