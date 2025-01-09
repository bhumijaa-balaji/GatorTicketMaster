from datetime import datetime
import sys

class RedBlackNode: 
# Node class for Red-Black Tree implementation.
# Each node contains user ID, seat number, color, and references to parent and children nodes.
    def __init__(self, user_identifier: int, seat_number: int):
        self.user_identifier = user_identifier
        self.seat_number = seat_number
        self.node_color = 'r'  # 'r' for red, 'b' for black
        self.left_child = None
        self.right_child = None
        self.parent = None

    def get_grandparent(self):
# Returns the grandparent node if it exists, otherwise None.
        if self.parent is None:
            return None
        return self.parent.parent

    def get_sibling(self):
# Returns the sibling node (other child of parent) if it exists, otherwise None.
        if self.parent is None:
            return None
        if self == self.parent.left_child:
            return self.parent.right_child
        return self.parent.left_child

    def get_uncle(self):
# Returns the uncle node (parent's sibling) if it exists, otherwise None.

        if self.parent is None:
            return None
        return self.parent.get_sibling()

class RedBlackTree:

# Red-Black Tree implementation for managing seat reservations.
# Maintains the following properties:
# 1. Every node is either red or black
# 2. Root is always black
# 3. No two adjacent red nodes
# 4. Every path from root to leaf has same number of black nodes


    def __init__(self):
