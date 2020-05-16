def clean_data(data: dict):
    """
    Clear income from db data from service info
    Args:
        data:

    Returns:

    """
    del data['_id']
    return data


async def get_next_sequence_value(db, sequence_id):
    sequence = await db.counters.find_one_and_update(
        {"_id": f"{sequence_id}"},
        {"$inc": {"sequence_value": 1}}, new=True)
    return sequence['sequence_value']
