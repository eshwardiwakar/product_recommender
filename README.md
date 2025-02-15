#  Product Recommender System - Django

## Problem Statement
The goal of this project is to design and implement a **Product Recommender System** that suggests products frequently bought together or relevant to each other based on **historical sales data** and **product similarities**.

###  Features:
- **Products Management**: CRUD APIs to create, update, delete, and fetch product details.
- **Order Management**: CRUD APIs to create and manage orders.
- **Recommendation Engine**: Suggests frequently bought together products using past order data.
- **Live API Deployment**: Hosted on a cloud platform with Docker support.

---

## Solution Approach

### **1️⃣ Data Modeling**
- **Product Model**: Stores product details (name, description, price).
- **Order Model**: Stores purchased products in each order (Many-to-Many relationship).

### **2️⃣ Recommendation Algorithm**
- The system **analyzes past orders** to find products that are frequently purchased together.
- Uses **order co-occurrence analysis** (counting products appearing together in the same orders).
- Returns the **top 5 most frequently bought together products**.

### **3️⃣ API Endpoints**
| **Method** | **Endpoint** | **Description** |
|-----------|------------|----------------|
| **POST** | `/api/products/` | Add a new product |
| **GET** | `/api/products/` | Get all products |
| **GET** | `/api/products/{id}/` | Get a product by ID |
| **PUT** | `/api/products/{id}/` | Update a product |
| **DELETE** | `/api/products/{id}/` | Delete a product |
| **POST** | `/api/orders/` | Create a new order |
| **GET** | `/api/orders/` | Get all orders |
| **GET** | `/api/recommender/recommend/{product_id}/` | Get recommended products |





### **Clone the Repository**
```sh
git clone https://github.com/eshwardiwakar/product_recommender.git
cd product_recommender
