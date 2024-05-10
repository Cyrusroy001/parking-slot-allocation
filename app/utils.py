def flatten_df(df):
    _slots=df.get("SlotID")
    _avail=df.get("Availability")
    _dict={
        "slots":[]
    }
    for i in range(len(_slots)):
        _dict.get("slots").append(
            {
                "id" : _slots[i].replace("IR", ""),
                "status" : map_avail(_avail[i])
            }
        )
    return _dict


def map_avail(status: int):
    if status==0:
        return "available"
    elif status==1:
        return "occupied"
    else:
        return "reserved for me"