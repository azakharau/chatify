def clean_data(data: dict):
    """
    Clear income from db data from service info
    Args:
        data:

    Returns:

    """
    del data['_id']
    return data
