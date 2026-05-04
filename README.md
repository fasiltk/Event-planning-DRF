# 🎉 Event Planning & Management System (DRF + Session Based)

## 📌 Project Overview

This is a **Django REST Framework (DRF)** based backend project for an **Event Planning & Management System**.

The system connects:

* Event Organizers
* Customers
* Vendors

It allows users to **create events, book seats, and manage service requests** in a simple and structured way.

> ⚠️ Note: This project uses **custom session-based authentication** (no default Django User model, no JWT).

---

## 🚀 Key Features

* Custom Authentication (No default User model)
* Role-based system (Organizer, Customer, Vendor)
* Event creation & management
* Seat booking system with validation
* Vendor service request system
* Session-based login/logout

---

## 👥 Roles & Responsibilities

---

### 🧑‍💼 Organizer

* Register & login
* Create events
* Update / delete events
* View bookings for their events
* View vendor requests
* Accept / reject vendor requests

---

### 👤 Customer

* Register & login
* View all events
* Book seats for events
* View their bookings
* Cancel bookings

---

### 🧑‍🔧 Vendor

* Register & login
* View events
* Send service requests (catering, photography, etc.)
* View their requests
* Track request status (pending / accepted / rejected)

---

## 🔄 System Flow

1. User registers based on role
2. User logs in → session created
3. Organizer creates events
4. Customer books seats
5. Vendor sends service requests
6. Organizer manages:

   * bookings
   * vendor requests

---

## 🔐 Authentication

* Session-based authentication
* Email stored in session after login
* All APIs manually check session

---

# 🧪 API ENDPOINTS & TEST DATA

---

## 🔹 AUTHENTICATION

### Register

```http
POST /api/auth/register/
```

```json
{
  "name": "Fasil",
  "email": "fasil@gmail.com",
  "password": "123",
  "role": "organizer"
}
```

---

### Login

```http
POST /api/auth/login/
```

```json
{
  "email": "fasil@gmail.com",
  "password": "123"
}
```

---

### Logout

```http
POST /api/auth/logout/
```

---

### Profile

```http
GET /api/auth/profile/
```

---

# 🎯 EVENT MODULE

---

### Create Event (Organizer)

```http
POST /api/event/create/
```

```json
{
  "title": "Music Show",
  "description": "Live concert",
  "location": "Kochi",
  "date": "2026-07-10",
  "time": "18:00:00",
  "total_seats": 200
}
```

---

### My Events

```http
GET /api/event/my-events/
```

---

### All Events

```http
GET /api/event/all/
```

---

### Event Detail

```http
GET /api/event/detail/1/
```

---

### Update Event

```http
PUT /api/event/update/1/
```

```json
{
  "title": "Updated Event"
}
```

---

### Delete Event

```http
DELETE /api/event/delete/1/
```

---

# 🎟️ BOOKING MODULE

---

### Book Seats (Customer)

```http
POST /api/booking/book/
```

```json
{
  "event": 1,
  "number_of_seats": 2
}
```

---

### My Bookings

```http
GET /api/booking/my-bookings/
```

---

### Cancel Booking

```http
POST /api/booking/cancel/1/
```

---

### Event Bookings (Organizer)

```http
GET /api/booking/event-bookings/1/
```

---

# 🛠️ VENDOR MODULE

---

### Send Request (Vendor)

```http
POST /api/vendor/send/
```

```json
{
  "event": 1,
  "service_type": "Catering",
  "description": "Full food service"
}
```

---

### My Requests

```http
GET /api/vendor/my-requests/
```

---

### Event Requests (Organizer)

```http
GET /api/vendor/event-requests/1/
```

---

### Update Request Status (Organizer)

```http
POST /api/vendor/update-status/1/
```

```json
{
  "status": "accepted"
}
```

---

# 🧪 SAMPLE USERS

| Role      | Email                                       | Password |
| --------- | ------------------------------------------- | -------- |
| Organizer | [fasil@gmail.com](mailto:fasil@gmail.com)   | 123      |
| Customer  | [rahul@gmail.com](mailto:rahul@gmail.com)   | 123      |
| Vendor    | [vishnu@gmail.com](mailto:vishnu@gmail.com) | 123      |

---

# ⚙️ Tech Stack

* Python 🐍
* Django
* Django REST Framework
* SQLite (default)

---

# 🚀 Future Enhancements

* Payment integration 💳
* Notification system 🔔
* Chat between users 💬
* Admin dashboard 📊
* Event analytics

---

# 📌 Conclusion

This project demonstrates:

* Custom authentication design
* Role-based API architecture
* Real-world business logic implementation

---

🔥 Built for learning & real-world backend development.
