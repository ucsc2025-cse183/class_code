# Final project

You will work on the final project in groups.
Use https://canvas.ucsc.edu/courses/82493/pages/final-project-groups to join a group

You must use py4web for serverside. You can use the css library of your choice.
You are not required to use a client-side framework but you can.

Part of your grade includes:
- usability
- code quality
- security / vulnerabilities
- individual contribution to the project (commits)


## Project Option I - Custom Recipe Manager

You will develop a web-based recipe manager that allows users to create, browse, and share recipes. This is a database-driven application that must include user accounts and support for searching and managing shared ingredients and recipes.

### Minimum Requirements (for a passing grade)
Your app must include the following features:

Database Schema:

- A table for ingredients with fields: name, unit, calories_per_unit, description
- A table for recipes with fields: name, type, description, image, author, instruction_steps, servings
- A linking table to connect recipes and ingredients, with fields: recipe_id, ingredient_id, quantity_per_serving

Functionality:

- Ability to search ingredients by name.
- Ability to add new ingredients.
- Ingredients are shared across users and cannot be edited once created.
- Ability to search recipes by name and type.
- All recipes are public.
- Ability to create new recipes.
- Ability to edit recipes authored by the logged-in user only.
- Users cannot edit others' recipes.

Documentation:

- A PDF with instructions and screenshots showing functionality

### Requirements for Full Grade

To earn full credit, your app must include all of the above, plus:

- Import data from TheMealDB API to populate recipes (import only once; the import code must be included).
- A professional, self-documenting, and intuitive user interface.
- A public search API for recipes (JSON format).
- Secure recipe editing logic: only allow authors to modify their own recipes.
- Automatically compute total calories per recipe based on ingredients and quantities.

### Optional Features (for extra credit)

Implementing any of the following will earn you bonus points:
 -Support for multiple images per recipe.
- Ability to search recipes by ingredients (any subset).
- A public search API for ingredients.
- Store additional nutritional info beyond just calories.
- Automatically scale ingredients when changing number of servings.

## Project Option II - Hotel Room Reservation System

You will build a hotel room reservation web application that allows staff (and optionally customers) to manage rooms, bookings, and customer information. This project emphasizes relational data modeling, user roles, and secure access control.

### Minimum Requirements (for a passing grade)

Your app must include the following database tables and features:

Database Schema:

- A table for rooms with fields: number_of_beds, amenities, price_per_night, image
- A table for customers with fields: name, address, phone_number, email, etc.
- A table for reservations with fields: room_id, customer_id, start_date, end_date, notes, total_cost

Functionality:

- Ability to add and edit rooms.
- Ability to search available rooms based on date range and filters.
- Ability to search customers by name or email.
- Ability to add new customers.
- Ability to create and cancel reservations.

Documentation:

- A PDF with instructions and screenshots showing functionality

### Requirements for Full Grade
To earn full credit, your app must also include:

- A visual chart or calendar view showing room availability.
- A customer invoice page, showing reservations and charges.
- Ability for customers to register and view their reservation history (matched by email).

Access control:

- Only managers (staff) can create and modify reservations.
- Customers can view, but not alter, their bookings.
- A public API endpoint to retrieve room information in JSON format.

### Optional Features (for extra credit)

You can earn additional credit by implementing the following features:

- Allow customers to log in and create their own reservations.
- Provide an authenticated API to create reservations using tokens.
- Add support for extra services (e.g. room service, minibar) and include them in invoices.





