from bitcoin import transaction
import bitcoin
import bitcoinutils
from bitcoinutils.utils import to_satoshis
from bitcoinutils import transactions
from bitcoinrpc.authproxy import  AuthServiceProxy, JSONRPCException
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Locktime, Sequence, Transaction, TxInput, TxOutput, TxOutput, Locktime, Sequence
from bitcoinutils.keys import P2shAddress, P2pkhAddress, P2wshAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_ABSOLUTE_TIMELOCK
from createp2Sh import create_redeem_script, create_P2SH_address

def spend_frm_P2SH_add(conn,seq,p2sh_address,p2sh_prvk,redeem_script,p2pkh_address):
        
        # check p2sh_address if UTXOs is available
        unspent=conn.listunspent(6,9999999, [p2pkh_address])
        # unspent=bitcoin.unspent()
        if len(unspent)==0:
            print("There are no spendable coins", unspent)
            return
        else:
            txinput=None
            tot_amnt_to_spend=0
            for txs in unspent:
                txid=txs['txid']
                vout=txs['vout']
                
                txinput+=TxInput(txid,vout,sequence=seq.for_input_sequence())
                tot_amnt_to_spend+=txs['amount']
            
            # spend funds
            # print(txinput)
             
            
            txOutput=TxOutput(to_satoshis(tot_amnt_to_spend),p2pkh_address.to_script_pub_key())
            print(txOutput)
            
            
        # Send funds to from p2sh_add to p2pkh_address
            coins_spend_trx=Transaction([txinput],[txOutput])
            
            print('Transaction details \n.......................\n',coins_spend_trx)
        
        # calculate fees with respect to transaction size
            transaction_fee=conn.estimaterawfee(6)
            print('Transaction Fee:',transaction_fee)
        
        # display raw unsigned transaction
            print('\n Raw unsigned transaction \n........................................................\n', coins_spend_trx)
       
        # sign the transaction
            signature=p2sh_prvk.sign_input(coins_spend_trx,0,redeem_script)
            print("Signature \n .........................................\n",signature)
            txinput.script_sig=Script([signature, p2sh_prvk.get_public_key().to_hex(),redeem_script.to_hex()])
            signed_coins_spend_trx=coins_spend_trx.serialize()
        
        # display the raw signed transaction
        print('Signed Raw Transaction\n...........................................\n',signed_coins_spend_trx)
        # display the transaction id
        trx_id=coins_spend_trx.get_txid()
        print('Transaction id\n...........................................\n',trx_id)
        # verify transaction id if valid and acceptable by bitocin nodes
        
        
        # send transaction with the above valid transaction to the blockchain
        conn.sendrawtransaction(trx_id)
        # return validated transaction
        return coins_spend_trx
        
def main():
    setup('testnet') 
    
    # Accept Inputs
    # nLockTime time in block heights
    user = "iniakpothompson"
    pw = "iniakpothompson"
    # create connection
    conn=AuthServiceProxy("http://%s:%s@127.0.0.1:18332"%(user, pw))
    # Accept Spendable Future Time from user
    f_t_str=input("Enter spendable future time in block height \n")
    lockTime=int(f_t_str)
    
    # Accept Private Key frome user
    user_priv_key=input('Please enter private key:> \n')
    priv_key=PrivateKey(user_priv_key)
    
    # Specify timelock type as Absolute
    seq=Sequence(TYPE_ABSOLUTE_TIMELOCK,lockTime)
    
    # get public_key_address
    pub_key_address=priv_key.get_public_key().get_address()
    print('Public Key Address:',pub_key_address.to_string())
    redeem_script=create_redeem_script(seq,pub_key_address)
    # Confirm P2SH address containing funds to spend from
    print('Confirm P2SH Address containing funds:\n',P2shAddress.from_script(redeem_script).to_string())
    
    
    # Accept desitination p2pkh address from user
    user_pk2pkh=input('Enter a desitination P2PKH address:> \n') 
    p2pkh_address=P2pkhAddress(user_pk2pkh) 
    # spend coins from the P2SH address created
    validated_tx=spend_frm_P2SH_add(conn,seq,create_P2SH_address(create_redeem_script(seq,pub_key_address)),priv_key,redeem_script,p2pkh_address.to_string())
    
if __name__=="__main__":
    main()