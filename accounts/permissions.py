from .models import User

def is_admin(u): return u.is_authenticated and u.actif and u.role == User.Role.ADMIN
def is_resp(u): return u.is_authenticated and u.actif and u.role == User.Role.RESP_PEDAGO
def is_etudiant(u): return u.is_authenticated and u.actif and u.role == User.Role.ETUDIANT
def is_entreprise(u): return u.is_authenticated and u.actif and u.role == User.Role.ENTREPRISE
