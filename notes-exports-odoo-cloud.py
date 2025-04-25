import xmlrpc.client
import csv
from datetime import datetime

# 🔐 Paramètres de connexion à Odoo
url = "https://votre-domaine.odoo.com"   # Remplacez par votre URL
db = "votre_base_de_donnees"             # Remplacez par votre base
username = "votre.email@domaine.com"     # Remplacez par votre identifiant
password = "api-token"                   # Remplacez par votre token d'API Odoo Cloud

# 📡 Connexion aux endpoints XML-RPC
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# 🔎 Vérification de l'authentification
if not uid:
    raise Exception("❌ Échec de l'authentification auprès de l'instance Odoo. Veuillez vérifier vos identifiants.")

# 📋 Vérification de l'existence du modèle 'note.note'
model_list = models.execute_kw(db, uid, password, 'ir.model', 'search_read',
    [[('model', '=', 'note.note')]],
    {'fields': ['model', 'name']})

# 📒 Extraction des notes personnelles si possible
notes = []
if model_list:
    print("✅ Le modèle 'note.note' existe. Extraction des notes personnelles...")
    notes = models.execute_kw(db, uid, password,
        'note.note', 'search_read',
        [[]],
        {'fields': ['name', 'memo', 'create_date', 'write_date']})
else:
    print("⚠️ Le modèle 'note.note' n'existe pas. Passage aux notes du Chatter uniquement.")

# 🧾 Extraction des messages internes du Chatter
print("✅ Extraction des commentaires internes ('mail.message')...")
messages = models.execute_kw(db, uid, password,
    'mail.message', 'search_read',
    [[('message_type', '=', 'comment')]],
    {'fields': ['model', 'res_id', 'date', 'body', 'author_id']})

# 📂 Exportation vers fichier CSV avec encodage UTF-8 BOM et séparateur "£"
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
filename = f"odoo_notes_export_{timestamp}.csv"

print(f"💾 Génération du fichier CSV (UTF-8 BOM, séparateur £) : {filename}")

with open(filename, mode='w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter='£', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Source', 'Objet lié', 'ID de l\'objet', 'Auteur', 'Date', 'Contenu'])

    # Ajout des notes personnelles si disponibles
    for note in notes:
        writer.writerow([
            'note.note',
            note.get('name', ''),
            '',
            '',
            note.get('create_date', ''),
            note.get('memo', '').replace('\n', ' ').replace('\r', '')
        ])

    # Ajout des messages internes (Chatter)
    for msg in messages:
        writer.writerow([
            f"mail.message ({msg.get('model', '')})",
            msg.get('model', ''),
            msg.get('res_id', ''),
            msg.get('author_id', [])[1] if msg.get('author_id') else '',
            msg.get('date', ''),
            msg.get('body', '').replace('\n', ' ').replace('\r', '')
        ])

print(f"\n✅ Export terminé avec succès. Fichier généré : {filename}")
