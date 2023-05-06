# Description
This my implementation to the final project of  [API'S](https://www.coursera.org/learn/apis) course from [Meta Back-End Developer Professional Certificate](https://www.coursera.org/professional-certificates/meta-back-end-developer#courses) Using [Django REST FrameWork](https://www.django-rest-framework.org/)

### Preview


https://user-images.githubusercontent.com/67506662/236642931-f0ed118d-edf7-49c4-8dda-ce96968a2c20.mp4



# Installing / Getting started (Unix)


### Prerequisites

```shell
pip install -r requirements.txt
```


### Setting up Dev

- Create folder for project
```shell
mkdir <name-for-project>
cd <name-for-project>
```
- Inside created foleder create virtual enviroment
```shell
python -m venv <virtual enviroment name>
```
- clone  project to this folder
``` shell
git clone https://github.com/mostafanasser2000/RestaurantAPI.git
```
- activate eniviroment
```shell
source <virtual enviroment name>/bin/activate
```
- Install requirments
```shell
pip install -r requirements.txt
```
- Open project folder with any IDE
- run this commands
``` shell
python manage.py makemigrations
python manage.py migrate
```
- create super user (Admin)
```shell
python manage.py createsuperuser
```
- run development server
```shell
python manage.py runserver
```


# End Points


### User registration and token generation endpoints

| Endpoint                 | Role                                      | Method   | Purpose                                                                     |
| ------------------------ | ----------------------------------------- | -------- | --------------------------------------------------------------------------- |
| __/api__                 | No role required                          | __GET__  | display all end points                                                      |
| __/api/users__           | No role required                          | __POST__ | Creates a new user with name, email and password                            |
| __/api/users/users/me/__ | Anyone with a valid user token            | __GET__  | Displays only the current user                                              |
| __/auth/token/login/__   | Anyone with a valid username and password | __POST__ | Generates access tokens that can be used in other API calls in this project |


### Menu-items endpoints

| Endpoint                         | Role                    | Method                       | Purpose                                                           |
| -------------------------------- | ----------------------- | ---------------------------- | ----------------------------------------------------------------- |
| __/api/menu-items__              | Customer, delivery crew | __GET__                      | Lists all menu items. Return a __200 – Ok__ HTTP status code      |
| __/api/menu-items__              | Customer, delivery crew | __POST, PUT, PATCH, DELETE__ | Denies access and returns __403 – Unauthorized__ HTTP status code |
| __/api/menu-items__              | Manager                 | __GET__                      | Lists all menu items                                              |
| __/api/menu-items__              | Admin                   | __POST__                     | Creates a new menu item and returns 201 - Created                 |
| __/api/menu-items/{menuItemID}__ | Manager                 | __GET__                      | Lists single menu item                                            |
| __/api/menu-items/{menuItemID}__ | Manager                 | __PUT, PATCH__               | Updates single menu item                                          |
| __/api/menu-items/{menuItemID}__ | Manager                 | __DELETE__                   | Deletes menu item                                                 |


### User group management endpoints

| Endpoint                                     | Role    | Method     | Purpose                                                                                                                                                        |
| -------------------------------------------- | ------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| __/api/groups/manager/users__                | Admin   | __GET__    | Returns all managers                                                                                                                                           |
| __/api/groups/manager/users__                | Admin   | __POST__   | Assigns the user in the payload to the manager group and returns __201-Created__                                                                               |
| __/api/groups/manager/users/{userId}__       | Admin   | __DELETE__ | Removes this particular user from the manager group and returns __200 – Success__ if everything is okay. If the user is not found, returns __404 – Not found__ |
| __/api/groups/delivery-crew/users__          | Manager | __GET__    | Returns all delivery crew                                                                                                                                      |
| __/api/groups/delivery-crew/users__          | Manager | __POST__   | Assigns the user in the payload to delivery crew group and returns __201-Created HTTP__                                                                        |  |
| __/api/groups/delivery-crew/users/{userId}__ | Manager | __DELETE__ | Removes this user from the manager group and returns __200 – Success__ if everything is okay.If the user is not found, returns  __404 – Not found__            |


### Cart management endpoints 

| Endpoint                            | Role     | Method     | Purpose                                                                                         |
| ----------------------------------- | -------- | ---------- | ----------------------------------------------------------------------------------------------- |
| __/api/cart/menu-items__            | Customer | __GET__    | Returns current items in the cart for the current user token                                    |
| __/api/cart/menu-items/{menuitem}__ | Customer | __GET__    | Returns sinfle item in the cart for the current user token                                      |
| __/api/cart/menu-items__            | Customer | __POST__   | Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items |
| __/api/cart/menu-items__            | Customer | __DELETE__ | Deletes all menu items created by the current user token                                        |


### Order management endpoints

| Endpoint                  | Role          | Method         | Purpose                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------- | ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| __/api/orders__           | Customer      | __GET__        | Returns all orders with order items created by this user                                                                                                                                                                                                                                                                                                                                                  |
| __/api/orders__           | Customer      | __POST__       | Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user.                                                                                                                                                                                                         |
| __/api/orders/{orderId}__ | Customer      | __GET__        | Returns all items for this order id. If the order ID doesn’t belong to the current user, Returns. returns __403 – Unauthorized__                                                                                                                                                                                                                                                                          |
| __/api/orders__           | Manager       | __GET__        | Returns all orders with order items by all users                                                                                                                                                                                                                                                                                                                                                          |
| __/api/orders/{orderId}__ | Manager       | __PUT, PATCH__ | Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0  or 1.                                                     If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery.If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered. |
| __/api/orders/{orderId}__ | Manager       | __DELETE__     | Deletes this order                                                                                                                                                                                                                                                                                                                                                                                        |
| __/api/orders/{orderId}__ | Delivery crew | __PATCH__      | A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order.                                                                                                                                                                                                                                                     |



