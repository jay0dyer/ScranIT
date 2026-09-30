print("Welcome to the text ScranIT demo")

# slinence hugging face warning
import os
import warnings
os.environ["HF_HUB_VERBOSITY"] = "error"
warnings.filterwarnings("ignore", message=".*unauthenticated requests.*")

print("Initiating Search engine...")
from ScranSearch import ScranSearchEngine
engine = ScranSearchEngine()

resultFormat = """======================================================================
{ItemName} - {Price}
{Description}
from {restrauntname} @ {address} {postcode} / confidence {confidence}%"""

print("Suggested demo searchs inculde 'pizza', 'latte', 'dessert'")
while True:
    userinput = input("Enter a search >: ")
    results = engine.Search(userinput)
    for result in results:
        print(resultFormat.format(
            ItemName=result[0],
            Description=result[1],
            Price=result[2],
            restrauntname=result[3],
            postcode=result[4],
            address=result[5],
            confidence=result[7],
        ))
