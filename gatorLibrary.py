import sys
import time

class Book:
    def __init__(self, BookId=0, BookName="", AuthorName="", AvailabilityStatus=True, BorrowedBy=None):
        """
        Initialize a Book object with the given attributes.
        
        Parameters:
        - BookId (int): The ID of the book.
        - BookName (str): The name of the book.
        - AuthorName (str): The name of the author of the book.
        - AvailabilityStatus (bool): The availability status of the book.
        - BorrowedBy (str): The ID of the patron who borrowed the book.
        """
        self.BookId = int(BookId)
        self.BookName = BookName 
        self.AuthorName = AuthorName
        self.AvailabilityStatus = AvailabilityStatus
        self.BorrowedBy = BorrowedBy
        self.ReservationHeap = []

    def __str__(self):
        """
        Return a string representation of the Book object.
        """
        return f"BookID = {self.BookId}\nTitle = \"{self.BookName}\"\nAuthor = \"{self.AuthorName}\"\n" \
               f"Availability = \"{'Yes' if self.AvailabilityStatus else 'No'}\"\n" \
               f"BorrowedBy = {self.BorrowedBy if self.AvailabilityStatus is False else 'None'}\n" \
               f"Reservations = {self.get_reservation_list()}\n\n"

    def get_reservation_list(self):
        """
        Return a list of patron IDs who have reserved the book.
        """
        return [reservation[0] for reservation in self.ReservationHeap]

    def add_reservation(self, patron_id, priority_number, time_of_reservation):
        """
        Add a reservation for the book with the given patron ID, priority number, and time of reservation.
        
        Parameters:
        - patron_id (str): The ID of the patron making the reservation.
        - priority_number (int): The priority number of the reservation.
        - time_of_reservation (datetime): The time of the reservation.
        """
        reservation = (patron_id, priority_number, time_of_reservation)
        self.ReservationHeap.append(reservation)
        self._heapify_up()

    def _heapify_up(self):
        """
        Perform heapify up operation to maintain the heap property of the reservation heap.
        """
        index = len(self.ReservationHeap) - 1
        while index > 0:
            parent_index = (index - 1) // 2
            if self._compare_reservations(index, parent_index) < 0:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _compare_reservations(self, index1, index2):
        """
        Compare two reservations based on priority number and time of reservation.
        
        Parameters:
        - index1 (int): The index of the first reservation in the heap.
        - index2 (int): The index of the second reservation in the heap.
        
        Returns:
        - int: -1 if the first reservation has higher priority, 1 if the second reservation has higher priority, 0 if they have the same priority.
        """
        patron_id1, priority_number1, time_of_reservation1 = self.ReservationHeap[index1]
        patron_id2, priority_number2, time_of_reservation2 = self.ReservationHeap[index2]

        if priority_number1 < priority_number2 or (priority_number1 == priority_number2 and time_of_reservation1 > time_of_reservation2):
            return -1
        elif priority_number1 > priority_number2 or (priority_number1 == priority_number2 and time_of_reservation1 < time_of_reservation2):
            return 1
        else:
            return 0

    def _swap(self, index1, index2):
        """
        Swap two reservations in the reservation heap.
        
        Parameters:
        - index1 (int): The index of the first reservation.
        - index2 (int): The index of the second reservation.
        """
        self.ReservationHeap[index1], self.ReservationHeap[index2] = self.ReservationHeap[index2], self.ReservationHeap[index1]

class RBTreeNode:
    def __init__(self, book):
        self.book = book
        self.color = "RED"
        self.left = None
        self.right = None
        self.parent = None
        self.colorChangingFunctionId=0
        

