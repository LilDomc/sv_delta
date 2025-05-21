import db
import hashlib

class Uporabnik:
    def __init__(self, email, geslo):
        self.email = email
        self.geslo = geslo

    @staticmethod
    def _hash_geslo(geslo):
        return hashlib.sha256(geslo.encode()).hexdigest()

    @staticmethod
    def registriraj(ime, priimek, email, geslo):
        """
        Registrira uporabnika in shrani podatke v bazo.
        """
        try:
            conn = db.get_connection()
            cursor = conn.cursor()

            hashirano_geslo = Uporabnik._hash_geslo(geslo)

            cursor.execute('''
                INSERT INTO users (ime, priimek, email, geslo)
                VALUES (%s, %s, %s, %s);
            ''', (ime, priimek, email, hashirano_geslo))

            conn.commit()
            cursor.close()
            conn.close()
            print(f"Uporabnik {email} uspešno registriran.")
            return True

        except Exception as e:
            print(f"Napaka pri registraciji: {e}")
            return False

    @staticmethod
    def prijavi(email, geslo):
        """
        Preveri, če obstaja uporabnik z ustreznim emailom in geslom.
        """
        try:
            conn = db.get_connection()
            cursor = conn.cursor()

            hashirano_geslo = Uporabnik._hash_geslo(geslo)

            cursor.execute('''
                SELECT * FROM users
                WHERE email = %s AND geslo = %s;
            ''', (email, hashirano_geslo))

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                print(f"Uporabnik {email} uspešno prijavljen.")
                return True
            else:
                print("Napačen email ali geslo.")
                return False

        except Exception as e:
            print(f"Napaka pri prijavi: {e}")
            return False

    @staticmethod
    def odjavi():
        """
        Simulacija odjave uporabnika (v resnici bi odstranil session/cookie).
        """
        print("Uporabnik je bil odjavljen.")
        return True

    @staticmethod
    def je_prijavljen():
        """
        Preveri prijavo (trenutno le simulacija).
        """
        print("Preverjanje stanja prijave (simulacija).")
        return False
