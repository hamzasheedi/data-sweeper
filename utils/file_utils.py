def validate_file_type(file):
    """
    Validate if the uploaded file is of a supported type.
    
    Args:
        file: Uploaded file object
        
    Returns:
        bool: True if file type is supported, False otherwise
    """
    # Get the file extension
    file_name = file.name.lower()
    
    # Check if it's a supported file type
    supported_extensions = ['.csv', '.xlsx', '.xls']
    
    for ext in supported_extensions:
        if file_name.endswith(ext):
            return True
    
    return False


def get_file_extension(file):
    """
    Get the file extension from the file name.
    
    Args:
        file: Uploaded file object
        
    Returns:
        str: File extension (with dot)
    """
    file_name = file.name.lower()
    return '.' + file_name.split('.')[-1]


def sanitize_filename(filename):
    """
    Sanitize filename by removing problematic characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Replace problematic characters with underscores
    sanitized = filename.replace(' ', '_').replace('/', '_').replace('\\', '_')
    return sanitized