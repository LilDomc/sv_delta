class Uporabnik:
    def __init__(self, email, geslo):
        self.email = email
        self.geslo = geslo

    @staticmethod
    def registriraj(ime, priimek, email, geslo):
        """
        Registrira uporabnika.
        Trenutno samo simulira uspešno registracijo.
        """
        print(f"Registracija uporabnika: {email}")
        # Tukaj bi bila logika za vpis v bazo
        return True

    @staticmethod
    def prijavi(email, geslo):
        """
        Prijavi uporabnika.
        Trenutno samo simulira uspešno prijavo.
        """
        print(f"Prijava uporabnika: {email}")
        # Tukaj bi bila logika za preverjanje emaila in gesla v bazi
        return True

    @staticmethod
    def odjavi():
        """
        Odjavi uporabnika.
        Trenutno samo simulira odjavo.
        """
        print("Uporabnik odjavljen")
        # Tukaj bi izbrisal podatke iz seje
        return True

    @staticmethod
    def je_prijavljen():
        """
        Preveri, ali je uporabnik trenutno prijavljen.
        Trenutno samo simulira stanje.
        """
        print("Preverjanje prijave")
        # V resnici bi pogledal v session ali cookie
        return False  # Spremeni na True za test
