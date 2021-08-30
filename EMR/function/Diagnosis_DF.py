import load_data

def makeDf(Schema):
    dataconn = load_data.LoadData()
    try:
        temp = dataconn.select_data(
            f"""
        SELECT   a.Diagnosis, d.NAME_ENG, d.NAME_KOR,am.Memo,s.CC FROM `{Schema}`.chartlist as c
        INNER JOIN `{Schema}`.assessment as a
        ON a.Chart_No = c.SNo
        INNER JOIN `{Schema}`.dx as d
        ON a.Dx_Code = d.SNO
        INNER JOIN `{Schema}`.assessment_memo as am
        ON am.Assessment_No = c.Sno
        INNER JOIN `{Schema}`.subjective as s
        ON s.Chart_No = c.SNo
        INNER JOIN `{Schema}`.pet as p
        ON p.SNO = c.Pet_NO
        INNER JOIN `{Schema}`.breed as b
        ON p.Breed = b.SNo
        WHERE b.Master_Code = 1 and d.bInsur = 1;
            """
        )
        dataconn.close()
        return temp
    except:
        print(f"{Schema} doesn't exist")
        

