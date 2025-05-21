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
        Registrira uporabnika in shrani v PostgreSQL bazo.
        """
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                hashirano_geslo = Uporabnik._hash_geslo(geslo)
                cursor.execute('''
                    INSERT INTO users (ime, priimek, email, geslo)
                    VALUES (%s, %s, %s, %s);
                ''', (ime, priimek, email, hashirano_geslo))
                conn.commit()
            print(f"[INFO] Uporabnik {email} uspešno registriran.")
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
                cursor.execute('''
                    SELECT userID, ime, priimek, email FROM users
                    WHERE email = %s AND geslo = %s;
                ''', (email, hashirano_geslo))
                user = cursor.fetchone()

                if user:
                    # Shrani uporabnika v sejo
                    session['user'] = {
                        'userID': user[0],
                        'ime': user[1],
                        'priimek': user[2],
                        'email': user[3]
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
