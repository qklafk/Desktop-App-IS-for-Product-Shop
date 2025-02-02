
# Desktop-App-IS-for-Product-Shop  

🛍 **A desktop application for product shop management.**  

## 📂 Project Functionality  

- On the first launch, the application creates a `products_and_users.db` file.  
- The database initially contains only user data, while products are stored in a dictionary and will be cleared upon restarting the program.  
- The main window includes buttons:  
  - **Login** – Opens a login menu where users enter their credentials (name, password) and access the system based on their assigned role.  
  - **Register** – Allows new users to sign up.  
  - **Exit** – Closes the application.  
- **User Roles:**  
  - **Administrator** – Manages users and products.  
  - **Moderator** – Manages products.  
  - **User** – Views product information and filters products by specific criteria.  

## 📦 Dependencies  

The application uses the following Python library:  

```
sqlite3
```
