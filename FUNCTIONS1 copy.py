import psycopg2

from getpass import getpass

def connect_db():
    return psycopg2.connect(dbname='fitness_club2', user='postgres', password='postgres', host='localhost')

def user_registration(cur):
    print("Registering a new member.")
    full_name = input("Enter full name: ")
    email = input("Enter email: ")
    password = getpass("Enter password: ")
    weight_goal = input("Enter weight goal: ")
    weight = input("Enter current weight: ")
    try:
        cur.execute("INSERT INTO Member (FullName, Email, Password, Weight_goal, Weight) VALUES (%s, %s, %s, %s, %s)",
                    (full_name, email, password, weight_goal, weight))
        print("Registration successful.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_profile(cur,member_id):
    new_weight = input("Enter new weight: ")
    new_goal = input("Enter new weight goal: ")
    try:
        cur.execute("UPDATE Member SET Weight = %s, Weight_goal = %s WHERE MemberID = %s", (new_weight, new_goal, member_id))
        print("Profile updated successfully.")
    except Exception as e:
        print(f"Error updating profile: {e}")


def view_dashboard(cur, member_id):
    try:
        cur.execute("SELECT * FROM Member WHERE MemberID = %s", (member_id,))
        member = cur.fetchone()
        if member:
            print("Member Dashboard:")
            print(f"Name: {member[1]}, Email: {member[2]}, Weight Goal: {member[4]}, Current Weight: {member[5]}")
        else:
            print("Member not found.")
    except Exception as e:
        print(f"Error retrieving dashboard: {e}")

def schedule_session(cur, member_id):
    """Schedules a session for a member with a trainer and generates a billing record."""
    trainer_id = input("Enter trainer ID: ")
    date_time = input("Enter session datetime (YYYY-MM-DD HH:MM): ")
    duration_hours = float(input("Enter duration in hours (e.g., 1.5 for one and a half hours): "))
    status = 'Scheduled'
    rate_per_hour = 100  # Rate per hour

    try:
        # Convert duration from hours to an interval acceptable by PostgreSQL
        duration_interval = f'{duration_hours} hours'
        
        # Insert the session
        cur.execute("""
            INSERT INTO Session (TrainerID, MemberID, DateTime, Duration, Status)
            VALUES (%s, %s, %s, %s::interval, %s)
            RETURNING SessionID;
            """, (trainer_id, member_id, date_time, duration_interval, status))
        session_id = cur.fetchone()[0]
        
        # Calculate the cost of the session
        total_cost = rate_per_hour * duration_hours
        
        # Insert a billing record for the session
        cur.execute("""
            INSERT INTO Billing (MemberID, Amount, DueDate, SessionID)
            VALUES (%s, %s, %s, %s);
            """, (member_id, total_cost, date_time, session_id))
        print(f"Session scheduled successfully. Total cost: ${total_cost:.2f}")
    except Exception as e:
        print(f"Error scheduling session: {e}")

def trainer_schedule_management(cur, trainer_id):
    day = input("Enter day for availability (e.g., 'Monday'): ")
    try:
        cur.execute("INSERT INTO Availability (TrainerID, Day) VALUES (%s, %s)", (trainer_id, day))
        print("Trainer availability updated.")
    except psycopg2.Error as e:
        print(f"Error updating trainer schedule: {e.pgerror}")

def make_payment(cur, member_id, bill_id, payment_method):
    payment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current time as payment time
    try:
        cur.execute("""
        INSERT INTO Payment (BillID, PaymentMethod, PaymentDate) VALUES (%s, %s, %s) RETURNING PaymentID;
        """, (bill_id, payment_method, payment_date))
        payment_id = cur.fetchone()[0]
        cur.execute("""
        UPDATE Billing SET PaymentID = %s WHERE BillID = %s;
        """, (payment_id, bill_id))
        print("Payment made successfully.")
    except Exception as e:
        print(f"Error making payment: {e}")
        
def view_payments(cur, member_id):
    try:
        cur.execute("""
        SELECT p.PaymentID, p.PaymentMethod, p.PaymentDate, b.Amount
        FROM Payment p
        JOIN Billing b ON p.BillID = b.BillID
        WHERE b.MemberID = %s;
        """, (member_id,))
        payments = cur.fetchall()
        if payments:
            print("PaymentID | PaymentMethod | PaymentDate | Amount")
            for payment in payments:
                print(f"{payment[0]} | {payment[1]} | {payment[2]} | {payment[3]}")
        else:
            print("No payments found.")
    except Exception as e:
        print(f"Error retrieving payments: {e}")

def view_schedule(cur, user_id, role):
    """Displays the schedule for a member or trainer."""
    if role == 'Member':
        query = """
        SELECT s.DateTime, s.Duration, s.Status, t.FullName AS Trainer
        FROM Session s
        JOIN Trainer t ON s.TrainerID = t.TrainerID
        WHERE s.MemberID = %s;
        """
    elif role == 'Trainer':
        query = """
        SELECT s.DateTime, s.Duration, s.Status, m.FullName AS Member
        FROM Session s
        JOIN Member m ON s.MemberID = m.MemberID
        WHERE s.TrainerID = %s;
        """
    else:
        print("Invalid role specified. Please enter 'Member' or 'Trainer'.")
        return

    try:
        cur.execute(query, (user_id,))
        sessions = cur.fetchall()
        if sessions:
            print(f"{'DateTime':<20} {'Duration':<15} {'Status':<15} {'Name':<20}")
            for session in sessions:
                dt, dur, status, name = session
                print(f"{dt:<20} {dur:<15} {status:<15} {name:<20}")
        else:
            print("No scheduled sessions found.")
    except Exception as e:
        print(f"Error retrieving schedule: {e}")
        
def view_member_profile(cur):

    member_name = input("Enter member's name to search: ")
    try:
        cur.execute("SELECT * FROM Member WHERE FullName ILIKE %s", ('%' + member_name + '%',))
        members = cur.fetchall()
        if members:
            for member in members:
                print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}, Weight: {member[5]}")
        else:
            print("No members found with that name.")
    except Exception as e:
         print(f"member not found")



