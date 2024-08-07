from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
# from solana.keypair import Keypair
from solana.transaction import Transaction
from solders.instruction import Instruction
# from solana.system_program import SYS_PROGRAM_ID
from solana.rpc.types import TxOpts
from dotenv import load_dotenv
import base64
import os

def load_private_key():
    # Load environment variables from .env file
    load_dotenv()

    # Access the environment variables
    secret_key_byte_array_string = os.getenv('SECRET_KEY')

    # Remove brackets and split the string by commas
    secret_key_byte_array_string = secret_key_byte_array_string.strip("[]")
    secret_key_byte_array_string = secret_key_byte_array_string.strip("''")
    byte_array_list = secret_key_byte_array_string.split(",")

    # Convert to byte array
    scretkey_byte_array = bytearray(int(byte) for byte in byte_array_list)

    return scretkey_byte_array




def main():
    ba_secretkey = load_private_key()

    net_url = os.getenv('NET_URL')

    # Initialize the Solana client
    client = Client(net_url)

    # Load your wallet keypair
    keypair = Keypair.from_bytes(ba_secretkey)

    print(f"address: {keypair.pubkey()}")
    balance = client.get_balance(keypair.pubkey())
    print(f"Balance: {balance.value / 1000000000} SOL")

    # Raydium Program ID
    RAYDIUM_PROGRAM_ID = Pubkey.from_string("HWy1jotHpo6UqeQxx49dpYYdQB8wj9Qk9MdxwjLvDHB8")
    POOL_ID = Pubkey.from_string("BbZjQanvSaE9me4adAitmTTaSgASvzaVignt4HRSM7ww")
    Input_Token_Mint = Pubkey.from_string("GfmdKWR1KrttDsQkJfwtXovZw9bUBHYkPAEwB6wZqQvJ") # SPL Token
    Output_Token_Mint = Pubkey.from_string("2SiSpNowr7zUv5ZJHuzHszskQNaskWsNukhivCtuVLHo") # SPL Token
    slippage = 50 # 0.5%

    byte_array_list = ['0']
    byte_array = bytearray(int(byte) for byte in byte_array_list)
    instruction_data = byte_array

    swap_instruction = Instruction(
        accounts=[
            {"pubkey": keypair.pubkey(), "is_signer": True, "is_writable": True},
            {"pubkey": Input_Token_Mint, "is_signer": False, "is_writable": True},
            {"pubkey": Output_Token_Mint, "is_signer": False, "is_writable": True},
            # Add other necessary accounts based on Raydium's requirements
        ],
        program_id=RAYDIUM_PROGRAM_ID,
        data=instruction_data
    )

    # Create and send the transaction
    transaction = Transaction().add(swap_instruction)
    response = client.send_transaction(transaction, keypair, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed"))
    print("Transaction Response:", response)

if __name__ == "__main__":
    main()