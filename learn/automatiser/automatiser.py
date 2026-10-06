"""
Démo Selenium — Remplissage automatique du formulaire demoqa.com
Remplit le "Student Registration Form" avec un profil fictif complet.
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ═══════════════════════════════════════════════════════════════════
# 1. PROFIL ÉTUDIANT FICTIF
# ═══════════════════════════════════════════════════════════════════

PROFIL = {
    "prenom": "Marie",
    "nom": "Dupont",
    "email": "marie.dupont@example.com",
    "genre": "Female",  # Male | Female | Other
    "telephone": "0612345678",  # 10 chiffres
    "date_naissance": "15 Mar 1995",
    "matieres": ["Maths", "English"],
    "hobbies": ["Sports", "Reading"],  # Sports | Reading | Music
    "adresse": "42 rue de la Paix, 75002 Paris",
    "etat": "NCR",
    "ville": "Delhi",
}

# ═══════════════════════════════════════════════════════════════════
# 2. LANCEMENT DU NAVIGATEUR
# ═══════════════════════════════════════════════════════════════════

URL = "https://demoqa.com/automation-practice-form"

options = Options()
options.add_argument("--window-size=1280,900")
options.add_argument("--disable-search-engine-choice-screen")

driver = webdriver.Chrome(options=options)
driver.get(URL)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "userForm")))

# Supprimer le footer, les pubs et les iframes qui bloquent les clics
driver.execute_script("""
    document.querySelector('footer')?.remove();
    document.getElementById('fixedban')?.remove();
    document.getElementById('Ad.Plus-970x250-2')?.remove();
    document.getElementById('Ad.Plus-300x250-1')?.remove();
    document.getElementById('Ad.Plus-300x250-2')?.remove();
    document.querySelectorAll('[id*="google_ads"]').forEach(el => el.remove());
    document.querySelectorAll('iframe').forEach(el => el.remove());
""")

print("Page chargée — début du remplissage\n")


def scroll_to(element):
    """Scroll l'élément au centre de l'écran avant interaction."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.3)


def js_click(element):
    """Clic via JavaScript — contourne les overlays publicitaires."""
    driver.execute_script("arguments[0].click();", element)


# ═══════════════════════════════════════════════════════════════════
# 3. REMPLISSAGE DU FORMULAIRE
# ═══════════════════════════════════════════════════════════════════

# --- Prénom et Nom ---
driver.find_element(By.ID, "firstName").send_keys(PROFIL["prenom"])
driver.find_element(By.ID, "lastName").send_keys(PROFIL["nom"])
print(f"  ✓ Nom : {PROFIL['prenom']} {PROFIL['nom']}")
time.sleep(0.5)

# --- Email ---
driver.find_element(By.ID, "userEmail").send_keys(PROFIL["email"])
print(f"  ✓ Email : {PROFIL['email']}")
time.sleep(0.5)

# --- Genre (clic sur le label du radio bouton) ---
GENRE_MAP = {"Male": "gender-radio-1", "Female": "gender-radio-2", "Other": "gender-radio-3"}
radio_id = GENRE_MAP[PROFIL["genre"]]
js_click(driver.find_element(By.CSS_SELECTOR, f"label[for='{radio_id}']"))
print(f"  ✓ Genre : {PROFIL['genre']}")
time.sleep(0.5)

# --- Téléphone ---
driver.find_element(By.ID, "userNumber").send_keys(PROFIL["telephone"])
print(f"  ✓ Téléphone : {PROFIL['telephone']}")
time.sleep(0.5)

# --- Date de naissance (on efface la valeur par défaut puis on tape la date) ---
date_input = driver.find_element(By.ID, "dateOfBirthInput")
scroll_to(date_input)
date_input.click()
time.sleep(0.3)

date_input.send_keys(Keys.CONTROL, "a")
date_input.send_keys(PROFIL["date_naissance"])
date_input.send_keys(Keys.ENTER)
print(f"  ✓ Date de naissance : {PROFIL['date_naissance']}")
time.sleep(0.5)

# --- Matières (champ autocomplete : on tape puis on sélectionne) ---
subjects_input = driver.find_element(By.ID, "subjectsInput")
scroll_to(subjects_input)
for matiere in PROFIL["matieres"]:
    subjects_input.send_keys(matiere)
    time.sleep(0.5)
    subjects_input.send_keys(Keys.ENTER)
print(f"  ✓ Matières : {', '.join(PROFIL['matieres'])}")
time.sleep(0.5)

# --- Hobbies (clic sur le label de chaque checkbox) ---
HOBBY_MAP = {"Sports": "hobbies-checkbox-1", "Reading": "hobbies-checkbox-2", "Music": "hobbies-checkbox-3"}
for hobby in PROFIL["hobbies"]:
    checkbox_id = HOBBY_MAP[hobby]
    label = driver.find_element(By.CSS_SELECTOR, f"label[for='{checkbox_id}']")
    scroll_to(label)
    js_click(label)
    time.sleep(0.3)
print(f"  ✓ Hobbies : {', '.join(PROFIL['hobbies'])}")
time.sleep(0.5)

# --- Adresse ---
address_field = driver.find_element(By.ID, "currentAddress")
scroll_to(address_field)
address_field.send_keys(PROFIL["adresse"])
print(f"  ✓ Adresse : {PROFIL['adresse']}")
time.sleep(0.5)

# --- État (React-Select : focus JS sur l'input caché, puis frappe clavier) ---
state_wrapper = driver.find_element(By.ID, "stateCity-wrapper")
scroll_to(state_wrapper)

state_input = driver.find_element(By.ID, "react-select-3-input")
driver.execute_script("arguments[0].focus();", state_input)
time.sleep(0.5)
state_input.send_keys(PROFIL["etat"])
time.sleep(0.8)
state_input.send_keys(Keys.ENTER)
print(f"  ✓ État : {PROFIL['etat']}")
time.sleep(1)

# --- Ville (React-Select : activé après sélection de l'état) ---
city_input = driver.find_element(By.ID, "react-select-4-input")
driver.execute_script("arguments[0].focus();", city_input)
time.sleep(0.5)
city_input.send_keys(PROFIL["ville"])
time.sleep(0.8)
city_input.send_keys(Keys.ENTER)
print(f"  ✓ Ville : {PROFIL['ville']}")
time.sleep(0.5)

# ═══════════════════════════════════════════════════════════════════
# 4. SOUMISSION DU FORMULAIRE
# ═══════════════════════════════════════════════════════════════════

submit_btn = driver.find_element(By.ID, "submit")
scroll_to(submit_btn)
js_click(submit_btn)
print("\n  → Formulaire soumis !")

# Attendre la modale de confirmation
try:
    wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
    print("  → Modale de confirmation affichée ✓")
except Exception:
    print("  → Pas de modale détectée (vérifier le formulaire)")

time.sleep(5)
driver.quit()
print("\nNavigateur fermé — démo terminée.")
