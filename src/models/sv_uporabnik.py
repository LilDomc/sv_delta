import hashlib
from flask import session
import db  # tvoja db.py datoteka naj omogoča PostgreSQL povezavo prek psycopg2 ali podobno

class Uporabnik:
    def __init__(self, email, geslo):
        self.email = email
        self.geslo = geslo

    @staticmethod
    def _hash_geslo(geslo):
        """
        Vrne SHA-256 hash gesla.
        """
        return hashlib.sha256(geslo.encode()).hexdigest()

    @staticmethod
    def registriraj(ime, priimek, email, geslo):
        """
        Registrira uporabnika, če še ne obstaja z enakim emailom.
        Če obstaja v tabeli employees (glede na email), se mu dodeli vloga 'employee'
        in poveže z njegovim employeeID.
        """
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                # Preveri, če uporabnik že obstaja
                cursor.execute("SELECT userID FROM users WHERE email = %s;", (email,))
                if cursor.fetchone():
                    print(f"[WARN] Uporabnik z emailom {email} že obstaja.")
                    return "Uporabnik s tem e-poštnim naslovom že obstaja."

                # Hashiraj geslo
                hashirano_geslo = Uporabnik._hash_geslo(geslo)

                # Privzete vrednosti
                employee_id = None
                role = 'user'

                # Preveri, če je ta email tudi med zaposlenimi
                cursor.execute("SELECT employeeID FROM employees WHERE email = %s;", (email,))
                rezultat = cursor.fetchone()
                if rezultat:
                    employee_id = rezultat[0]
                    role = 'employee'

                # Vstavi uporabnika v bazo
                cursor.execute('''
                    INSERT INTO users (ime, priimek, email, geslo, employeeID, role)
                    VALUES (%s, %s, %s, %s, %s, %s);
                ''', (ime, priimek, email, hashirano_geslo, employee_id, role))
                conn.commit()

            print(f"[INFO] Uporabnik {email} uspešno registriran kot {role}.")
            return True
        except Exception as e:
            print(f"[ERROR] Napaka pri registraciji: {e}")
            return False
        finally:
            if conn:
                conn.close()



    @staticmethod
    def prijavi(email, geslo):
        """
        Prijavi uporabnika, preveri poverilnice in nastavi sejo.
        """
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                hashirano_geslo = Uporabnik._hash_geslo(geslo)

                # Step 1: Verify user exists and get basic info
                cursor.execute('''
                    SELECT userID, ime, priimek, email, role FROM users
                    WHERE email = %s AND geslo = %s;
                ''', (email, hashirano_geslo))
                user = cursor.fetchone()

                if user:
                    # Step 2: If role is employee, fetch employeeID from employees table
                    employee_id = None
                    if user[4] == 'employee':
                        cursor.execute('''
                            SELECT employeeID FROM employees WHERE email = %s;
                        ''', (email,))
                        employee_result = cursor.fetchone()
                        if employee_result:
                            employee_id = employee_result[0]
                        else:
                            print("[WARN] Employee not found in employees table.")

                    # Step 3: Set session with all info
                    session['user'] = {
                        'userID': user[0],
                        'ime': user[1],
                        'priimek': user[2],
                        'email': user[3],
                        'role': user[4],
                        'employeeID': employee_id
                    }

                    print(f"[INFO] Uporabnik {email} uspešno prijavljen.")
                    return True
                else:
                    print("[WARN] Napačen email ali geslo.")
                    return False

        except Exception as e:
            print(f"[ERROR] Napaka pri prijavi: {e}")
            return False
        finally:
            if conn:
                conn.close()


    @staticmethod
    def odjavi():
        """
        Odjavi uporabnika tako, da pobriše sejo.
        """
        session.pop('user', None)
        print("[INFO] Uporabnik odjavljen.")
        return True

    @staticmethod
    def je_prijavljen():
        """
        Preveri ali je uporabnik prijavljen.
        """
        return 'user' in session

    @staticmethod
    def pridobi_trenutnega_uporabnika():
        """
        Vrne podatke trenutnega prijavljenega uporabnika (če obstaja).
        """
        return session.get('user')
    
    @staticmethod
    def menjava_gesla(email, staro_geslo, novo_geslo):
        """
        Menja geslo za uporabnika, če je staro geslo pravilno.
        """
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                staro_hash = Uporabnik._hash_geslo(staro_geslo)

                # Preveri staro geslo
                cursor.execute("SELECT userID FROM users WHERE email = %s AND geslo = %s;", (email, staro_hash))
                user = cursor.fetchone()

                if not user:
                    print("[WARN] Napačno staro geslo.")
                    return False

                novo_hash = Uporabnik._hash_geslo(novo_geslo)
                cursor.execute("UPDATE users SET geslo = %s WHERE email = %s;", (novo_hash, email))
                conn.commit()
                print(f"[INFO] Geslo za {email} uspešno spremenjeno.")
                return True
        except Exception as e:
            print(f"[ERROR] Napaka pri menjavi gesla: {e}")
            return False
        finally:
            if conn:
                conn.close()
