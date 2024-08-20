# ./sort_opts_by_phase.py

def sort_opts_by_phase(data):
    """
    Sorts the 'opts' key in the data by phase.
    
    Args:
        data (dict): The JSON data containing an 'opts' key.

    Returns:
        dict: The input data with the 'opts' key sorted by phase.
    """
    if "opts" in data:
        data["opts"].sort(key=lambda opt: opt.get("opt_txt", ""))
    return data
