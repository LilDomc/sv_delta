import hashlib
from flask import session
import datetime
import db  # predpostavljam, da imaš funkcijo get_connection() v tej datoteki

class Uporabnik:
    def __init__(self, email, geslo):
        self.email = email
        self.geslo = geslo

    @staticmethod
    def _hash_geslo(geslo):
        """Vrne SHA-256 hash gesla."""
        return hashlib.sha256(geslo.encode()).hexdigest()

    @staticmethod
    def registriraj(ime, priimek, email, geslo):
        """Registrira uporabnika, če še ne obstaja z enakim emailom."""
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT userID FROM users WHERE email = %s;", (email,))
                if cursor.fetchone():
                    print(f"[WARN] Uporabnik z emailom {email} že obstaja.")
                    return "Uporabnik s tem e-poštnim naslovom že obstaja."

                hashirano_geslo = Uporabnik._hash_geslo(geslo)
                employee_id = None
                role = 'user'

                cursor.execute("SELECT employeeID FROM employees WHERE email = %s;", (email,))
                rezultat = cursor.fetchone()
                if rezultat:
                    employee_id = rezultat[0]
                    role = 'employee'

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
        """Prijavi uporabnika, preveri poverilnice in nastavi sejo."""
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                hashirano_geslo = Uporabnik._hash_geslo(geslo)
                cursor.execute('''
                    SELECT userID, ime, priimek, email, role FROM users
                    WHERE email = %s AND geslo = %s;
                ''', (email, hashirano_geslo))
                user = cursor.fetchone()

                if user:
                    session['user'] = {
                        'userID': user[0],
                        'ime': user[1],
                        'priimek': user[2],
                        'email': user[3],
                        'role': user[4]
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
        """Odjavi uporabnika tako, da pobriše sejo."""
        session.pop('user', None)
        print("[INFO] Uporabnik odjavljen.")
        return True

    @staticmethod
    def je_prijavljen():
        """Preveri ali je uporabnik prijavljen."""
        return 'user' in session

    @staticmethod
    def pridobi_trenutnega_uporabnika():
        """Vrne podatke trenutnega prijavljenega uporabnika (če obstaja)."""
        return session.get('user')

    @staticmethod
    def menjava_gesla(email, staro_geslo, novo_geslo):
        """Menja geslo za uporabnika, če je staro geslo pravilno."""
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                staro_hash = Uporabnik._hash_geslo(staro_geslo)
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

    @staticmethod
    def poisci_po_emailu(email):
        """Vrne uporabnika po emailu ali None."""
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                uporabnik = cur.fetchone()
                return uporabnik
        except Exception as e:
            print(f"[ERROR] Napaka pri iskanju po emailu: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def spremeni_geslo(email, novo_geslo):
        """Nastavi novo geslo za uporabnika brez preverjanja starega."""
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cur:
                novo_hash = Uporabnik._hash_geslo(novo_geslo)
                cur.execute("UPDATE users SET geslo = %s WHERE email = %s", (novo_hash, email))
                conn.commit()
                print(f"[INFO] Geslo za {email} uspešno posodobljeno.")
                return True
        except Exception as e:
            print(f"[ERROR] Napaka pri spreminjanju gesla: {e}")
            return False
        finally:
            if conn:
                conn.close()
    @staticmethod
    def najdi_po_emailu(email):
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                uporabnik = cursor.fetchone()
                return uporabnik
        finally:
            conn.close()

    @staticmethod
    def shrani_reset_token(email, token):
        conn = None
        try:
            conn = db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO password_reset_tokens (token, email, created_at)
                    VALUES (%s, %s, %s)
                """, (token, email, datetime.datetime.utcnow()))
                conn.commit()
        except Exception as e:
            print(f"[ERROR] Napaka pri shranjevanju reset tokena: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def preveri_reset_token(token):
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT email FROM password_reset_tokens
                    WHERE token = %s AND created_at > (NOW() - INTERVAL '1 hour')
                """
                cursor.execute(sql, (token,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                return None
        finally:
            conn.close()

    @staticmethod
    def odstrani_reset_token(token):
        """Izbriše token iz baze, ko je uporabljen."""
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM password_reset_tokens WHERE token = %s", (token,))
                conn.commit()
        except Exception as e:
            print(f"[ERROR] Napaka pri brisanju reset tokena: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def spremeni_geslo(email, novo_geslo):
        """Spremeni geslo uporabnika (predpostavljam, da ga moraš še predhodno hashrati)."""

        hashrano_geslo = Uporabnik._hash_geslo(novo_geslo)
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET geslo = %s WHERE email = %s", (hashrano_geslo, email))
                conn.commit()
        except Exception as e:
            print(f"[ERROR] Napaka pri spremembi gesla: {e}")
        finally:
            if conn:
                conn.close()
    @staticmethod
    def vrni_vse_reset_token():
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                cursor.execute('''SELECT token, email, created_at FROM password_reset_tokens;''')
                rezultati = cursor.fetchall()
                return rezultati  # seznam dict-ov s ključi: token, email, created_at
        except Exception as e:
            print(f"[ERROR] Napaka pri pridobivanju reset tokenov: {e}")
            return []
        finally:
            if conn:
                conn.close()
    @staticmethod
    def getTokenID(token):
        conn = None
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                cursor.execute('''SELECT id_token FROM password_reset_tokens WHERE token = %s''', (token,))
                rezultat = cursor.fetchone()
                if rezultat:
                    return rezultat[0]  # vrni samo id_token
                else:
                    return None  # če ni najden
        except Exception as e:
            print(f"[ERROR] Napaka pri pridobivanju reset tokenov: {e}")
            return None
        finally:
            if conn:
                conn.close()


