

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
