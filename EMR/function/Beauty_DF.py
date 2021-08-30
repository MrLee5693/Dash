import load_data

def makeDf(Schema):
    dataconn = load_data.LoadData()
    try:
        temp = dataconn.select_data(   
            f"""
            SELECT bl.Name as BT, bt.Beauty_Count,bt.Price,b.Name2,b.Name3,p.Sex,timestampdiff(day,p.BirthDate,bt.Reg_Date) as `Day`,'{Schema}' as Label FROM `{Schema}`.beauty as bt
            JOIN `{Schema}`.pet as p ON p.SNo = bt.Pet_No
            JOIN `{Schema}`.breed as b ON b.SNo = p.Breed
            JOIN `{Schema}`.beautylist as bl ON bl.CODE = bt.Beauty_Code
            WHERE b.Master_Code = 1
            ;
            """
        )
        dataconn.close()
        return temp
    except:
        print(f"{Schema}.Beauty doesn't exist\n")







