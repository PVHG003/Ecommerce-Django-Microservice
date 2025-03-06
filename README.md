﻿# Ecommerce-Django-Microservice


- create your own .env file in root directory
```
# this should be the same in the compose.yml file
JWT_SECRET=example

# MySQL Configuration (Customer Service)
MYSQL_ROOT_PASSWORD=example
MYSQL_DB_NAME=example
MYSQL_USER=example
MYSQL_PASSWORD=example
MYSQL_HOST=example
MYSQL_PORT=example

# MongoDB Configuration (Product Service)
MONGO_INITDB_ROOT_USERNAME=example
MONGO_INITDB_ROOT_PASSWORD=example
MONGO_DB_NAME=example
MONGO_HOST=example
MONGO_PORT=example

# PostgreSQL Configuration (Cart, Order, Payment, Shipping Service)
POSTGRES_USER=example
POSTGRES_PASSWORD=example
POSTGRES_HOST=example
POSTGRES_PORT=example

POSTGRES_CART_DB=example
POSTGRES_ORDER_DB=example
POSTGRES_SHIPPING_DB=example
POSTGRES_PAYMENT_DB=example

# PostgreSQL Connection Strings
POSTGRES_CART_URI=example
POSTGRES_ORDER_URI=example
POSTGRES_SHIPPING_URI=example
POSTGRES_PAYMENT_URI=example


# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=example
CLOUDINARY_API_KEY=example
CLOUDINARY_API_SECRET=example
```

- Run 
``` bash
    docker-compose up --build -d 
```

