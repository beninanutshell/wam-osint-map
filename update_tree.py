from json import dump, load

class convertion:
    def __init__(self, Dict:dict) -> None:
        self.dict = Dict

    def to_arf(self) -> dict:
        """Converts the userfriendly dict to the arf.json dict"""
        return self._to_arf(self.dict)
    
    def from_arf(self) -> dict: 
        """Converts the arf.json dict to the userfriendly dict"""
        return self._from_arf(self.dict)

    def _to_arf(self, dictio:dict) -> dict:
        retour = {}
        for k, v in dictio.items():
            retour["name"] = k
            if type(v) is dict:
                retour["children"] = [self._to_arf({x:y}) for x, y in v.items()]
                retour["type"] = "folder"
            elif type(v) is str:
                retour["url"] = v
                retour["type"] = "url"
            else:
                raise TypeError(f"{v} must be a dict or a string.")

        return retour

    def _from_arf(self, dictio:dict) -> dict:
        retour = {}
        if dictio["type"] == "url":
            retour[dictio["name"]] = dictio["url"]

        elif dictio["type"] == "folder":
            retour[dictio["name"]] = {}
            for item in dictio["children"]:
                retour[dictio["name"]].update(self._from_arf(item))

        return retour

    # module pour sort en alphabétique ?

def main() -> None:
    print("export ...", end="\r")
    c = convertion(load(open("database.json","r")))
    with open("js/db.json","w") as f:
        dump(c.to_arf(),f,indent=4)
    print("finished ! ")

if __name__ == "__main__":
    main()