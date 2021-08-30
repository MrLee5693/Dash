import load_data

def makeDf(Schema):
    dataconn = load_data.LoadData()
    try:
        temp = dataconn.select_data(   

            
            f"""
            SELECT DISTINCT b.Name2,b.Name3,p.Sex,vd.Name as Diagnosis,timestampdiff(day,p.BirthDate,vc.Reg_Date) as `Day`,timestampdiff(month,p.BirthDate,vc.Reg_Date) as `_Month`,timestampdiff(year,p.BirthDate,vc.Reg_Date) as `_Year` FROM `{Schema}`.vaccine_procdate as vc
            JOIN `{Schema}`.pet as p ON vc.Pet_No=p.SNO
            JOIN `{Schema}`.breed as b ON p.Breed = b.SNo
            JOIN `{Schema}`.vaccine_detail as vd ON vc.Vaccine_Code=vd.Code;
"""            
        )
        dataconn.close()
        return temp
    except:
        print(f"{Schema}.vital doesn't exist\n")




