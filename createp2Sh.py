from os import times
from bitcoinutils.setup import setup

from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Locktime, Sequence
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_ABSOLUTE_TIMELOCK

# compute redeem script
def create_redeem_script(time_lock_type,pub_key):
    redeem_script=Script([ time_lock_type.for_script(),'OP_CHECKLOCKTIMEVERIFY', 'OP_DROP', 'OP_DUP', 'OP_HASH160', pub_key.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
    return redeem_script
    
# Create P2SH address from Redeem Script
def create_P2SH_address(redeem_script):
    p2sh_addr=P2shAddress.from_script(redeem_script)
 
    # Print P2SH Address
    # print(p2sh_addr.to_string())
    return p2sh_addr.to_string()

def main():
    
    setup('testnet') #setup network to work with
    
    # Accept Inputs
    # nLockTime time in block heights
    f_t_str=input("Enter spendable future time in block height \n")
    nLockTimeInBlocks=int(f_t_str)
    
    # P2PKH address
    pub_key_input=input("Please enter a Public Key \n")
    pub_key=P2pkhAddress(pub_key_input)
    pub_k=pub_key.get_address()
    
    # Specify timelock type as Absolute
    seq=Sequence(TYPE_ABSOLUTE_TIMELOCK,nLockTimeInBlocks)
    
    # call the create Pay to Script Hash Address (create_P2SH_address) function to create the P2SH address
    create_P2SH_address(create_redeem_script(seq,pub_k)) 
    
if __name__=="__main__":
    main()