# Initialize with a sentinel nil node (used as leaf nodes)        
        self.nil_node = RedBlackNode(None, None)
        self.nil_node.node_color = 'b'
        self.root = self.nil_node

    def insert_node(self, user_identifier, seat_number):
        """
        Inserts a new node into the tree and maintains Red-Black properties.
        Args:
            user_identifier: User ID for the reservation
            seat_number: Assigned seat number
        """
        # Create new red node
        new_node = RedBlackNode(user_identifier, seat_number)
        new_node.left_child = self.nil_node
        new_node.right_child = self.nil_node
        new_node.node_color = 'r'

        # Find proper insertion point
        current_node = self.root
        parent_node = None
        while current_node != self.nil_node:
            parent_node = current_node
            if new_node.user_identifier < current_node.user_identifier:
                current_node = current_node.left_child
            else:
                current_node = current_node.right_child

        new_node.parent = parent_node

        # Insert node in proper position
        if parent_node is None:
            self.root = new_node
        elif new_node.user_identifier < parent_node.user_identifier:
            parent_node.left_child = new_node
        else:
            parent_node.right_child = new_node

        # Handle special cases and fix violations
        if new_node.parent is None:
            new_node.node_color = 'b'
            return
        if new_node.get_grandparent() is None:
            return

        self.fix_insert_violation(new_node)

    def fix_insert_violation(self, node):
        """
        Fixes Red-Black Tree properties after insertion.
        Handles three cases:
        1. Uncle is red - Recolor
        2. Uncle is black (triangle) - Rotate once
        3. Uncle is black (line) - Rotate twice
        """     

        while node.parent and node.parent.node_color == 'r':
            if node.parent == node.get_grandparent().right_child:
                uncle = node.get_uncle()
                if uncle and uncle.node_color == 'r':
                    # Case 1: Uncle is red, perform recoloring
                    uncle.node_color = 'b'
                    node.parent.node_color = 'b'
                    node.get_grandparent().node_color = 'r'
                    node = node.get_grandparent()
                else:
                    # Case 2 & 3: Uncle is black, perform rotations
                    if node == node.parent.left_child:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.node_color = 'b'
                    node.get_grandparent().node_color = 'r'
                    self.left_rotate(node.get_grandparent())
            else:
                uncle = node.get_uncle()
                if uncle and uncle.node_color == 'r':
                    # Case 1: Uncle is red, perform recoloring
                    uncle.node_color = 'b'
                    node.parent.node_color = 'b'
                    node.get_grandparent().node_color = 'r'
                    node = node.get_grandparent()
                else:
                    # Case 2 & 3: Uncle is black, perform rotations
                    if node == node.parent.right_child:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.node_color = 'b'
                    node.get_grandparent().node_color = 'r'
                    self.right_rotate(node.get_grandparent())
            if node == self.root:
                break
        self.root.node_color = 'b'

    def left_rotate(self, x):
        """Performs left rotation around node x to maintain tree balance."""
        y = x.right_child
        x.right_child = y.left_child
        if y.left_child != self.nil_node:
            y.left_child.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left_child:
            x.parent.left_child = y
        else:
            x.parent.right_child = y
        y.left_child = x
        x.parent = y

    def right_rotate(self, y):
        """Performs right rotation around node y to maintain tree balance."""
        x = y.left_child
        y.left_child = x.right_child
        if x.right_child != self.nil_node:
            x.right_child.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right_child:
            y.parent.right_child = x
        else:
            y.parent.left_child = x
        x.right_child = y
        y.parent = x

    def search(self, user_identifier):
        """
        Searches for a node with given user_identifier.
        Returns the node if found, None otherwise.
        """
        current_node = self.root
        while current_node != self.nil_node:
            if user_identifier == current_node.user_identifier:
                return current_node
            elif user_identifier < current_node.user_identifier:
                current_node = current_node.left_child
            else:
                current_node = current_node.right_child
        return None

    def delete_node(self, user_identifier):
        """
        Deletes node with given user_identifier and maintains Red-Black properties.
        Uses standard BST deletion with additional color fixing.
        """
        node_to_remove = self.search(user_identifier)
        if node_to_remove is None:
            return
        
        y = node_to_remove
        y_original_color = y.node_color
        # Handle different cases based on number of children
        if node_to_remove.left_child == self.nil_node:
            x = node_to_remove.right_child
            self.transplant(node_to_remove, node_to_remove.right_child)
        elif node_to_remove.right_child == self.nil_node:
            x = node_to_remove.left_child
            self.transplant(node_to_remove, node_to_remove.left_child)
        else:
            # Node has two children
            y = self.find_minimum(node_to_remove.right_child)
            y_original_color = y.node_color
            x = y.right_child
            if y.parent == node_to_remove:
                x.parent = y
            else:
                self.transplant(y, y.right_child)
                y.right_child = node_to_remove.right_child
                y.right_child.parent = y
            self.transplant(node_to_remove, y)
            y.left_child = node_to_remove.left_child
            y.left_child.parent = y
            y.node_color = node_to_remove.node_color

        # Fix Red-Black properties if necessary
        if y_original_color == 'b':
            self.delete_fixup(x)

    def delete_fixup(self, x):
        while x != self.root and x.node_color == 'b':
            if x == x.parent.left_child:
                w = x.parent.right_child
                # Handle various cases of double-black fixing
                if w.node_color == 'r':
                    w.node_color = 'b'
                    x.parent.node_color = 'r'
                    self.left_rotate(x.parent)
                    w = x.parent.right_child
                if w.left_child.node_color == 'b' and w.right_child.node_color == 'b':
                    w.node_color = 'r'
                    x = x.parent
                else:
                    if w.right_child.node_color == 'b':
                        w.left_child.node_color = 'b'
                        w.node_color = 'r'
                        self.right_rotate(w)
                        w = x.parent.right_child
                    w.node_color = x.parent.node_color
                    x.parent.node_color = 'b'
                    w.right_child.node_color = 'b'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                # Mirror cases for right child
                w = x.parent.left_child
                if w.node_color == 'r':
                    w.node_color = 'b'
                    x.parent.node_color = 'r'
                    self.right_rotate(x.parent)
                    w = x.parent.left_child
                if w.right_child.node_color == 'b' and w.left_child.node_color == 'b':
                    w.node_color = 'r'
                    x = x.parent
                else:
                    if w.left_child.node_color == 'b':
                        w.right_child.node_color = 'b'
                        w.node_color = 'r'
                        self.left_rotate(w)
                        w = x.parent.left_child
                    w.node_color = x.parent.node_color
                    x.parent.node_color = 'b'
                    w.left_child.node_color = 'b'
                    self.right_rotate(x.parent)
                    x = self.root
        x.node_color = 'b'

    def transplant(self, u, v):
        """Helper function for node deletion. Replaces subtree rooted at u with subtree rooted at v."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left_child:
            u.parent.left_child = v
        else:
            u.parent.right_child = v
        v.parent = u.parent

    def find_minimum(self, node):
        """Finds the minimum value in the subtree rooted at given node."""
        while node.left_child != self.nil_node:
            node = node.left_child
        return node

    def inorder_traversal(self):
        """Returns sorted list of (seat_number, user_identifier) pairs."""
        result = []
        stack = []
        current_node = self.root
        while current_node != self.nil_node or stack:
            while current_node != self.nil_node:
                stack.append(current_node)
                current_node = current_node.left_child
            current_node = stack.pop()
            result.append((current_node.seat_number, current_node.user_identifier))
            current_node = current_node.right_child
        return sorted(result)

class MinHeap:
    """
    Min Heap implementation for managing available seats and waitlist.
    Ensures O(log n) insertion and deletion of minimum element.
    """
    def __init__(self):
        self.heap = []  # Data structure for heap

    def is_empty(self):
        """Returns True if heap is empty, False otherwise."""
        return len(self.heap) == 0

    def insert(self, key):
        """Inserts new key into heap and maintains heap property."""
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def delete_min(self):
        """Removes and returns minimum element from heap."""
        if self.is_empty():
            return None
        min_value = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._heapify_down(0)
        return min_value

    def _heapify_up(self, index):
        """Maintains heap property by moving element up if needed."""
        parent_index = (index - 1) // 2
        while parent_index >= 0 and self.heap[parent_index] > self.heap[index]:
            # Swap parent and child
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            index = parent_index
            parent_index = (index - 1) // 2

    def _heapify_down(self, index):
        """Maintains heap property by moving element down if needed."""
        smallest = index
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        if left_child_index < len(self.heap) and self.heap[left_child_index] < self.heap[smallest]:
            smallest = left_child_index
        if right_child_index < len(self.heap) and self.heap[right_child_index] < self.heap[smallest]:
            smallest = right_child_index

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def get_min(self):
        """Returns minimum element without removing it."""
        if self.is_empty():
            return None
        return self.heap[0]

class GatorTicketMaster:
    """
    Main ticket management system that combines Red-Black Tree and Min Heap
    to provide efficient seat reservation and waitlist management.
    """
    def __init__(self):
        self.reserved_seats = RedBlackTree()
        self.available_seats = MinHeap()
        self.waitlist = MinHeap()
        self.total_seats = 0

    def initialize(self, seat_count):
        """
        Initializes the ticket system with given number of seats.
        Args:
            seat_count: Number of seats to initialize
        Returns:
            str: Status message
        """
        if seat_count <= 0:
            return 'Invalid input. Please provide a valid number of seats.'
        self.total_seats = seat_count
        for seat in range(1, seat_count + 1):
            self.available_seats.insert(seat)
        return f'{seat_count} Seats are made available for reservation'

    def available(self):
        """
        Reports current system status.
        Returns:
            str: Message showing available seats and waitlist length
        """
        return f'Total Seats Available: {len(self.available_seats.heap)}, Waitlist: {len(self.waitlist.heap)}'

    def reserve(self, user_id, user_priority):
        """
        Handles seat reservation requests.
        If seats are available, assigns seat to user.
        If no seats available, adds user to waitlist with priority.
        
        Args:
            user_id: Unique identifier for the user
            user_priority: Priority level for waitlist positioning
        Returns:
            str: Status message indicating reservation or waitlist status
        """
        if self.available_seats.heap:
            seat_id = self.available_seats.delete_min()
            self.reserved_seats.insert_node(user_id, seat_id)
            return f'User {user_id} reserved seat {seat_id}'
        else:
            self.waitlist.insert((-user_priority, datetime.now(), user_id))
            return f'User {user_id} is added to the waiting list'

    def cancel(self, seat_id, user_id):
        """
        Cancels reservation for given user and seat.
        If waitlist exists, assigns seat to highest priority user in waitlist.
        
        Args:
            seat_id: Seat number to cancel
            user_id: User ID canceling the reservation
        Returns:
            str: Status message about cancellation and potential reassignment
        """
        node = self.reserved_seats.search(user_id)
        if node is None:
            return f'User {user_id} has no reservation to cancel'
        if node.seat_number != seat_id:
            return f'User {user_id} has no reservation for seat {seat_id} to cancel'
        self.reserved_seats.delete_node(user_id)
        if self.waitlist.heap:
            next_user = self.waitlist.delete_min()
            self.reserved_seats.insert_node(next_user[2], seat_id)
            return f'User {user_id} canceled their reservation\nUser {next_user[2]} reserved seat {seat_id}'
        else:
            self.available_seats.insert(seat_id)
            return f'User {user_id} canceled their reservation'

    def exit_waitlist(self, user_id):
        """
        Removes user from waitlist upon request.
        
        Args:
            user_id: User ID to remove from waitlist
        Returns:
            str: Status message about waitlist removal
        """
        for i, (_, _, uid) in enumerate(self.waitlist.heap):
            if uid == user_id:
                self.waitlist.heap[i] = self.waitlist.heap[-1]
                self.waitlist.heap.pop()
                self.waitlist._heapify_down(i)
                return f'User {user_id} is removed from the waiting list'
        return f'User {user_id} is not in waitlist'

    def update_priority(self, user_id, user_priority):
        """
        Updates priority for user in waitlist.
        
        Args:
            user_id: User ID to update
            user_priority: New priority level
        Returns:
            str: Status message about priority update
        """
        for i, (_, timestamp, uid) in enumerate(self.waitlist.heap):
            if uid == user_id:
                self.waitlist.heap[i] = (-user_priority, timestamp, uid)
                self.waitlist._heapify_up(i)
                self.waitlist._heapify_down(i)
                return f'User {user_id} priority has been updated to {user_priority}'
        return f'User {user_id} priority is not updated'

    def add_seats(self, count):
        """
        Adds new seats to the system and assigns them to waitlist users if any.
        
        Args:
            count: Number of new seats to add
        Returns:
            str: Status message about added seats and assignments
        """
        if count <= 0:
            return 'Invalid input. Please provide a valid number of seats.'
        new_seats = list(range(self.total_seats + 1, self.total_seats + count + 1))
        self.total_seats += count
        result = [f'Additional {count} Seats are made available for reservation']
        for seat in new_seats:
            if self.waitlist.heap:
                next_user = self.waitlist.delete_min()
                self.reserved_seats.insert_node(next_user[2], seat)
                result.append(f'User {next_user[2]} reserved seat {seat}')
            else:
                self.available_seats.insert(seat)
        return '\n'.join(result)

    def print_reservations(self):
        """
        Prints all current reservations in order of seat number.
        
        Returns:
            str: Formatted list of all reservations
        """
        reservations = self.reserved_seats.inorder_traversal()
        if not reservations:
            return 'No reservations to print.'
        return '\n'.join(f'Seat {seat}, User {user}' for seat, user in reservations)

    def release_seats(self, user_id1, user_id2):
        """
        Releases all reservations for users in given ID range.
        Reassigns released seats to waitlist users if any.
        
        Args:
            user_id1: Start of user ID range
            user_id2: End of user ID range (inclusive)
        Returns:
            str: Status message about released seats and reassignments
        """
        if user_id1 > user_id2:
            return 'Invalid input. Please provide a valid range of users.'
        released_seats = []
        for user_id in range(user_id1, user_id2 + 1):
            node = self.reserved_seats.search(user_id)
            if node:
                released_seats.append(node.seat_number)
                self.reserved_seats.delete_node(user_id)
        self.waitlist.heap = [item for item in self.waitlist.heap if not (user_id1 <= item[2] <= user_id2)]
        result = [f'Reservations of the Users in the range [{user_id1}, {user_id2}] are released']
        for seat in released_seats:
            if self.waitlist.heap:
                next_user = self.waitlist.delete_min()
                self.reserved_seats.insert_node(next_user[2], seat)
                result.append(f'User {next_user[2]} reserved seat {seat}')
            else:
                self.available_seats.insert(seat)
        return '\n'.join(result)

    def quit(self):
        """
        Terminates the program.
        
        Returns:
            str: Termination message
        """
        return 'Program Terminated!!'



if __name__ == '__main__':
    # Check if the input test case file is provided
    if len(sys.argv) != 2:
        print('Check the usage. It should be of the form: python3 gatorTicketMaster.py <test_case_fname>')
        sys.exit(1)

    test_case_input = sys.argv[1]
    output_file = f"{test_case_input.split('.')[0]}_output_file.txt"

    # Initialize ticket master system
    ticket_master = GatorTicketMaster()

    with open(test_case_input, 'r') as input_file, open(output_file, 'w') as output_file:
        for line in input_file:
            line = line.strip()
            if not line:
                continue

            # Parse command and arguments
            command = line.split('(')[0]
            args_str = line.split('(')[1].split(')')[0]
            args = [int(arg.strip()) for arg in args_str.split(',')] if args_str else []

            result = ''

            # Execute appropriate command
            if command == 'Initialize':
                result = ticket_master.initialize(args[0])
            elif command == 'Available':
                result = ticket_master.available()
            elif command == 'Reserve':
                result = ticket_master.reserve(args[0], args[1])
            elif command == 'Cancel':
                result = ticket_master.cancel(args[0], args[1])
            elif command == 'ExitWaitlist':
                result = ticket_master.exit_waitlist(args[0])
            elif command == 'UpdatePriority':
                result = ticket_master.update_priority(args[0], args[1])
            elif command == 'AddSeats':
                result = ticket_master.add_seats(args[0])
            elif command == 'PrintReservations':
                result = ticket_master.print_reservations()
            elif command == 'ReleaseSeats':
                result = ticket_master.release_seats(args[0], args[1])
            elif command == 'Quit':
                result = ticket_master.quit()
                output_file.write(result + '\n')
                break

            # Write result to output file
            output_file.write(result + '\n')