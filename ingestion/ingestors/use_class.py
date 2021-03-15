generic_use_classes = [
    "FoodBev",
    "ShopOfficeSvc",
    "Education",
    "SportsRec",
    "Accommodation",
    "IndRelatedUse",
    "CommunityRelatedUse",
    "ReligiousUse"
]

specific_use_class_map = {
    "Restaurant": "FoodBev",
    "Bar/Pub": "FoodBev",
    "Restaurant and Bar": "FoodBev",
    "Nightclub": "FoodBev",
    "Shop": "ShopOfficeSvc",
    "Laundromat": "ShopOfficeSvc",
    "Office": "ShopOfficeSvc",
    "Massage Establishment": "ShopOfficeSvc",
    "Medical Clinic": "ShopOfficeSvc",
    "Pet Shop": "ShopOfficeSvc",
    "Pet Boarding": "ShopOfficeSvc",
    "Commercial School": "Education",
    "Childcare Centre": "Education",
    "Fitness Centre": "SportsRec",
    "Amusement Centre": "SportsRec",
    "Residential": "Accommodation",
    "Backpacker Hostel": "Accommodation",
    "Hotel": "Accommodation",
    "Student Hostel": "Accommodation",
    "Service Apartment": "Accommodation",
    "Worker Dorm": "Accommodation",
    "Light Industrial Use": "IndRelatedUse",
    "General Industrial Use": "IndRelatedUse",
    "Industrial Training": "IndRelatedUse",
    "Warehouse": "IndRelatedUse",
    "Industrial Canteen": "IndRelatedUse",
    "Showroom": "IndRelatedUse",
    "E-Business": "IndRelatedUse",
    "Core Media Activities": "IndRelatedUse",
    "Association/Community Club/Family Service Centre": "CommunityRelatedUse",
    "Religious Activities": "ReligiousUse",
    "Limited & Non-Exclusive Religious Use": "ReligiousUse",
}

use_class_details = {
    "Restaurant": {
        "definition": "Restaurants are premises primarily used for sale of food "
                      "for consumption at the premises without performance of live music, or live entertainment. "
                      "The sale of liquor and alcoholic drinks, if any, is for consumption on the premises "
                      "and incidental to the consumption of food",
        "requirements": "The premises should have sufficient parking space and "
                        "proper sound proofing measures to reduce noise disturbances",
        "examples": ["Coffee Shop", "Eating House", "Snack Bar", "Cafeteria", "Food Court", "Fast-food Restaurant"]
    },
    "Bar/Pub": {
        "definition": "Bars/Pubs are premises primarily used for the sale of alcoholic drinks for consumption on the premises "
                      "without dancing, singing or performance of live music or live entertainment.",
        "requirements": "The premises should have proper sound proofing measures to reduce noise disturbances.",
        "examples": [],
    },
    "Shop": {
        "definition": "Shops are premises used for any trade or business "
                      "where its primary purpose is the sale of goods or foodstuff by retail or provision of services.",
        "requirements": "",
        "examples": {
            "Retail Shop": ["Departmental Store", "Supermarket", "Provision Shop", "Minimart", "Pawnshop",
                     "Fashion Boutique", "Florist", "Gift Shop", "Furniture Shop"
                     ],
            "Service": ["Barber Shop", "Beauty Salon", "Photo Studio", "Tailor Shop",
                     "Foot Reflexology", "Travel Agency", "Money Changer", "Acupuncturist"
                     ],
            "Takeaway Foodshop": ["Pastry Shop", "Bubble Tea Shop", "Bakery", "Ice Cream Shop"]
        }
    },
    "Amusement Centre": {
        "definition": "Amusement Centres are premises with game machines (e.g. jackpot machines, pin-bill machines, darts machines) for entertainment.",
        "requirements": "In addition to URA’s planning permission, business operators are required to obtain "
                        "a Public Entertainment (PE) Licence from the Police Licensing and Regulatory Department (PLRD) "
                        "before committing to a tenancy agreement or starting the renovation works.",
        "examples": ["Arcade Centre", "Computer Gaming Centre", "Billiard Centre", "Bowling Alley", "Darts Club"],
    },
    "Massage Establishment": {
        "definition": "Massage establishments are premises used for massage or spa services licenced by the Police.",
        "requirements": "In addition to URA’s planning permission, business operators are required to obtain "
                        "a Massage Establishment (ME) Licence from the Police Licensing and Regulatory Department (PLRD) "
                        "before committing to a tenancy agreement or starting the renovation works.",
    }
}