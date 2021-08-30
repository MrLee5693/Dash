import load_data

def makeDf(Schema):
    dataconn = load_data.LoadData()
    temp = dataconn.select_data(
        """SELECT c.SNO, c.Pet_NO, c.Chart_Date, c.Class_Code
        FROM `%s`.chartlist as c; """ % Schema)
    dataconn.close()
    return temp

