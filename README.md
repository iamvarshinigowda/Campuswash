CAMPUS WASH POINT-Laundry Management System

Overview

The Laundry Management System is designed to streamline laundry services for both users and admins. The project includes functionalities for managing user registrations, memberships, laundry orders, feedback, and additional services. Admins can manage users and track the system's overall performance.

Features

User Page

Sign Up: New users can register on the platform.

Login: Existing users can log in to access their account.

Membership: Users must take a membership to access the laundry order page.

Membership options: 6 months or 12 months.

Users without a membership will be redirected to the membership page.

Laundry Orders:

Users can place up to 2 laundry orders per week.

Users can track the status of their orders.

Extra Services:

Users can avail of additional services multiple times.

Feedback:

Users can submit feedback multiple times.

Admin Page

View Statistics:

Total registered users.

Total number of laundry orders.

Total memberships taken.

Pending laundry orders (orders with no updated status).

User Management:

Create a new user.

Reset user password.

Delete a user.

Laundry Order Management:

View all laundry orders.

Add new laundry orders.

Remove laundry orders.

Update the status of laundry orders.

Once the admin updates the status, users will be notified via email.

Functionalities

Membership Enforcement: Users must have an active membership to access laundry order services.

Email Notifications: Users receive email updates regarding their laundry order statuses.

Weekly Order Limit: Users are restricted to 2 laundry orders per week.

Multiple Extra Services and Feedback: Users can repeatedly access extra services and submit feedback.

Admin Control Panel: Admins have full control over user management and laundry service operations.

Pending Orders Management: Admins can track and update the status of pending laundry orders.

Unique Features

Users receive email notifications for updates on their laundry order statuses.

Additional services can be availed multiple times by users.

db.createCollection("hospital", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["hospital_id", "date", "age", "blood_group", "name"],
      properties: {
        hospital_id: {
          bsonType: "string",
          description: "Hospital ID must be exactly 6 alphanumeric characters",
          pattern: "^[a-zA-Z0-9]{6}$"
        },
        date: {
          bsonType: "string",
          description: "Date must be in YYYY-MM-DD format",
          pattern: "^\\d{4}-\\d{2}-\\d{2}$"
        },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 120,
          description: "Age must be an integer between 0 and 120"
        },
        blood_group: {
          bsonType: "string",
          enum: ["A+", "B+", "B-", "AB+", "AB-", "O+", "O-"],
          description: "Blood group must be one of A+, B+, B-, AB+, AB-, O+, O-"
        },
        name: {
          bsonType: "string",
          minLength: 3,
          description: "Name must be at least 3 characters long"
        }
      }
    }
  }
});
