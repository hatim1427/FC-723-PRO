#used to generate random booking references 
import random 
#provides the list of letters and digits for references
import string






#This class represents a single seat on the plane
class Seat:
    
    #sets up the seat with its row and number and starting status
    def __init__(self, row, number, status):        
        self.row = row
        self.number = number
        self.status = status        
    
    
    #return true if the seat is free
    def is_free(self):
        return self.status == "F"    
    
    
    #return true if the seat is allowed to be booked (not an aisle or storage) 
    def is_bookable(self):
        return self.status not in ["X", "S"]
    
    
    def book(self, reference):
        if self.is_free():
            #store the unique 8 char reference instead of "R"
            self.status = reference  
            return True
        return False
   
    
    def free(self):
        #a booked seat now stores a code like "AB12CD78" not just "R"
        #so we check if the status is anything other than F, X or S
        if self.status not in ["F", "X", "S"]:
            self.status = "F"
            return True
        return False
    
    
    def is_booked(self):
        #return True if the seat has a booking code saved in it
        return self.status not in ["F", "X", "S"]
    
    def get_display_status(self):
        #on the seat map we still show R so it easy to read
        #the actual booking code only shows when the user checks that seat
        if self.is_booked():
            return "R"
        return self.status
    
    
    
    #return the seat as a readable string e.g. "25B%
    def get_reference(self):
        return f"{self.number}{self.row}"
    #return just the status letter when the seat is printed
    def __str__(self):
        return self.get_display_status()


#this class represents the whole plane and all its seats    
class Plane:    
    #the order rows appear on screen
    ROW_ORDER = ["A", "B", "C", "X", "D", "E", "F"]
    #the rows that contain storage at positions 77 and 78
    STORAGE_ROWS = ["D", "E", "F"]
    #every row has 80 seats
    TOTAL_COLUMNS = 80
    
    
    #creates the plane and fills it with seat objects
    def __init__(self):
        self.seats = {}
        self.create_seats()
    
    #builds every seat in the plane and gives each one the correct starting status    
    def create_seats(self):
        for row in self.ROW_ORDER:
            self.seats[row] = {}
            for col_index in range(self.TOTAL_COLUMNS):
                
                
                #seat numbers start at 1 but list indexes start at 0
                seat_number = col_index +1
                
                #row X is the aisle
                if row == "X":
                    status = "X"
                
                #seats 77 and 78 in rows D and E and F are storage areas 
                elif row in self.STORAGE_ROWS and seat_number in [77, 78]:
                    status = "S"
                
                #everything alse starts as free
                else:
                    status = "F" 
                
                #creat the seat object and store it
                self.seats[row][col_index] = Seat(row, seat_number, status)
    
    #returns the seat object at the given row and column position
    def get_seat(self, row, col_index):
        return self.seats[row][col_index]
    
    
    #counts how many seats have each status and returns the totals
    def count_seats(self):
        counts = {"F": 0, "R": 0, "S": 0, "X": 0}
        for row in self.ROW_ORDER:
            for col_index in range(self.TOTAL_COLUMNS):
                seat = self.seats[row][col_index]
                if seat.is_booked():                    
                    counts["R"] +=1
                else:
                    counts[seat.status] += 1                     
        return counts
    
    
    def get_all_references(self):
        #goes through every seat and collects all the booking codes in use
        #we need this to make sure any new code we make is not already taken
        refs = set()
        for row in self.ROW_ORDER:
            for col_index in range(self.TOTAL_COLUMNS):
                seat = self.seats[row][col_index]
                if seat.is_booked():
                    refs.add(seat.status)
        return refs
    
    
    #prints the full seat map to the screen with a summary at the bottom
    def display(self):
        print("\n" + "=" * 65)
        print("     APACHE AIRLINES - BURAK757 SEAT MAP")
        print("=" * 65)
        print(" F = Free       R = Reserved     X = Aisle    S = Storage")
        print("-" * 65)
        print("     ", end="")
        
        #print column number headers every 10 seats
        for col in range(1, 81, 10):
            print(f"{col:<10}", end=" ")
        print()
        
        #print each row with all its seat statuses
        for row in self.ROW_ORDER:
            print(f" {row}  ", end="")
            for col_index in range(self.TOTAL_COLUMNS):
                print(self.seats[row][col_index], end=" ")
            print()
        
        #print the seat count summary at the bottom
        counts = self.count_seats()
        print("=" * 65)
        print(f"  Free: {counts['F']}   Reserved: {counts['R']}   "
              f"Storage: {counts['S']}   Aisle: {counts['X']}")
        print("=" * 65)
        

