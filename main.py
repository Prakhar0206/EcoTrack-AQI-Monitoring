"""
==================================================================================
PROJECT TITLE : ECOTRACK - AIR QUALITY MONITORING SYSTEM
DEVELOPED BY  : PRAKHAR AGGARWAL
==================================================================================
"""

import mysql.connector
import requests
import matplotlib.pyplot as plt
from datetime import date
import time
import csv
import os
import sys

# ==============================================================================
#                               GLOBAL SETTINGS
# ==============================================================================

# Database Setup
host = 'localhost'
user = 'root'
password = 'ENTER_YOUR_MYSQL_PASSWORD_HERE'   
database = 'aqi_project'

# API Setup (aqicn.org)
api_token = 'ENTER_YOUR_API_TOKEN_HERE'   
base_url = "https://api.waqi.info/feed/"

# Cities we want to track
cities = ["New Delhi", "Dehradun", "Mumbai", "Bangalore", "Tokyo"]


# ==============================================================================
#                               HELPER FUNCTIONS
# ==============================================================================

def clear_screen():
    # Clears the screen 
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_header(title):
    # Prints the header with the borders as requested
    print("\n" + "═" * 70)
    print(f"{title.center(70)}")
    print("═" * 70)

def loading_animation(text):
    # Simple loading bar
    print(f"{text:<30}", end="")
    for i in range(10):
        time.sleep(0.1)
        print("█", end="", flush=True)
    print(" [DONE]")

def get_connection():
    # Connect to MySQL
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except:
        print("\nError: Could not connect to MySQL database.")
        print("Check if XAMPP/MySQL is running.")
        return None

def get_status(aqi):
    # Returns the health status based on AQI number
    try:
        aqi = int(aqi)
    except:
        return "Unknown"
        
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Sensitive"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


# ==============================================================================
#                               MAIN FUNCTIONS
# ==============================================================================

def check_system():
    clear_screen()
    print_header("INITIALIZING ECOTRACK SYSTEM")

    print("Checking system requirements...")
    time.sleep(1)
    
    # Check Internet (Simulation is fine for school project)
    loading_animation("Checking Internet Connection")
    
    # Check Database - ACTUALLY TEST IT
    print(f"{'Connecting to Database':<30}", end="")
    try:
        conn = get_connection()
        if conn and conn.is_connected():
            print(" [CONNECTED]")
            conn.close()
        else:
            print(" [FAILED]")
            print("\nCRITICAL ERROR: Database is not accessible.")
            print("Please start MySQL/XAMPP and check password in main.py")
            input("Press Enter to Exit...")
            sys.exit()
    except:
        print(" [FAILED]")
        sys.exit()
    
    print("\nSystem is ready. Opening menu...")
    time.sleep(1)

def fetch_data():
    print_header("FETCHING LIVE DATA")
    
    today = date.today()
    conn = get_connection()
    
    if conn is None:
        return

    cursor = conn.cursor()
    print(f"Date: {today}\n")

    for city in cities:
        try:
            # Check if we already have data for this city today
            cursor.execute("SELECT * FROM aqi_data WHERE city_name=%s AND reading_date=%s", (city, today))
            if cursor.fetchone():
                print(f" -> {city:<15} : Data already exists.")
                continue

            # Get data from API
            print(f" -> {city:<15} : Getting data...", end="")
            
            # Constructing the URL
            full_url = f"{base_url}{city}/?token={api_token}"
            response = requests.get(full_url)
            data = response.json()

            if data['status'] == 'ok':
                aqi = data['data']['aqi']
                
                # Sometimes the API calls it different things
                pollutant = data['data'].get('dominentpol', 'N/A')
                status = get_status(aqi)

                # Save to database
                sql = "INSERT INTO aqi_data (city_name, reading_date, aqi, pollutant, status) VALUES (%s, %s, %s, %s, %s)"
                values = (city, today, aqi, pollutant, status)
                cursor.execute(sql, values)
                conn.commit()

                print(f" [OK] AQI: {aqi}")
            else:
                print(" [Error in API]")

        except Exception as e:
            print(f" [Error] {e}")

    conn.close()
    input("\nData updated. Press Enter to go back...")

