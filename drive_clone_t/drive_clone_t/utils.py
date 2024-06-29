def add_error(
    message: str,
    request,
    tag: str,
    url_name: str,
) -> None:
    """_summary_

    Args:
        message (str): 
        request (_type_): 
        tag (str): 
        url_name (str)
    """
    error_tag = f'error_{url_name}_{tag}'
    request.session[error_tag] = message
    

def get_errors(request, url_name: str)-> dict:
    """_summary_

    Args:
        request (_type_): _description_
        url_name (str): _description_

    Returns:
        dict: _description_
    """
    
    error_prefix_tag = f"error_{url_name}_"
    current_errors = {}
    
    for key in list(request.session.keys()):
        if error_prefix_tag in key:
            tag = key.replace(error_prefix_tag, "")
            current_errors[tag] = request.session.pop(key)
    
    return current_errors