import load_data

# Vital.Pet_No = Pet.SNo
def makeDf(Schema):
    dataconn = load_data.LoadData()
    try:
        temp = dataconn.select_data(   
            f"""
            SELECT DISTINCT p.SNo,p.Name,b.Name2,b.Name3,p.Sex,timestampdiff(day,p.BirthDate,v.VT_Date) as `Day`,v.VT_BW FROM `{Schema}`.pet as p
            JOIN `{Schema}`.breed as b ON p.Breed = b.SNo
            JOIN `{Schema}`.chartlist as c ON p.SNo = c.Pet_NO
            JOIN `{Schema}`.treatment as t ON p.SNo = t.Pet_No
            JOIN `{Schema}`.vital as v ON p.SNo = v.Pet_No
            WHERE b.Master_Code = 1 and c.SNo = t.Chart_No and timestampdiff(day,p.BirthDate,v.VT_Date) = timestampdiff(day,p.BirthDate,t.Insert_Date); 
            """
        )
        dataconn.close()
        return temp
    except:
        print(f"{Schema}.vital doesn't exist\n")
