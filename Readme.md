# GatorLibrary System

## Table of Contents
- [Project Objective](#project-objective)
- [Setup and Running Instructions](#setup-and-running-instructions)
- [Overview](#overview)
- [Data Structures](#data-structures)
- [Function Prototypes](#function-prototypes)
- [Contact Information](#contact-information)

## Project Objective
The GatorLibrary system is designed to efficiently manage book borrowing operations and overall book management within a library context. Utilizing the Red Black tree data structure for effective management and a binary min-heap for maintaining book reservations, the system aims to streamline the borrowing process and reservation queue for books, ensuring a smooth operation for patrons and library staff.

## Setup and Running Instructions
1. Extract the contents from Harshit_Lohaan.zip and navigate to the extracted folder.
2. Open a terminal in the project folder.
3. Execute the following command to run the system, replacing `<input_file.txt>` with your input file name:
    - For Python 2: `python gatorLibrary.py <input_file.txt>`
    - For Python 3: `python3 gatorLibrary.py <input_file.txt>`
4. The output will be generated in a file named `<input_file>_output_file.txt`.

## Overview
The GatorLibrary system leverages two primary data structures:

1. Red Black Trees: Used for the efficient management of book records, ensuring balanced search, insert, and delete operations.
2. Binary Min-Heaps: Utilized for maintaining a priority queue for book reservations, allowing for orderly and fair processing of reservations.

## Function Prototypes
### Book Class Structure
- BookId: Integer for book ID.
- BookName, AuthorName: Strings for book and author names.
- AvailabilityStatus: Boolean for availability (True = available, False = borrowed).
- BorrowedBy: String for patron ID of the borrower.
- ReservationHeap: List of tuples for reservations.

### Key Functions
- Book management functions: initialize book objects, retrieve book info, add reservations.
- Red-black tree operations: insert, delete, search for books, manage borrow/return processes.
- Reservation system: maintain a priority queue for book reservations, ensuring fair access.

## Contact Information
- Name: Harshit Lohaan
- UFID: 7615-8695
- Email: h.lohaan@gmail.com
- Under the guidance of Dr. Sartaj Sahni.
