import unittest
import tempfile
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from unittest.mock import patch, mock_open
import sys
from io import StringIO

# Importez votre module ici
from mcps.email_processing.jsonise import clean_message, extract_body, clean_body, has_attachment, process_email, process_mbox, run_jsonise

class TestEmailProcessing(unittest.TestCase):

    def test_clean_message_with_valid_html(self):
        """Test du nettoyage HTML avec un HTML valide"""
        # Création d'un message email avec contenu HTML
        msg = MIMEText('<html><head><style>body {color: red;}</style></head><body><p>Hello <script>alert("test");</script> World!</p></body></html>', 'html')
        
        result = clean_message(msg)
        # Vérifie que le script et le style sont supprimés
        self.assertNotIn('script', result.lower())
        self.assertNotIn('color:', result.lower())
        self.assertIn('Hello', result)
        self.assertIn('World', result)

    def test_clean_message_with_invalid_html(self):
        """Test du nettoyage avec HTML invalide"""
        msg = MIMEText('<html><body><p>Invalid <tag>here</html>', 'html')
        result = clean_message(msg)
        # Doit retourner le HTML brut en cas d'erreur de parsing
        self.assertIn('Invalid', result)

    def test_clean_message_with_encoding_issues(self):
        """Test du nettoyage avec problèmes d'encodage"""
        # Création d'un message avec données brutes
        msg = MIMEText('Test message with encoding issues', 'plain')
        msg.set_payload(b'\xff\xfe invalid bytes')
        msg.set_charset('utf-8')
        
        result = clean_message(msg)
        # Devrait gérer les erreurs d'encodage
        self.assertIsInstance(result, str)

    def test_extract_body_plain_text(self):
        """Test de l'extraction du corps en texte brut"""
        msg = MIMEText('This is a plain text message', 'plain')
        
        result = extract_body(msg)
        self.assertEqual(result, 'This is a plain text message')

    def test_extract_body_html_text(self):
        """Test de l'extraction du corps HTML"""
        html_content = '<html><body><p>This is HTML content</p></body></html>'
        msg = MIMEText(html_content, 'html')
        
        result = extract_body(msg)
        # Doit appeler clean_message et retourner le texte nettoyé
        self.assertIn('This is HTML content', result)

    def test_extract_body_multipart(self):
        """Test de l'extraction du corps dans un message multipart"""
        msg = MIMEMultipart()
        
        # Ajouter une partie texte brut
        plain_part = MIMEText('Plain text part', 'plain')
        msg.attach(plain_part)
        
        # Ajouter une partie HTML
        html_part = MIMEText('<html><body><p>HTML part</p></body></html>', 'html')
        msg.attach(html_part)
        
        result = extract_body(msg)
        # Doit retourner la partie texte brut
        self.assertEqual(result, 'Plain text part')

    def test_clean_body_removes_quotes(self):
        """Test de la suppression des citations"""
        text = """Bonjour,
> Citer de l'autre personne
> Sur plusieurs lignes
Ceci est ma réponse
> Et une autre citation
Fin du message"""
        
        expected = """Bonjour,
Ceci est ma réponse
Fin du message"""
        
        result = clean_body(text)
        self.assertEqual(result, expected)

    def test_clean_body_removes_signature(self):
        """Test de la suppression des signatures"""
        text = """Bonjour,
Ceci est le contenu du message.

--
Signature
Contact info"""
        
        expected = """Bonjour,
Ceci est le contenu du message."""
        
        result = clean_body(text)
        self.assertEqual(result, expected)

    def test_clean_body_collapses_blank_lines(self):
        """Test de la réduction des lignes blanches multiples"""
        text = "Ligne 1\n\n\n\nLigne 2\n\nLigne 3"
        expected = "Ligne 1\n\nLigne 2\n\nLigne 3"
        
        result = clean_body(text)
        self.assertEqual(result, expected)

    def test_has_attachment_with_attachment(self):
        """Test de détection des pièces jointes"""
        msg = MIMEMultipart()
        
        # Ajouter une pièce jointe
        attachment = MIMEBase('application', 'octet-stream')
        attachment.add_header('Content-Disposition', 'attachment', filename='test.txt')
        msg.attach(attachment)
        
        self.assertTrue(has_attachment(msg))

    def test_has_attachment_without_attachment(self):
        """Test de non-détection des pièces jointes"""
        msg = MIMEMultipart()
        
        # Ajouter une partie normale
        part = MIMEText('Regular content', 'plain')
        msg.attach(part)
        
        self.assertFalse(has_attachment(msg))

    def test_process_email_basic(self):
        """Test du traitement complet d'un email"""
        msg = MIMEText('This is the body', 'plain')
        msg['From'] = 'sender@example.com'
        msg['Subject'] = 'Test Subject'
        msg['Date'] = 'Mon, 01 Jan 2026 12:00:00 +0000'
        
        result = process_email(msg)
        data = json.loads(result)
        
        self.assertEqual(data['from'], 'sender@example.com')
        self.assertEqual(data['subject'], 'Test Subject')
        self.assertEqual(data['date'], 'Mon, 01 Jan 2026 12:00:00 +0000')
        self.assertEqual(data['body'], 'This is the body')



    @patch('mailbox.mbox')
    @patch('builtins.open', new_callable=mock_open, read_data='mbox:\n  path: /test/path')
    @patch('os.path.isfile', return_value=True)
    def test_process_mbox(self, mock_isfile, mock_file, mock_mbox):
        """Test du traitement d'un fichier mbox"""
        # Créer un message de test
        msg = MIMEText('Test body', 'plain')
        msg['From'] = 'sender@example.com'
        msg['Subject'] = 'Test Subject'
        msg['Date'] = 'Mon, 01 Jan 2026 12:00:00 +0000'
        
        mock_mbox_instance = mock_mbox.return_value.__iter__.return_value
        mock_mbox_instance.__iter__.return_value = [msg]
        
        # Capturer stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            process_mbox('/test/path')
            output = captured_output.getvalue()
            
            # Vérifier que le JSON est imprimé
            self.assertIn('Test Subject', output)
            self.assertIn('sender@example.com', output)
        finally:
            sys.stdout = old_stdout

    @patch('builtins.open', new_callable=mock_open, read_data='mbox:\n  path: /test/path')
    @patch('os.path.isfile', side_effect=lambda x: x == '/test/path')
    def test_process_mbox_not_found(self, mock_isfile, mock_file):
        """Test du traitement d'un fichier mbox inexistant"""
        with self.assertRaises(SystemExit):
            process_mbox('/nonexistent/path')

    @patch('builtins.open', new_callable=mock_open, read_data='mbox:\n  SRC: "test"\n  path: /test/path')
    @patch('os.path.isfile', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_jsonise_success(self, mock_stdout, mock_isfile, mock_file):
        """Test de l'exécution réussie de run_jsonise"""
        # Simuler le processus mbox
        with patch('mailbox.mbox') as mock_mbox:
            msg = MIMEText('Test body', 'plain')
            msg['From'] = 'sender@example.com'
            msg['Subject'] = 'Test Subject'
            msg['Date'] = 'Mon, 01 Jan 2026 12:00:00 +0000'

            mock_mbox_instance = mock_mbox.return_value.__iter__.return_value
            mock_mbox_instance.__iter__.return_value = [msg]

            result = run_jsonise()
            # Vérifier que le résultat contient la clé 'output'
            self.assertIn('output', result)
            self.assertIn('écrit un résumé de 80 mots', result['output'])

    @patch('builtins.open', new_callable=mock_open, read_data='invalid: config: yaml')
    @patch('os.path.isfile', return_value=True)
    def test_run_jsonise_config_error(self, mock_isfile, mock_file):
        """Test de run_jsonise avec erreur de configuration"""
        result = run_jsonise()
        
        # Doit contenir une clé 'error'
        self.assertIn('error', result)

    def test_clean_body_empty_string(self):
        """Test de clean_body avec une chaîne vide"""
        result = clean_body("")
        self.assertEqual(result, "")

    def test_clean_body_only_quotes(self):
        """Test de clean_body avec seulement des citations"""
        text = "> Citation 1\n> Citation 2\n> Citation 3"
        result = clean_body(text)
        self.assertEqual(result, "")

    def test_clean_body_only_signature(self):
        """Test de clean_body avec seulement une signature"""
        text = "Ligne 1\nLigne 2\n--\nSignature"
        result = clean_body(text)
        self.assertEqual(result, "Ligne 1\nLigne 2")

    def test_process_email_with_long_words(self):
        """Test du filtrage des mots longs dans process_email"""
        long_word = "a" * 20  # Mot de 20 caractères
        msg = MIMEText(f'This is a {long_word} test message', 'plain')
        
        result = process_email(msg)
        data = json.loads(result)
        
        # Le mot long devrait être supprimé
        self.assertNotIn(long_word, data['body'])
        self.assertIn('This is a test message', data['body'])

    @patch('mcps.email_processing.jsonise.get_config_value')
    def test_run_jsonise_missing_config_values(self, mock_get_config):
        """Test de run_jsonise avec des valeurs de configuration manquantes"""
        # Mock config with SRC but no path
        mock_get_config.return_value = {"SRC": "test"}

        result = run_jsonise()

        self.assertIn('error', result)
        self.assertIn('SRC ou path non défini', result['error'])

if __name__ == '__main__':
    # Pour exécuter les tests, assurez-vous que votre module est importable
    # Remplacez 'votre_module' par le nom réel de votre fichier
    # import votre_module
    # globals().update(votre_module.__dict__)
    
    unittest.main()