#this class runs the program and handles everything the user does
class BookingSystem:
    
    #the letters and numbers we can use in a booking code: A-Z and 0-9
    REFERENCE_CHARS = string.ascii_uppercase + string.digits
    #every booking code must be exactly 8 characters
    REFERENCE_LENGTH= 8
    
    def __init__(self):
        self.plane = Plane()
        
    def generate_booking_reference(self):
        #get all booking codes already in use
        existing_reverences = self.plane.get_all_references()
        
        while True:
            #pick 8 random characters from A-Z and 0-9
            reference = "".join(
                random.choices(self.REFERENCE_CHARS, k=self.REFERENCE_LENGTH)
            )
            #if this code is not already taken use it
            if reference not in existing_reverences:
                return reference
    
    
    #ask the user to type a seat and checks the format is correct
    #return the column index and row letter if valid or none if not
    def get_seat_input(self):
        seat_input = input("\n Enter seat(e.g. 1A, 25B, 80F):").strip().upper()
        
        
        # must be at least 2 characters e.g. "1A"
        if len(seat_input) < 2:
            print(" ERROR: Invalid format. Use a number followed by a letter (e.g. 25B).")
            return None, None
        
        #last character is the row and the rest is the seat number
        row = seat_input[-1]
        seat_number_str = seat_input[:-1]
        
        #build the list of valid rows (exclude the aisle row X)
        valid_rows = [r for r in Plane.ROW_ORDER if r != "X"]   
        if row not in valid_rows:
            print(f"  ERROR: Row '{row}' is not valid. Choose from A, B, C, D, E or F.")
            return None, None
        
        #check the seat number is actually a number
        if not seat_number_str.isdigit():
            print(" ERROR: Seat number must be a whole number (e.g. 25B).")
            return None, None
        
        seat_number = int(seat_number_str)
        
        #check the seat number is between 1 and 80
        if seat_number < 1 or seat_number > 80:
            print(" ERROR: Seat number must be between 1 and 80.")
            return None, None
        
        #convert to 0 based index for the list
        col_index = seat_number - 1
        return col_index, row
    
    #option 1 checks if a seat is free and tells the user
    def check_availability(self):
        print("\n--- CHECK SEAT AVAILABILITY ---")
        col_index, row = self.get_seat_input()
        if col_index is None:
            return
        
        #get the seat and display its current status
        seat = self.plane.get_seat(row, col_index)
        if seat.is_free():                     
            print(f"\n Seat {seat.get_reference()} is AVAILABLE.")
        elif seat.is_booked():
            print(f"\n Seat {seat.get_reference()} is ALREADY RESERVED.")
            print(f" Booking reference: {seat.status}")
        elif seat.status == "S":
            print(f"\n  Seat {seat.get_reference()} is a STORAGE area - cannot be booked.")
        elif seat.status == "X":
            print(f"\n  Seat {seat.get_reference()} is part of the AISLE - cannot be booked.")
        
    
    #prints the main menu options to the screen 
    def display_menu(self):
        print("\n" + "=" * 40)
        print("    APACHE AIRLINES BOOKING SYSTEM")
        print("=" * 40)
        print("  1. Check availability of seat")
        print("  2. Book a seat")
        print("  3. Free a seat")
        print("  4. Show booking status")
        print("  5. Book multiple seats")
        print("  6. Exit program")
        print("-" * 40)
    
    #reasdt the users menu choice and checks it is a number between 1 and 5
    def get_menu_choice(self):
        choice = input("  Enter your choice (1-6): ").strip()
        
        #check it is a number 
        if not choice.isdigit():
            print("  ERROR: Please enter a number between 1 and 6.")
            return None
        choice = int(choice)
        
        #check it is within range
        if choice < 1 or choice > 6:
            print("  ERROR: Please enter a number between 1 and 6.")
            return None
        return choice
    
    
    #option 2 books a seat if its free
    def book_seat(self):
        print("\n--- BOOK A SEAT ---")
        col_index, row = self.get_seat_input()
        if col_index is None:
             return
        
        seat = self.plane.get_seat(row, col_index)
        
        #stop if the seat is an aisle or storage area
        if not seat.is_bookable():
             print(" ERROR: This seat cannot be booked.")

        elif seat.is_free():
            #make a new unique booking code for this seat
            reference = self.generate_booking_reference()
            seat.book(reference)
            print(f"\n SUCCESS: Seat {seat.get_reference()} has been booked.")
            #show the customer their booking code
            print(f" Your booking reference is: {reference}")

        #book() returns False if the seat was already reserved 
        else:
            print(f"\n ERROR: Seat {seat.get_reference()} is already reserved.")
    
    
    #starts the program and keeps the menu running until the user exists
    def run(self):
        print("\n Welcome to the Apache Airlines Booking System")
        print(" Initialising Burak757 seating plan...\n")
        
        #keep showing the menu until the user picks option 5 
        running = True
        while running:
            self.display_menu()
            choice = self.get_menu_choice()
            
            #if the input was invalid it shows the menu again
            if choice is None:
                continue
            
            #send the user to the right method based on their choice
            if choice == 1:
                self.check_availability()
            elif choice == 2:
                self.book_seat()
            elif choice == 3:
                self.free_seat()
            elif choice == 4:
                self.show_booking_status()
            elif choice == 5:
                self.book_multiple_seats()
            elif choice == 6:
                print("\n  Thank you for using Apache Airlines Booking System.")
                print("  Goodbye!\n")
                running = False
    
    #option 3 frees a seat that was previously booked
    def free_seat(self):
        print("\n--- FREE A SEAT ---")
        col_index, row = self.get_seat_input()
        if col_index is None:
            return
        
        seat = self.plane.get_seat(row, col_index)

        #stop if the seat is an aisle or storage area
        if not seat.is_bookable():           
            print(f"\n ERROR: Seat {seat.get_reference()} cannot be modified.")
        
        #try to free free() returns true if its worked
        elif seat.free():                    
            print(f"\n SUCCESS: Seat {seat.get_reference()} is now free.")
        
        #free() returns False if the seat was not reserved
        else:
            print(f"\n ERROR: Seat {seat.get_reference()} was not reserved.")
                   
    #option 4 shows the full seat map on screen
    def show_booking_status(self):
         self.plane.display()



    def book_multiple_seats(self):
        #Additional feature that allows the user to book several seats
        #All seats are validated first - if any unavailable none are booked
        print("\n--- BOOK MULTIPLE SEATS ---")
        count_input = input("\n How many seats would you like to book?").strip()
        
        #Validate the number entered is positive integer
        if not count_input.isdigit() or int(count_input) < 1:
            print(" ERROR: Please enter a valid number of seats (e.g. 2).")
            return
        
        count = int(count_input)
        seats_to_book = []
        
        #collect and validate each seat before booking any
        print(f"\n Enter {count} seat(s) one at a time:")
        for i in range(count):
            print(f"\n Seat {i + 1} of {count}:")
            col_index, row = self.get_seat_input()
            if col_index is None:
                print(" Booking cancelled due to invalid seat entry.")
                return
            seat = self.plane.get_seat(row, col_index)
            
            #check the seat can be booked
            if not seat.is_bookable():
                kind = "an aisle" if seat.status == "X" else "a storage area"
                print(f" ERROR: Seat {seat.get_reference()} is {kind} - booking cancelled.")
                return
            
            if not seat.is_free():
                print(f"   ERROR: Seat {seat.get_reference()} is already reserved - booking cancelled")
                return
            #Check for duplicate antries in this request
            if(col_index, row) in [(s[0], s[1]) for s in seats_to_book]:
                print(f"  ERROR: Seat {seat.get_reference()} entered twice — booking cancelled.")
                return
            
            seats_to_book.append((col_index, row, seat))
            
        #all seats are valid and free - now book them all
        print("\n  All seats available. Booking now...")
        for col_index, row, seat in seats_to_book:
            #make a seperate booking code for each seat
            reference = self.generate_booking_reference()
            seat.book(reference)
            print(f"  SUCCESS: Seat {seat.get_reference()} booked - reference: {reference}")

        print(f"\n  {count} seat(s) successfully booked.")



#starts the program by creating a BookingSystem and calling run()
if __name__ == "__main__":
    system = BookingSystem()
    system.run()
            
        
        
                
                     
                 
                    
                
        
            
      
        
        
        
    
    