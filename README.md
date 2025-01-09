# Project Overview
The Gator Ticket Master project is a reservation and seat allocation system for Gator events. This system uses data structures such as Red-Black Tree and Binary Min-Heap to manage available seats, reserved seats, and a waitlist, allowing efficient seat assignments based on priority and availability.
## Project Architecture and Structure
The program is organized into four main classes, each responsible for specific operations within the system:
•	Red-Black Node: Represents a node within the Red-Black Tree.
•	Red-Black Tree: Manages reservations and provides efficient insertion, deletion, and search capabilities.
•	MinHeap: Manages both available seats and waitlist by priority.
•	GatorTicketMaster: The main class that interfaces with the Red-Black Tree and MinHeap to execute commands for reservation and cancellation.
## Data Flow:
•	Seat Allocation: Seats are assigned from the available_seats MinHeap.
•	Reservation Management: GatorTicketMaster interacts with the Red-Black Tree to maintain reservations.
•	Waitlist Handling: The waitlist MinHeap manages users based on priority, assigning seats as they become available.
