import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

#ici en evite que les valeurs nane peut etre  string mais en change  rend à origin
df = pd.read_csv("data/dataset.csv", na_values=['NaN', 'NaN ', 'null', 'NULL', 'None', ' ', 'N/A'],skipinitialspace=True)
df = df.drop(
    ["ID", "Delivery_person_ID", "Delivery_person_Age","Delivery_person_Ratings","Vehicle_condition","Festival"
     ],
    axis=1
)
print(df.isna().sum())
#evite les espaces dans mots
for col in df.select_dtypes(include="object"):
    df[col]=df[col].str.strip()
#eviter les valeurs parasite comm min
df["Time_taken(min)"]=df['Time_taken(min)'].str.replace("(min)","",regex=False)
df["Weatherconditions"]=df['Weatherconditions'].str.replace("conditions","",regex=False)
val_num=["Time_taken(min)","Restaurant_latitude","Restaurant_longitude","Delivery_location_latitude","Delivery_location_longitude","multiple_deliveries"]

for col in val_num:
    df[col]=pd.to_numeric(df[col],errors="coerce")
df["Order_Date"] = pd.to_datetime(df["Order_Date"],  dayfirst=True,errors="coerce").dt.date
df["Time_Orderd"] = pd.to_datetime(
    df["Time_Orderd"],
    format="%H:%M:%S",
    errors="coerce"
)

df["Time_Order_picked"] = pd.to_datetime(
    df["Time_Order_picked"],
    format="%H:%M:%S",
    errors="coerce"
)


# print(df["Time_taken(min)"].head())

df['multiple_deliveries']=df['multiple_deliveries'].astype('Int64')


gps_cols = [
    "Restaurant_latitude",
    "Restaurant_longitude",
    "Delivery_location_latitude",
    "Delivery_location_longitude"
]
print("les nombre des valeurs is nul en latitude et longitude",df[gps_cols].isna().sum())


invalid = (
    (df["Restaurant_latitude"].abs() > 90) |
    (df["Restaurant_longitude"].abs() > 180) |
    (df["Delivery_location_latitude"].abs() > 90) |
    (df["Delivery_location_longitude"].abs() > 180)
)

print("\n=== COORDONNÉES INVALIDES ===")
print("Nombre des colonene latitude et longitude sont invalid :", invalid.sum())

df.loc[invalid,gps_cols]=pd.NA


zero_restaurant = (
    (df["Restaurant_latitude"] == 0) &
    (df["Restaurant_longitude"] == 0)
)
zero_client=(df['Delivery_location_latitude']==0)&(df["Delivery_location_longitude"]==0)
print("nombre de zero geographique client",zero_client.sum(),"PourRestaurant",zero_restaurant.sum())
# Si restaurant = (0, 0)
df.loc[
    zero_restaurant,
    ["Restaurant_latitude", "Restaurant_longitude"]
] = pd.NA

# Si client = (0, 0)
df.loc[
    zero_client,
    ["Delivery_location_latitude", "Delivery_location_longitude"]
] = pd.NA


negative = (
    (df["Restaurant_latitude"] < 0) |
    (df["Restaurant_longitude"] < 0) |
    (df["Delivery_location_latitude"] < 0) |
    (df["Delivery_location_longitude"] < 0)
)
print("\n=== COORDONNÉES NÉGATIVES ===")
print("Nombre de lignes  :", negative.sum())

gps_columns = [
    "Restaurant_latitude",
    "Restaurant_longitude",
    "Delivery_location_latitude",
    "Delivery_location_longitude"
]
#transforme les value negatif en value  positif
df[gps_columns] = df[gps_columns].abs()




#had funvtvion drnaha bach nkhaliw limachii Nan hit dej afach l9ina values machi normale raja3nahom nan


def calcule_distance(row):

    restaurant = (
        row['Restaurant_latitude'],
        row['Restaurant_longitude']
    )

    client = (
        row['Delivery_location_latitude'],
        row['Delivery_location_longitude']
    )

    return geodesic(restaurant, client).km




gps_complete = df[gps_cols].notna().all(axis=1)

print("\n=== GPS COMPLET ===")
print("Lignes avec GPS complet :", gps_complete.sum())
# print("Lignes avec GPS incomplet :", (~gps_complete).sum())


df["distance_KM"] = pd.NA

df.loc[gps_complete, "distance_KM"] = (
    df.loc[gps_complete]
    .apply(calcule_distance, axis=1)
)


# Convertir en numérique
df["distance_KM"] = pd.to_numeric(
    df["distance_KM"],
    errors="coerce"
)
print("\n=== STATISTIQUES DISTANCE ===")

print(df["distance_KM"].describe())








# # print(df["Time_Orderd"].head(10))

# print("Time_ordres",df["Time_Orderd"].isna().sum())

# print("Date",df["Order_Date"].isna().sum())
# print("Time_Order_picked",df["Time_Order_picked"].isna().sum())
# #diagramme pour determiner les  quel pourcentage de valeur manquante
# missing_percent = df.isnull().mean() * 100

# plt.figure(figsize=(12, 6))

# missing_percent.plot(kind="bar")

# plt.axhline(y=50, linestyle="--")

# plt.title("Pourcentage de valeurs manquantes par colonne")
# plt.xlabel("Colonnes")
# plt.ylabel("Pourcentage (%)")

# plt.xticks(rotation=45)
# plt.tight_layout()

# plt.savefig("data/missing_values.png")
# plt.close()


# #diagramme dterminer outlieres
# df[val_num].boxplot(figsize=(12, 6))
# plt.xticks(rotation=45)
# plt.title("Détection des outliers")

# plt.tight_layout()
# plt.savefig("data/outliers.png")
# plt.close()

nb_manquants = df["Time_Orderd"].isna().sum()
total_lignes = len(df)


nb_manquants = df["Time_Orderd"].isna().sum()
total_lignes = len(df)
pourcentage_time_odrder = df['Time_Orderd'].isna().mean() * 100
pourcentage_restaunrant_latitude=df['Restaurant_latitude'].isna().mean() * 100
pourcentage_restaunrant_longitude=df['Restaurant_longitude'].isna().mean() * 100
pourcentage_client_latitude=df['Delivery_location_latitude'].isna().mean() * 100
pourcentage_client_longitude=df['Delivery_location_latitude'].isna().mean() * 100
print(f"Nombre de valeurs manquantes : {nb_manquants} sur {total_lignes}")
print(f"Pourcentage de valeurs manquantes : {pourcentage_time_odrder:.1f}%")
print(f"Pourcentage de valeurs restaurant manquantes : {pourcentage_restaunrant_latitude:.1f}%")
print(f"Pourcentage de valeurs  restaurant manquantes : {pourcentage_restaunrant_longitude:.1f}%")
print(f"Pourcentage de valeurs client manquantes : {pourcentage_client_latitude:.1f}%")
print(f"Pourcentage de valeurs client manquantes : {pourcentage_client_longitude:.1f}%")


df = df.dropna(
    subset=["Restaurant_latitude", "Restaurant_longitude","Delivery_location_latitude","Delivery_location_longitude","Time_Orderd"]
)



df["Road_traffic_density"]=df["Road_traffic_density"].fillna(df["Road_traffic_density"].mode()[0])



mode_val = df['multiple_deliveries'].mode()[0]

df['multiple_deliveries'] = df['multiple_deliveries'].fillna(mode_val)

df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)






