class RedBlackTree:
    def __init__(self):
        """
        Initializes a Red-Black Tree with a NULL node as the root and sets the initial values for color_flip_count and currentFunctionId.
        """
        self.NULL = RBTreeNode(Book())
        self.NULL.color = "BLACK"
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL
        self.color_flip_count = 0
        self.currentFunctionId = 0

    def LeftRotate(self, x):
        """
        Performs a left rotation on the given node x in the Red-Black Tree.
        """
        y = x.right
        x.right = y.left

        if y.left != self.NULL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def RightRotate(self, x):
        """
        Performs a right rotation on the given node x in the Red-Black Tree.
        """
        y = x.left
        x.left = y.right

        if y.right != self.NULL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def Insert(self, z):
        """
        Inserts a new node z into the Red-Black Tree and maintains the Red-Black Tree properties.
        """
        z.parent = None
        z.left = self.NULL
        z.right = self.NULL
        z.color = "RED"    

        y = None
        x = self.root

        while x != self.NULL:
            y = x
            if z.book.BookId < x.book.BookId:
                x = x.left
            else:
                x = x.right

        z.parent = y

        if y is None:
            self.root = z
        elif z.book.BookId < y.book.BookId:
            y.left = z
        else:
            y.right = z

        if z.parent is None:                         
            z.color = "BLACK"
            return
        
        if z.parent.parent is None :                  
            return
        
        self.InsertFixup(z)

    def InsertFixup(self, z):
        """
        Fixes the Red-Black Tree properties after an insertion of a new node z.
        """
        while z.parent.color == "RED":
            if z.parent == z.parent.parent.right:
                lg = z.parent.parent.left
                if lg.color == "RED":
                    self.ChangeNodeColor(lg,"BLACK")
                    self.ChangeNodeColor(z.parent,"BLACK")
                    self.ChangeNodeColor(z.parent.parent,"RED")
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.RightRotate(z)
                    self.ChangeNodeColor(z.parent,"BLACK")
                    self.ChangeNodeColor(z.parent.parent,"RED")
                    self.LeftRotate(z.parent.parent)
            else:
                rg = z.parent.parent.right
                if rg.color == 'RED':
                    self.ChangeNodeColor(rg,"BLACK")
                    self.ChangeNodeColor(z.parent,"BLACK")
                    self.ChangeNodeColor(z.parent.parent,"RED")
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.LeftRotate(z)
                    self.ChangeNodeColor(z.parent,"BLACK")
                    self.ChangeNodeColor(z.parent.parent,"RED")
                    self.RightRotate(z.parent.parent)
            if z == self.root:
                break
        self.ChangeNodeColor(self.root,"BLACK")
        
    def Transplant(self, u, v):
        """
        Replaces the subtree rooted at node u with the subtree rooted at node v in the Red-Black Tree.
        """
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def DeleteFixup(self, x):
        """
        Fixes the Red-Black Tree properties after a deletion of a node x.
        """
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    self.ChangeNodeColor(w,"BLACK")
                    self.ChangeNodeColor(x.parent,"RED")
                    self.LeftRotate(x.parent)
                    w = x.parent.right

                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    self.ChangeNodeColor(w,"RED")
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        self.ChangeNodeColor(w,"BLACK")
                        self.ChangeNodeColor(w,"RED")
                        self.RightRotate(w)
                        w = x.parent.right

                    self.ChangeNodeColor(w,x.parent.color)
                    self.ChangeNodeColor(x.parent,"BLACK")
                    self.ChangeNodeColor(w.right,"BLACK")
                    self.LeftRotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    self.ChangeNodeColor(w.color,"BLACK")
                    self.ChangeNodeColor(x.parent,"RED")
                    self.RightRotate(x.parent)
                    w = x.parent.left

                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    self.ChangeNodeColor(w,"RED")
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        self.ChangeNodeColor(w.right,"BLACK")
                        self.ChangeNodeColor(w,"RED")
                        self.LeftRotate(w)
                        w = x.parent.left

                    self.ChangeNodeColor(w,x.parent.color)
                    self.ChangeNodeColor(x.parent,"BLACK")
                    self.ChangeNodeColor(w.left,"BLACK")
                    self.RightRotate(x.parent)
                    x = self.root

        self.ChangeNodeColor(x,"BLACK")

    def Delete(self, z):
        y = z
        y_original_color = y.color

        if z.left == self.NULL:
            x = z.right
            self.Transplant(z, z.right)
        elif z.right == self.NULL:
            x = z.left
            self.Transplant(z, z.left)
        else:
            y = self.TreeMaximum(z.left)
            y_original_color = y.color
            x = y.left
            if y.parent == z:
                x.parent = y
            else:
                self.Transplant(y, y.left)
                y.left = z.left
                y.left.parent = y

            self.Transplant(z, y)
            y.right = z.right
            y.right.parent = y
            self.ChangeNodeColor(y, z.color)

        if y_original_color == "BLACK":
            self.DeleteFixup(x)

    def TreeMaximum(self, x):
        while x.right != self.NULL:
            x = x.right
        return x

    def InsertBook(self, book_id, book_name, author_name, availability_status=True, borrowed_by=None, reservation_heap=None):
        book = Book(book_id, book_name, author_name, availability_status, borrowed_by)
        z = RBTreeNode(book)
        self.currentFunctionId+=1
        self.Insert(z)
        return ""

    def DeleteBook(self, book_id):
        z = self.SearchBookNode(self.root, book_id)
        reservation = [str(x) for x in z.book.get_reservation_list()]
        if z is not None and z.book.BookId !=0:
            self.currentFunctionId+=1
            self.Delete(z)
            if len(reservation)>1:
                return f"Book {book_id} is no longer available. Reservations made by Patrons {', '.join(reservation)} have been cancelled!\n\n"
            elif len(reservation)==1:
                return f"Book {book_id} is no longer available. Reservation made by Patron {reservation[0]} has been cancelled!\n\n"
            else:
                return f"Book {book_id} is no longer available.\n\n"
        else:
            return f"Book {book_id} not found in the Library\n\n"

    def SearchBookNode(self, node, book_id):
        while node != self.NULL and int(book_id) != int(node.book.BookId):
            if int(book_id) < int(node.book.BookId):
                node = node.left
            else:
                node = node.right
        return node

    def PrintBook(self, book_id):
        node = self.SearchBookNode(self.root, book_id)
        if (node is not None) and (node.book.BookId != 0):
            return str(node.book)
        else:
            return f"Book {book_id} not found in the Library\n\n"

    def PrintBooks(self, book_id1, book_id2):
        books = self.GetBooksInRange(self.root, book_id1, book_id2)
        opstring= ""
        if books:
            for book in books:
                opstring+=str(book)
        else:
            opstring ="No Books found in the given range."
        return opstring

    def GetBooksInRange(self, node, book_id1, book_id2):
            books = []
            if node is not None:
                if int(book_id1) < int(node.book.BookId):
                    books.extend(self.GetBooksInRange(node.left, book_id1, book_id2))
                if int(book_id1) <= int(node.book.BookId) <= int(book_id2):
                    books.append(node.book)
                if int(book_id2) > node.book.BookId:
                    books.extend(self.GetBooksInRange(node.right, book_id1, book_id2))
            return books


    def BorrowBook(self, patron_id, book_id, patron_priority):
        """
        This function allows a patron to borrow a book from the library.
        
        Parameters:
        - patron_id: The ID of the patron borrowing the book.
        - book_id: The ID of the book being borrowed.
        - patron_priority: The priority of the patron borrowing the book.
        
        Returns:
        - opmssg: A string indicating the status of the borrowing operation.
        """
        book_node = self.SearchBookNode(self.root, book_id)
        if book_node is not None:
            if book_node.book.AvailabilityStatus:
                book_node.book.AvailabilityStatus = False
                book_node.book.BorrowedBy = patron_id
                return f"Book {book_id} Borrowed by Patron {patron_id}\n\n"
            else:
                book_node.book.add_reservation(int(patron_id), int(patron_priority), time.time())
                return f"Book {book_id} Reserved by Patron {patron_id}\n\n"
        else:
            return f"Book {book_id} not found in the Library\n\n"


    def ReturnBook(self, patron_id, book_id):
        """
        This function allows a patron to return a borrowed book to the library.
        
        Parameters:
        - patron_id: The ID of the patron returning the book.
        - book_id: The ID of the book being returned.
        
        Returns:
        - opmssg: A string indicating the status of the returning operation.
        """
        book_node = self.SearchBookNode(self.root, book_id)
        if book_node is not None and not book_node.book.AvailabilityStatus:
            book_node.book.AvailabilityStatus = True
            book_node.book.BorrowedBy = None
            opmssg = f"Book {book_id} Returned by Patron {patron_id}\n\n"
            if book_node.book.ReservationHeap:
                reservation = book_node.book.ReservationHeap.pop(0)
                book_node.book.BorrowedBy = reservation[0]
                opmssg += f"Book {book_id} Allotted to Patron {reservation[0]}\n\n"
                book_node.book.AvailabilityStatus = False
            return opmssg
        else:
            return f"Book {book_id} not found in the Library or not borrowed by Patron {patron_id}\n\n"


    def FindClosestBook(self, target_id):
        """
        This function finds the closest book(s) to a given target book ID in the Red-Black Tree.
        
        Parameters:
        - target_id: The target book ID.
        
        Returns:
        - closest_nodes: A string representation of the closest book(s) to the target book ID.
        """
        closest_nodes = self.FindClosestBookHelper(self.root, target_id)
        if closest_nodes:
            return "".join([str(book) for book in closest_nodes])
        else:
            return "No books in the Library.\n\n"


    def FindClosestBookHelper(self, node, target_id):
        """
        This helper function recursively finds the closest book(s) to a given target book ID in the Red-Black Tree.
        
        Parameters:
        - node: The current node being traversed in the Red-Black Tree.
        - target_id: The target book ID.
        
        Returns:
        - closest_nodes: A list of the closest book(s) to the target book ID.
        """
        if node is not None:
            closest_nodes = []
            # Traverse the tree to find the closest nodes
            while node:
                if int(node.book.BookId) == int(target_id):
                    return [node.book]

                if int(node.book.BookId) < int(target_id):
                    closest_nodes.append(node.book)
                    node = node.right
                else:
                    closest_nodes.append(node.book)
                    node = node.left

            # Find the inorder predecessor and successor
            pred, succ = self.InorderPredecessorSuccessor(target_id)

            # Calculate distances to the target ID
            pred_distance = abs(int(pred.book.BookId) - int(target_id)) if pred else float('inf')
            succ_distance = abs(int(succ.book.BookId) - int(target_id)) if succ else float('inf')

            # Compare distances and return the closest nodes
            if pred_distance < succ_distance:
                return [pred.book] if pred else []
            elif succ_distance < pred_distance:
                return [succ.book] if succ else []
            else:
                return sorted([pred.book, succ.book], key=lambda book: int(book.BookId) if book else float('inf'))
        return []


    def InorderPredecessorSuccessor(self, target_id):
        """
        This function finds the inorder predecessor and successor of a given target book ID in the Red-Black Tree.
        
        Parameters:
        - target_id: The target book ID.
        
        Returns:
        - pred: The inorder predecessor of the target book ID.
        - succ: The inorder successor of the target book ID.
        """
        pred = None
        succ = None
        current = self.root

        while current.book.BookId != 0:
            if int(current.book.BookId) == int(target_id):
                if current.left:
                    pred = current.left
                    while pred.right:
                        pred = pred.right

                if current.right:
                    succ = current.right
                    while succ.left:
                        succ = succ.left

                break
            elif int(current.book.BookId) < int(target_id):
                pred = current
                current = current.right
            else:
                succ = current
                current = current.left

        return pred, succ


    def ColorFlipCount(self):
        """
        This function returns the count of color flips performed in the Red-Black Tree.
        
        Returns:
        - count: The count of color flips.
        """
        return f"Color Flip Count: {self.color_flip_count}\n\n"


    def ChangeNodeColor(self, node, new_color):
        """
        This function changes the color of a given node in the Red-Black Tree.
        
        Parameters:
        - node: The node whose color needs to be changed.
        - new_color: The new color of the node.
        """
        if node.color != new_color:
            if node.colorChangingFunctionId != self.currentFunctionId:
                print(node.book.BookId, self.currentFunctionId, node.colorChangingFunctionId, node.color, "-->", new_color, " +1")
                self.color_flip_count += 1  # Increment color flip count
                node.colorChangingFunctionId = self.currentFunctionId
            else:
                print(node.book.BookId, self.currentFunctionId, node.colorChangingFunctionId, node.color, "-->", new_color, " -1")
                self.color_flip_count -= 1
                node.colorChangingFunctionId = 0

        node.color = new_color


    def Quit(self):
        """
        This function terminates the program.
        
        Returns:
        - message: A string indicating the termination of the program.
        """
        return "Program Terminated!!"


