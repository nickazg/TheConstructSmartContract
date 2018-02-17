from construct.common.StorageManager import StorageManager
from boa.code.builtins import list

class SmartTokenShare():
    """
    Interface for managing a Smart Token Share (STS). Based on NEP5 token, however all values 
    are dymanically stored in the contract storage.
    """
    project_id = ''
    symbol = ''
    decimals = 0
    owner = ''
    total_supply = 0
    in_circulation = 0

def sts_create(project_id, symbol, decimals, owner, total_supply) -> SmartTokenShare:
    """
    Args:
        project_id (str):
            ID for referencing the project

        symbol (str):
            Representation symbol
            
        decimals (int):
            Amount of decimal places, default 8

        owner (bytes):
            Owner of the token

        total_supply (int):
            total supply of the token
    Return:
        (None): 
    """
    storage = StorageManager()
    sts = SmartTokenShare()

    sts.project_id = ''
    sts.symbol = ''
    sts.decimals = 0
    sts.owner = ''
    sts.total_supply = 0
    
    # Default circulation
    sts.in_circulation = 0

    # Info structure
    sts_info = [symbol, decimals, owner, total_supply, sts.in_circulation]

    # Will only save to storage if none exsits for this project_id
    if not storage.get_double('STS', project_id):
        sts_info_serialized = storage.serialize_array(sts_info)
        storage.put_double('STS', project_id, sts_info_serialized)

    return sts

def sts_get(project_id:str) -> SmartTokenShare:
    """
    Get the info list

    Args:
        project_id (str):
            ID for referencing the project
    Return:
        (list): info list
    """    
    storage = StorageManager()
    sts = SmartTokenShare()
    
    # Pull STS info
    sts_info_serialized = storage.get_double('STS', project_id)
    sts_info = storage.deserialize_bytearray(sts_info_serialized)

    # info into vars
    sts.symbol = sts_info[0]
    sts.decimals = sts_info[1]
    sts.owner = sts_info[2]
    sts.total_supply = sts_info[3]
    sts.in_circulation = sts_info[4]

    return sts

def sts_total_available_amount(sts:SmartTokenShare):
    """
    Args:
        project_id (str):
            ID for referencing the project
    Return:
        (int): The avaliable tokens for the total project
    """
    available = sts.supply - sts.in_circulation

    return available

def sts_add_to_total_circulation(sts:SmartTokenShare, amount:int):
    """
    Adds an amount of token to circlulation

    Args:
        project_id (str):
            ID for referencing the project
        amount (int):
            amount of tokens added
    """
    storage = StorageManager()
    
    # Calculation
    sts.in_circulation = sts.in_circulation + amount 

    # output STS info
    updated_sts_info = [sts.symbol, sts.decimals, sts.owner, sts.total_supply, sts.in_circulation]
    
    # Save STS info
    updated_sts_info_serialized = storage.serialize_array(updated_sts_info)
    storage.put_double('STS', sts.project_id, updated_sts_info_serialized)    

def sts_get_total_circulation(sts:SmartTokenShare):
    """
    Get the total amount of tokens in circulation

    Args:
        project_id (str):
            ID for referencing the project
    Return:
        (int): The total amount of tokens in circulation
    """        
    return sts.in_circulation