def admin_manage_room_bookings(cur, admin_id):
    room_id = input("Enter room ID for booking update: ")
    new_capacity = input("Enter new capacity: ")
    try:
        cur.execute("UPDATE Room SET Capacity = %s WHERE RoomID = %s", (new_capacity, room_id))
        print("Room booking updated.")
    except Exception as e:
        print(f"Error updating room bookings: {e}")

def admin_manage_equipment(cur, admin_id):
    equipment_id = input("Enter equipment ID for maintenance update: ")
    new_schedule = input("Enter new maintenance schedule (YYYY-MM-DD): ")
    try:
        cur.execute("UPDATE Equipment SET MaintenanceSchedule = %s WHERE EquipmentID = %s", (new_schedule, equipment_id))
        print("Equipment maintenance updated.")
    except Exception as e:
        print(f"Error updating equipment maintenance: {e}")

def admin_update_class_schedule(cur, admin_id):
    class_id = input("Enter class ID for schedule update: ")
    new_day = input("Enter new day for the class: ")
    new_start_time = input("Enter new start time (HH:MM): ")
    new_end_time = input("Enter new end time (HH:MM): ")
    try:
        cur.execute("UPDATE ClassSchedule SET Day = %s, StartTime = %s, EndTime = %s WHERE ClassID = %s",
                    (new_day, new_start_time, new_end_time, class_id))
        print("Class schedule updated.")
    except Exception as e:
        print(f"Error updating class schedule: {e}")


def login_user(cur):
    email = input("Enter your email: ")
    password = getpass("Enter your password: ")
    cur.execute("SELECT MemberID, FullName FROM Member WHERE Email = %s AND Password = %s", (email, password))
    user = cur.fetchone()
    if user:
        return 'Member', user[0]
    cur.execute("SELECT TrainerID, FullName FROM Trainer WHERE Email = %s AND Password = %s", (email, password))
    user = cur.fetchone()
    if user:
        return 'Trainer', user[0]
    cur.execute("SELECT StaffID, FullName FROM AdminStaff WHERE Email = %s AND Password = %s", (email, password))
    user = cur.fetchone()
    if user:
        return 'Admin', user[0]
    return None, None

def member_menu(cur, member_id):
    while True:
        print("\nMember Menu")
        print("1. Update Profile")
        print("2. View Dashboard")
        print("3. Schedule session")
        print("4. Make a Payment")
        print("5. View Payments")
        print("6. Log Out")
        choice = input("Choose an option: ")
        if choice == '1':
            update_profile(cur, member_id)
        elif choice == '2':
            view_dashboard(cur, member_id)
        elif choice == '3':
            schedule_session(cur, member_id)
        elif choice == '4':
            bill_id = input("Enter Bill ID to pay: ")
            payment_method = input("Enter payment method (e.g., Credit Card, PayPal): ")
            make_payment(cur, member_id, bill_id, payment_method)
        elif choice == '5':
            view_payments(cur, member_id)
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

def trainer_menu(cur, trainer_id):
    while True:
        print("\nTrainer Menu")
        print("1. Update Availability")
        print("2. View Member Profile")
        print("3. View Schedule")
        print("4. Log Out")
        choice = input("Choose an option: ")
        if choice == '1':
            trainer_schedule_management(cur, trainer_id)
        elif choice == '2':
            view_member_profile(cur)
        elif choice == '3':
            view_schedule(cur, trainer_id, 'Trainer')
        elif choice == '4':
            break
        else:
            print("Invalid choice.")
            
def admin_menu(cur, admin_id):
    while True:
        print("\nAdmin Menu")
        print("1. Manage Room Bookings")
        print("2. Manage Equipment")
        print("3. Update Class Schedules")
        print("4. Log Out")
        choice = input("Choose an option: ")
        if choice == '1':
            admin_manage_room_bookings(cur, admin_id)
        elif choice == '2':
            admin_manage_equipment(cur, admin_id)
        elif choice == '3':
            admin_update_class_schedule(cur, admin_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

def main():
    with connect_db() as conn:
        cur = conn.cursor()
        while True:
            choice = input("Do you want to [signup], [login], or [exit]? ").lower()
            if choice == 'exit':
                break
            elif choice == 'signup':
                user_registration(cur)
                conn.commit()
            elif choice == 'login':
                user_type, user_id = login_user(cur)
                if user_type == 'Member':
                    member_menu(cur, user_id)
                elif user_type == 'Trainer':
                    trainer_menu(cur, user_id)
                elif user_type == 'Admin':
                    admin_menu(cur,user_id)
                else:
                    print("Invalid login. Please try again.")
                conn.commit()

if __name__ == "__main__":
    main()