def main():
    # Check if a filename is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    # Get the filename from the command line argument
    input_filename = sys.argv[1]
    # Compute the filename of outputfile
    output_filename = f"{input_filename.split('.')[0]}_output_file.txt"
    
    # Create an instance of RedBlackTree
    rb_tree = RedBlackTree()
    
    # Map function names to corresponding methods in RedBlackTree class
    function_map = {
        "PrintBook": rb_tree.PrintBook,
        "PrintBooks": rb_tree.PrintBooks,
        "InsertBook": rb_tree.InsertBook,
        "BorrowBook": rb_tree.BorrowBook,
        "ReturnBook": rb_tree.ReturnBook,
        "DeleteBook": rb_tree.DeleteBook,
        "FindClosestBook": rb_tree.FindClosestBook,
        "ColorFlipCount": rb_tree.ColorFlipCount,
        "Quit": rb_tree.Quit
    }

    # Open input and output files
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        # Read input commands line by line
        for command in input_file:
            # Extract function name and parameters from the command
            function = command.strip().split("(")[0]
            parameters = command.strip().split("(")[1].replace('"', '')[:-1].strip(")").split(",")
            
            # Handle the case when there are no parameters
            if parameters == ['']:
                parameters = []
            
            # Perform the required function
            op = function_map[function](*parameters)
            
            # Write function output to file
            output_file.write(f"{op}")
            
            # Check if the program should terminate
            if op == "Program Terminated!!":
                break

if __name__ == "__main__":
    main()
