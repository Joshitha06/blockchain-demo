from flask import Flask,render_template,request
import hashlib

app = Flask(__name__)

difficulty = 4


def calculate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def mine_block(block,data,prev):
    nonce=0
    while True:

        text=str(block)+str(nonce)+data+prev
        hash_value=calculate_hash(text)

        if hash_value.startswith("0"*difficulty):
            return nonce,hash_value

        nonce+=1


@app.route("/")
def hash_page():
    return render_template("hash.html")


@app.route("/block")
def block_page():

    prev="0"*64
    nonce,hash_value=mine_block(1,"",prev)

    return render_template("block.html",
                           nonce=nonce,
                           hash_value=hash_value,
                           prev=prev)


@app.route("/blockchain")
def blockchain_page():

    chain=[]
    prev="0"*64

    for i in range(1,6):

        nonce,hash_value=mine_block(i,"",prev)

        chain.append({
        "block":i,
        "nonce":nonce,
        "data":"",
        "prev":prev,
        "hash":hash_value
        })

        prev=hash_value

    return render_template("blockchain.html",chain=chain)


if __name__=="__main__":
    app.run(debug=True)