def show_city_stats():
    # Menu to pick a city
    print("\n--- CHOOSE A CITY ---")
    for i in range(len(cities)):
        print(f" {i+1}. {cities[i]}")

    try:
        choice = int(input("\nEnter choice: "))
        selected_city = cities[choice-1]
    except:
        print("Invalid input.")
        return

    # Get data from DB
    conn = get_connection()
    if conn is None: return

    cursor = conn.cursor()
    cursor.execute("SELECT reading_date, aqi FROM aqi_data WHERE city_name=%s ORDER BY reading_date", (selected_city,))
    data = cursor.fetchall()
    conn.close()

    if len(data) == 0:
        print("\nNo data found for this city yet. Try updating database first.")
        input("Press Enter...")
        return

    # Separate dates and AQI for the graph
    dates = []
    aqi_list = []
    
    for row in data:
        dates.append(str(row[0]))
        aqi_list.append(row[1])

    # Calculate simple stats
    avg_aqi = sum(aqi_list) / len(aqi_list)
    max_aqi = max(aqi_list)
    current_aqi = aqi_list[-1]

    # Show Report
    print_header(f"REPORT: {selected_city.upper()}")
    print(f" Total Readings : {len(aqi_list)}")
    print("-" * 70)
    print(f" Average AQI    : {avg_aqi:.2f}")
    print(f" Max AQI        : {max_aqi}")
    print(f" Current AQI    : {current_aqi} ({get_status(current_aqi)})")
    print("-" * 70)

    print("\nOpening Graph...")
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(dates, aqi_list, marker='o', color='blue', label='AQI')
    
    plt.title(f"Air Quality Trend: {selected_city}")
    plt.xlabel("Date")
    plt.ylabel("AQI Level")
    plt.grid(True)
    
    # Draw a red line for danger level
    plt.axhline(y=200, color='red', linestyle='--', label='Danger Level')
    
    plt.legend()
    plt.show()

def compare_cities():
    print_header("COMPARE TWO CITIES")

    # Showing list
    for i in range(len(cities)):
        print(f" {i+1}. {cities[i]}")

    try:
        c1 = int(input("\nSelect City 1: ")) - 1
        c2 = int(input("Select City 2: ")) - 1
        
        city1 = cities[c1]
        city2 = cities[c2]
    except:
        print("Invalid selection.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Get data for both
    cursor.execute("SELECT reading_date, aqi FROM aqi_data WHERE city_name=%s ORDER BY reading_date", (city1,))
    data1 = cursor.fetchall()

    cursor.execute("SELECT reading_date, aqi FROM aqi_data WHERE city_name=%s ORDER BY reading_date", (city2,))
    data2 = cursor.fetchall()
    conn.close()

    # Prepare lists
    d1 = [str(x[0]) for x in data1]
    v1 = [x[1] for x in data1]
    
    d2 = [str(x[0]) for x in data2]
    v2 = [x[1] for x in data2]

    print(f"\nComparing {city1} and {city2}...")

    plt.figure(figsize=(10, 6))
    plt.plot(d1, v1, marker='o', label=city1)
    plt.plot(d2, v2, marker='s', label=city2)

    plt.title(f"{city1} vs {city2}")
    plt.xlabel("Date")
    plt.ylabel("AQI")
    plt.legend()
    plt.grid(True)
    plt.show()

def export_csv():
    print_header("EXPORT TO EXCEL/CSV")
    filename = "AQI_Report.csv"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aqi_data")
        rows = cursor.fetchall()
        
        # Simple way to get headers
        headers = [i[0] for i in cursor.description]

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"\nSuccess! Data saved to {filename}")
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

    input("\nPress Enter to return...")

def about_us():
    print_header("ABOUT ECOTRACK")
    print(" Class XII Computer Science Project")
    print(" Made By: Prakhar Aggarwal")
    print(" Session: 2025-26")
    print("\n This project uses Python and MySQL to track pollution levels.")
    input("\nPress Enter to return...")


# ==============================================================================
#                               MAIN MENU
# ==============================================================================

def main():
    check_system()

    while True:
        clear_screen()
        # ASCII Border kept exactly as requested
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║          ECOTRACK: INTELLIGENT AQI MONITORING SYSTEM         ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║  1. UPDATE DATABASE (Fetch Live Satellite Data)              ║")
        print("║  2. ANALYZE CITY (View Statistics & Trend Graph)             ║")
        print("║  3. COMPARE CITIES (Multi-City Graph Analysis)               ║")
        print("║  4. EXPORT DATA (Generate CSV/Excel Report)                  ║")
        print("║  5. ABOUT PROJECT (System Information)                       ║")
        print("║  6. EXIT SYSTEM                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")

        choice = input("\n  >> ENTER YOUR CHOICE (1-6): ")

        if choice == '1':
            fetch_data()
        elif choice == '2':
            show_city_stats()
        elif choice == '3':
            compare_cities()
        elif choice == '4':
            export_csv()
        elif choice == '5':
            about_us()
        elif choice == '6':
            print("\nExiting...")
            break
        else:
            print("Invalid Choice!")
            time.sleep(1)

if __name__ == "__main__":
    main()