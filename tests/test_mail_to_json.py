#!/usr/bin/env python3
"""Tests for the mail_to_json module."""
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')


def test_clean_body():
    """Test that clean_body properly cleans text."""
    # We'll test the clean_body function by importing it directly
    with patch('email_processing.mail_to_json.re'):
        from email_processing.mail_to_json import clean_body
        
        # Test input with citations and signatures
        test_input = "> This is a citation\n\nThis is real content\n\n--\nSignature line\nMore signature"
        result = clean_body(test_input)
        
        # The result should not contain the citation or signature
        assert "> This is a citation" not in result
        assert "--" not in result
        assert "Signature line" not in result
        assert "This is real content" in result


def test_has_attachment():
    """Test that has_attachment correctly identifies attachments."""
    from email_processing.mail_to_json import has_attachment
    
    # Create a mock message with an attachment
    mock_message = MagicMock()
    mock_part = MagicMock()
    mock_part.get_content_disposition.return_value = "attachment"
    mock_message.walk.return_value = [mock_part]
    
    result = has_attachment(mock_message)
    
    # Should return True when there's an attachment
    assert result is True