Food wastage is a significant issue, with many households and restaurants discarding
surplus food while numerous people struggle with food insecurity. This project aims to
develop a Local Food Wastage Management System, where:
● Restaurants and individuals can list surplus food.
● NGOs or individuals in need can claim the food.
● SQL stores available food details and locations.
● A Streamlit app enables interaction, filtering, CRUD operation and visualization.
Business Use Cases
● Connecting surplus food providers to those in need through a structured
platform.
● Reducing food waste by redistributing excess food efficiently.
● Enhancing accessibility via geolocation features to locate food easily.
● Data analysis on food wastage trends for better decision-making.
Approach
1. Data Preparation
● Utilize a provided dataset containing food donation records.
● Ensure consistency and accuracy in data formatting.
2. Database Creation
● Store food availability data in SQL tables.
● Implement CRUD operations for updating, adding, and removing records.
3. Data Analysis.
● Identify food wastage trends based on categories, locations, and expiry dates.
● Generate reports for effective food distribution.
4. Application Development
Develop a Streamlit-based user interface to:
● Display output of the 15 SQL queries .
● Provide filtering options based on city, provider, food type, and meal type.
● Show contact details of providers for direct coordination.
5. Deployment
● Deploy the Streamlit application for accessibility and real-time interaction
Data Flow and Architecture
Data Storage:
● Use SQL database to store food donations, locations, and provider details.
Processing Pipeline:
● Do analysis and generate insights into food wastage patterns.
Deployment:
● Develop a Streamlit-based interface for food providers and seekers
--------------------------------------------------------------------------------------------

Dataset Description
1. Providers Dataset
The providers.csv file contains details of food providers who contribute surplus food to
the system.
● Provider_ID (Integer) – Unique identifier for each provider.
● Name (String) – Name of the food provider (e.g., restaurants, grocery stores,
supermarkets).
● Type (String) – Category of provider (e.g., Restaurant, Grocery Store,
Supermarket).
● Address (String) – Physical address of the provider.
● City (String) – City where the provider is located.
● Contact (String) – Contact information (e.g., phone number).
2. Receivers Dataset
The receivers.csv file contains details of individuals or organizations receiving food.
● Receiver_ID (Integer) – Unique identifier for each receiver.
● Name (String) – Name of the receiver (individual or organization).
● Type (String) – Category of receiver (e.g., NGO, Community Center, Individual).
● City (String) – City where the receiver is located.
● Contact (String) – Contact details (e.g., phone number).
3. Food Listings Dataset
The food_listings.csv file stores details of available food items that can be claimed by
receivers.
● Food_ID (Integer) – Unique identifier for each food item.
● Food_Name (String) – Name of the food item.
● Quantity (Integer) – Quantity available for distribution.
● Expiry_Date (Date) – Expiry date of the food item.
● Provider_ID (Integer) – Reference to the provider offering the food.
● Provider_Type (String) – Type of provider offering the food.
● Location (String) – City where the food is available.
● Food_Type (String) – Category of food (e.g., Vegetarian, Non-Vegetarian, Vegan).
● Meal_Type (String) – Type of meal (e.g., Breakfast, Lunch, Dinner, Snacks).
4. Claims Dataset
The claims.csv file tracks food claims made by receivers.
● Claim_ID (Integer) – Unique identifier for each claim.
● Food_ID (Integer) – Reference to the food item being claimed.
● Receiver_ID (Integer) – Reference to the receiver claiming the food.
● Status (String) – Current status of the claim (e.g., Pending, Completed,
Cancelled).
● Timestamp (Datetime) – Date and time when the claim was made
